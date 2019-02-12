# bigswitch-tools

Eric Pearce eric.pearce@nutanix.com

I do not claim to have written all code myself - fragments may be recognizable as coming from stackoverflow or other python examples. Use at your own risk.  Beware that the script is hardcoded to our particular environment (see bottom).

**show_xfabric.py** - iterates through all fabrics, producing endpoint count for each tenant in each fabric and grand total for fabric at end.  A '-' symbol means tenant is not present in that fabric.

Sample output:
```
$ python show_xfabric.py 
tenant                    BCF1  BCF2  BCF3  BCF4    
IT-Staging                0     -     -     -       
eng-calm-blr              -     199   -     -    
eng-prism-qa-blr          136   -     -     -     
IT-Production             105   -     -     -       
eng-sre-escalation        -     109   -     -    
eng-xtract                -     195   -     -       
eng-foundation            -     -     0     -    
eng-prism-infra           90    -     -     -    
eng-infra-core-hq         524   -     -     -    
eng-dev-blr               -     420   -     -    
eng-process-infra         26    -     -     -    
system                    0     0     0     0    
eng-dev-ext               -     -     -     58   
eng-cdv-era               -     554   -     -    
it-dev-xi                 13    -     -     -    
eng-dev-prism             19    -     -     -    
eng-afs                   -     2194  -     -    
eng-qa-ahv                -     511   -     -       
tenant0                   68    107   -     8       
eng-solution-lab-2        -     -     105   -    
eng-solution-lab-1        277   -     -     -    
EDGE                      1     1     1     1    
eng-cdp-dr                2357  -     -     -        
it-build-infra            690   -     -     -    
it-ericpearce             14    -     14    0    
TOTAL                     7014  14048 914   1330
```

There are several hard-coded parameters that you will have to customize for your environment:
*Fabric Username and Password:*
```
  data = '{"user": "readonly", "password": "password"}'
```
*Controller IPs and names:*
```
   controllers = {
          "10.1.1.10":"BCF1",
          "10.1.1.20":"BCF2",
          "10.1.1.30":"BCF3",
          "10.1.1.40":"BCF4",
         }
```
*Controller names:*
```
             tenant_all[name]['BCF1'] = '-'
             tenant_all[name]['BCF2'] = '-'
             tenant_all[name]['BCF3'] = '-'
             tenant_all[name]['BCF4'] = '-'
```
*Number of and names of controllers:*
```
   print "%-25s %-5s %-5s %-5s %-5s" % ("tenant","BCF1","BCF2","BCF3","BCF4")
   for tenant_name, fabrics in tenant_all.items():
       print "%-25s %-5s %-5s %-5s %-5s" % (tenant_name,fabrics['BCF1'],fabrics['BCF2'],fabrics['BCF3'],fabrics['BCF4'])
   print "%-25s %-5s %-5s %-5s %-5s" % ("TOTAL",eptotal["BCF1"],eptotal["BCF2"],eptotal["BCF3"],eptotal["BCF4"])
```
**search_xfabric.py** -- Search for LLDP-provided hostname across fabrics - displays fabric, tenant, switch, port, vlan and all hostname matches using Unix-style wildcards:
```
# python search_xfabric.py 'iguanodon1*'
BCF5 eng-systems-qa-2x5 p5r7r11-leaf1 ethernet11:4 untagged Iguanodon10-4
BCF5 eng-systems-qa-2x5 p5r7r11-leaf1 ethernet11:1 untagged Iguanodon10-1
BCF5 eng-systems-qa-2x5 p5r7r11-leaf1 ethernet11:2 untagged Iguanodon10-2
BCF5 eng-systems-qa-2x5 p5r7r11-leaf1 ethernet11:3 untagged Iguanodon10-3
BCF5 eng-systems-qa-2x5 p5r7r11-leaf2 ethernet11:1 untagged Iguanodon10-1
BCF5 eng-systems-qa-2x5 p5r7r11-leaf2 ethernet11:4 untagged Iguanodon10-4
BCF5 eng-systems-qa-2x5 p5r7r11-leaf2 ethernet11:2 untagged Iguanodon10-2
BCF5 eng-systems-qa-2x5 p5r7r11-leaf2 ethernet11:3 untagged Iguanodon10-3
# python search_xfabric.py '*miette*'
BCF4 it-eric-pearce p4r6r02-leaf1 ethernet27:1 untagged miette-2
BCF4 it-eric-pearce p4r6r02-leaf1 ethernet27:2 untagged miette-1
BCF4 it-eric-pearce p4r6r02-leaf1 ethernet27:3 untagged miette-3
BCF4 it-eric-pearce p4r6r02-leaf2 ethernet27:1 untagged miette-2
BCF4 it-eric-pearce p4r6r02-leaf2 ethernet27:2 untagged miette-1
BCF4 it-eric-pearce p4r6r02-leaf2 ethernet27:3 untagged miette-3
```
This is mainly for people handling tickets, as all they get from the customer is a hostname, and they need to map this to a bunch of attributes in order to debug the issue.

**get_controllers.py** - Helper to find which controller to talk to for a given tenant name (should not be needed after MCD is available)
```
# python get_tenant.py it-eric-pearce
get_controllers = ['10.4.6.3', '10.4.6.4']
# python get_tenant.py it-eric-pearc
get_controllers = None
```
**findip.py** - Search all fabrics for IP address and print fabric, tenant, segment, vlan and matching IP. Beware this is quite slow, as it produces an endpoint list for every fabric and searches it in a linear fashion.
```
# python findip.py 10.5.9.24
BCF4 it-eric-pearce p4r6r02-leaf1:ethernet27:4 host-cvm untagged 10.5.9.24

# python findip.py 10.4.153.200
BCF1 eng-infra-core p1r1r11-leaf2:ethernet9:1 host-cvm-uvm untagged 10.4.153.200
BCF3 eng-infra-core-1 uplinks-to-bcf0 host-cvm-uvm 601 10.4.153.200
```
