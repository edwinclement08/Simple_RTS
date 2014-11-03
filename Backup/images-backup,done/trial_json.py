__author__ = 'Edwin Clement'

import json

d = open('map.json','r')
k = d.read()
s = json.loads(k)



print json.dumps(s, separators=(',', ': '))