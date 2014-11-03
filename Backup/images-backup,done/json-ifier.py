__author__ = 'Clement'
d = open('Arrangement-backup.json','r')
print "Data --->"
print d.read()
print '-'*40

e = []
d.seek(0)
for m in d.readlines():
    if m =='\n':
        s = '\n'
    else:
        s = '['+m.rstrip('\n')+'],\n'
    e.append(s)
w = ''.join(e)
w='[' +w[:-4]+']'
print w