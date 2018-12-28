import json
import re
import requests
from pprint import pprint
from natsort import natsorted
requests.packages.urllib3.disable_warnings()
def get_cookie(controller_ip):
    controller_url = "https://" + controller_ip + ":8443"
    path = "/api/v1/auth/login"
    url = controller_url + path
    data = '{"user": "readonly", "password": "password"}'
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

def get_ep(controller_ip,session_cookie):
    controller_url = "https://" + controller_ip + ":8443"
    path = '/api/v1/data/controller/applications/bcf/info/summary/fabric'
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

def main():
   controllers = {
          "10.1.1.10":"BCF1",
          "10.1.1.20":"BCF2",
          "10.1.1.30":"BCF3",
          "10.1.1.40":"BCF4",
         }
   tenant_all = {}
   eptotal = {}

   for controller_ip,fabric in natsorted(controllers.iteritems()):
      cookie = get_cookie(controller_ip)

      tenants = get_tenant(controller_ip,cookie)
      epcounts = get_ep(controller_ip,cookie)
      epcount = epcounts[0]['active-endpoint-count']
      eptotal[fabric] = epcount
      for i in tenants:
          name = i['name']
          epc = i['endpoint-count']
          if name in tenant_all:
             tenant_all[name][fabric] = epc
          else:
             tenant_all[name] = {}
             tenant_all[name]['BCF1'] = '-'
             tenant_all[name]['BCF2'] = '-'
             tenant_all[name]['BCF3'] = '-'
             tenant_all[name]['BCF4'] = '-'
             tenant_all[name][fabric] = epc

      delete_cookie(controller_ip,cookie) 

   print "%-25s %-5s %-5s %-5s %-5s" % ("tenant","BCF1","BCF2","BCF3","BCF4")
   for tenant_name, fabrics in tenant_all.items():
       print "%-25s %-5s %-5s %-5s %-5s" % (tenant_name,fabrics['BCF1'],fabrics['BCF2'],fabrics['BCF3'],fabrics['BCF4'])
   print "%-25s %-5s %-5s %-5s %-5s" % ("TOTAL",eptotal["BCF1"],eptotal["BCF2"],eptotal["BCF3"],eptotal["BCF4"])
   
if __name__ == "__main__":
  main()
