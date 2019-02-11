import json
import sys
import re
import requests
from pprint import pprint
from natsort import natsorted
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
def get_cookie(controller_ip):
    controller_url = "https://" + controller_ip + ":8443"
    path = "/api/v1/auth/login"
    url = controller_url + path
    data = '{"user": "readonly", "password": "secret"}'
    headers = {"content-type": "application/json"}
    response = requests.request('POST', url, data=data, headers=headers, verify=False) 
    cookie = json.loads(response.content)['session_cookie']
    session_cookie = 'session_cookie=%s' % cookie
    return(session_cookie)

def get_tenant(controller_ip,session_cookie):
    controller_url = "https://" + controller_ip + ":8443"
    path = '/api/v1/data/controller/applications/bcf/info/endpoint-manager/tenant'
    url = controller_url + path
    data = ''
    headers = {"content-type": "application/json", 'Cookie': session_cookie}
    response = requests.request('GET', url, data=data, headers=headers, verify=False)
    response_dict = json.loads(response.content)
    return(response_dict)

def delete_cookie(controller_ip,session_cookie):
    controller_url = "https://" + controller_ip + ":8443"
    path = '/api/v1/data/controller/core/aaa/session[auth-token="'+session_cookie+'"]'
    url = controller_url + path
    headers = {"content-type": "application/json", 'Cookie': session_cookie}
    response = requests.request('DELETE', url, headers=headers, verify=False)

def get_controllers(search):
   controllers = {
          "10.4.6.1":"BCF1",
          "10.4.6.2":"BCF2",
          "10.4.6.3":"BCF3",
          "10.4.6.4":"BCF4",
          "10.4.6.5":"BCF5",
         }
   tenant_all = {}
   for controller_ip,fabric in natsorted(controllers.iteritems()):
      cookie = get_cookie(controller_ip)

      tenants = get_tenant(controller_ip,cookie)
      for i in tenants:
          name = i['name']
          if name not in tenant_all:
             tenant_all[name] = []
          tenant_all[name].append(controller_ip)
      delete_cookie(controller_ip,cookie)

   if search in tenant_all:
      return(tenant_all[search])
   else:
      return(None)
      

def main():
   search = sys.argv[1]
   print "get_controllers = %s" % (get_controllers(search)) 

if __name__ == "__main__":
  main()
