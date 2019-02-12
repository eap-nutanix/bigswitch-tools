import json
import re
import sys
import requests
from pprint import pprint
from natsort import natsorted
requests.packages.urllib3.disable_warnings()
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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

def get_ep(controller_ip,session_cookie):
    controller_url = "https://" + controller_ip + ":8443"
    path = '/api/v1/data/controller/applications/bcf/info/endpoint-manager/endpoint'
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
          "10.4.6.1":"BCF1",
          "10.4.6.2":"BCF2",
          "10.4.6.3":"BCF3",
          "10.4.6.4":"BCF4",
          "10.4.6.5":"BCF5",
         }
   lldp_all = {}
   search = sys.argv[1]

   for controller_ip,fabric in natsorted(controllers.iteritems()):
      cookie = get_cookie(controller_ip)

      ep_fabric = get_ep(controller_ip,cookie)
      for i in ep_fabric:
           if 'ip-address' in i.keys():
               ip_list = i['ip-address']
               for j in ip_list:
                   ip = j['ip-address']
                   if ip == search:
                      tenant = i['tenant']
                      vlan = i['vlan']
                      if vlan == -1:
                         vlan = 'untagged'
                      segment = i['segment']
                      if 'interface-group' in i.keys():
                         interface = i['interface-group']
                      if 'switch' in i.keys():
                         interface = i['interface']
                         switch = i['switch']
                         interface = switch + ":" + interface
                      print "%s %s %s %s %s %s" % (fabric,tenant,interface,segment,vlan,ip)

      delete_cookie(controller_ip,cookie) 

if __name__ == "__main__":
  main()
