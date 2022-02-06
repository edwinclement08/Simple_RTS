__author__ = 'Edwin Clement'
map = [[0]*10 for t in xrange(10)]

start = (3, 3)
unchecked =[]
good_spots = []

##############################################################################
###########################  Spiral search ###################################
L = 4
x, y = (0, 0)
dx = 0
dy = -1
for i in range(L**2):
    if (-L/2 < x <= L/2) and (-L/2 < y <= L/2):
        unchecked.append((x + start[0], y + start[1]))
    if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
        dx, dy = -dy, dx
    x, y = x+dx, y+dy
##############################################################################


for t in unchecked:
    # if empty
        # if path to there
            # good_spots.append(t)
    print t

print "rshhg"

import time
time.sleep(443)