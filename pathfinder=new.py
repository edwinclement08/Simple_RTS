class Star(object):
    def __init__(self, parent):
        self.moves = [(1, 0), (-1, 0), (0,  1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.heuristic = lambda x, y: max(x, y)
        self.parent = parent

        # Just for definition sake
        self.start, self.end, self.map = None, None, None
        self.solution, self.solved = [], False
        self.hx, self.gx, self.fx = {}, {}, {}
        self.closed_set,  self.came_from, self.current = None, None, None
        # self.open_set =  None

    def find_path(self, start, end):
        self.start, self.end = start, end
        # self.map = self.parent.game_data.places_occupied
        self.map = [[0]*10 for t in range(10)]
        self.setup()
        return self.evaluate()

    def setup(self):
        print "setup"
        self.closed_set = set(self.start)  # Set of cells already evaluated
        self.open_set = set()  # Set of cells to be evaluated.
        self.came_from = {}  # Used to reconstruct path once solved.
        self.gx = {self.start: 0}  # Cost from start to current position.
        self.hx = {}  # Optimal estimate to goal based on heuristic.
        self.fx = {}  # Distance-plus-cost heuristic function.
        self.current = self.start
        self.current = self.follow_current_path()
        self.solution = []
        self.solved = False

    def get_neighbors(self):
        """Find adjacent neighbors with respect to how our agent moves."""
        neighbors = set()
        for (i, j) in self.moves:
            check = (self.current[0]+i, self.current[1]+j)
            if check not in self.closed_set:
                if self.map[check[1]][check[0]] == 0:
                    neighbors.add(check)
        return neighbors

    def follow_current_path(self):
        next_cell = None
        for cell in self.get_neighbors():
            tentative_gx = self.gx[self.current]+1
            if cell not in self.open_set:
                self.open_set.add(cell)
                tentative_best = True
            elif cell in self.gx and tentative_gx < self.gx[cell]:
                tentative_best = True
            else:
                tentative_best = False

            if tentative_best:
                x, y = abs(self.end[0]-cell[0]), abs(self.end[1]-cell[1])
                self.came_from[cell] = self.current
                self.gx[cell] = tentative_gx
                self.hx[cell] = self.heuristic(x, y)
                self.fx[cell] = self.gx[cell]+self.hx[cell]
                if not next_cell or self.fx[cell]<self.fx[next_cell]:
                    next_cell = cell
        return next_cell

    def get_path(self, cell):
        """Recursively reconstruct the path. No real need to do it recursively."""
        if cell in self.came_from:
            self.solution.append(cell)
            self.get_path(self.came_from[cell])

    def evaluate(self):
        """Core logic for executing the A* algorithm."""
        if self.open_set and not self.solved:
            print "op but nmot"
            for cell in self.open_set:
                print 'gse'
                if (self.current not in self.open_set) or (self.fx[cell] < self.fx[self.current]):
                    print "hgyujkgky"
                    self.current = cell
            if self.current == self.end:
                self.get_path(self.current)
                self.solved = True
            self.open_set.discard(self.current)
            self.closed_set.add(self.current)
            self.current = self.follow_current_path()

        elif not self.solution:
            self.solution = None
        return self.solution


c = Star("Friar")
print c.find_path((2, 2), (7, 7))