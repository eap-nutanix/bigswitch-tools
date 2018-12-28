# bigswitch-tools

**show_xfabric.py** - iterates through all fabrics, producing endpoint count for each tenant in each fabric and grand total for fabric at end.

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
