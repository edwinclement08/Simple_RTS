__author__ = 'Clement'

data = [[0,0,"smooth.grass",305],
[2,0,"rough.grass",278],
[4,0,"road",160],
[6,0,"mountain",211],

[0,2,"road.left.grass",108],
[2,2,"road.up.grass",84],
[4,2,"road.right.grass",112],
[6,2,"road.down.grass",136],

[0,4,"cliff.left.top.grass",293],
[2,4,"cliff.right.top.grass",297],
[4,4,"cliff.left.bottom.grass",313],
[6,4,"cliff.right.bottom.grass",317],

[0,6,"cliff.horizontal.grass",295],
[2,6,"cliff.vertical.grass",84],
[4,6,"useless",-1],
[6,6,"useless",-1],

[0,8,"soil.left.top.grass",199],
[2,8,"soil.right.top.grass",-1],
[4,8,"soil.left.bottom.grass",219],
[6,8,"soil.right.bottom.grass",223],

[0,10,"soil.left.grass",209],
[2,10,"soil.top.grass",201],
[4,10,"soil.left.grass",213],
[6,10,"soil.bottom.grass",221],

[0,12,"soil.left.top.grass.invert",293],
[2,12,"soil.right.top.grass.invert",297],
[4,12,"soil.left.bottom.grass.invert",313],
[6,12,"soil.right.bottom.grass.invert",317],

[0,14,"tree1.0.0",338],
[2,14,"tree1.1.0",340],
[4,14,"tree1.2.0",342],
[6,14,"mine.1",289],

[0,16,"tree1.0.1",352],
[2,16,"tree1.1.1",354],
[4,16,"tree1.2.1",356],
[6,16,"mine.2",290],

[0,18,"tree1.0.2",366],
[2,18,"tree1.1.2",368],
[4,18,"tree1.2.2",370],
[6,18,"mine.3",291],

[0,20,"tree2.0.0", 382],
[2,20,"tree2.1.0", 384],
[4,20,"tree2.0.1", 396],
[6,20,"tree2.1.1", 398]]

l = []
for t in data:
    l.append([t[3],t[2],[t[0],t[1]]])
for m in l:
    print str(m)+','

new_data = [
[305, 'smooth.grass', [0, 0]],
[278, 'rough.grass', [2, 0]],
[160, 'road', [4, 0]],
[211, 'mountain', [6, 0]],
[108, 'road.left.grass', [0, 2]],
[84, 'road.up.grass', [2, 2]],
[112, 'road.right.grass', [4, 2]],
[136, 'road.down.grass', [6, 2]],
[293, 'cliff.left.top.grass', [0, 4]],
[297, 'cliff.right.top.grass', [2, 4]],
[313, 'cliff.left.bottom.grass', [4, 4]],
[317, 'cliff.right.bottom.grass', [6, 4]],
[295, 'cliff.horizontal.grass', [0, 6]],
[84, 'cliff.vertical.grass', [2, 6]],
[-1, 'useless', [4, 6]],
[-1, 'useless', [6, 6]],
[199, 'soil.left.top.grass', [0, 8]],
[-1, 'soil.right.top.grass', [2, 8]],
[219, 'soil.left.bottom.grass', [4, 8]],
[223, 'soil.right.bottom.grass', [6, 8]],
[209, 'soil.left.grass', [0, 10]],
[201, 'soil.top.grass', [2, 10]],
[213, 'soil.left.grass', [4, 10]],
[221, 'soil.bottom.grass', [6, 10]],
[293, 'soil.left.top.grass.invert', [0, 12]],
[297, 'soil.right.top.grass.invert', [2, 12]],
[313, 'soil.left.bottom.grass.invert', [4, 12]],
[317, 'soil.right.bottom.grass.invert', [6, 12]],
[338, 'tree1.0.0', [0, 14]],
[340, 'tree1.1.0', [2, 14]],
[342, 'tree1.2.0', [4, 14]],
[289, 'mine.1', [6, 14]],
[352, 'tree1.0.1', [0, 16]],
[354, 'tree1.1.1', [2, 16]],
[356, 'tree1.2.1', [4, 16]],
[290, 'mine.2', [6, 16]],
[366, 'tree1.0.2', [0, 18]],
[368, 'tree1.1.2', [2, 18]],
[370, 'tree1.2.2', [4, 18]],
[291, 'mine.3', [6, 18]],
[382, 'tree2.0.0', [0, 20]],
[384, 'tree2.1.0', [2, 20]],
[396, 'tree2.0.1', [4, 20]],
[398, 'tree2.1.1', [6, 20]]
]