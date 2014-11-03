class ds:
    x, y, w, h = 3, 3, 5, 4

def get_neighbour(self):
    x, y, w, h = self.x, self.y, self.w, self.h

    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    occupied = set([])
    for my in range(y, y+h):
        for mx in range(x, x+w):
            occupied.add((mx, my))
    print occupied
    all_cover = set([])
    for s in occupied:
        for q in directions:
            all_cover.add((s[0]+q[0], s[1]+q[1]))
    actual_neighbours = all_cover - occupied
    return list(actual_neighbours)

m = ds()

ret = get_neighbour(m)
display = [[0]*10 for f in range(10)]

for q in ret:
    display[q[1]][q[0]] = 1

for y in display:
    for x in y:
        if x == 1:
            print "#",
        else:
            print "*",
    print 
