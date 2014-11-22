#!/usr/bin/env python
# -*- coding: utf-8 -*-

import png
from copy import deepcopy

class Mapa:
    def __init__(self, lista):
        self.mapa = lista
        self.fil = len(self.mapa)
        self.col = len(self.mapa[0])
                
    def __str__(self):
        salida = ""
        for f in range(self.fil):
            for c in range(self.col):
                if self.output[f][c] == 0:
                    salida += "  "
                elif self.output[f][c] == 4:
                    salida += ". "
                elif self.output[f][c] != 0:
                    salida += "# "
            salida += "\n"
        return salida
        
    def camino(self, lista):
        self.output = deepcopy(self.mapa)
        del lista[-1]
        for i in range(len(lista)):
            self.output[lista[i][0]][lista[i][1]] = 4
    
    def valid_point(self, pos):
        if self.mapa[pos[0]][pos[1]] != 0:
            return False
        return True
        
class Node:
    def __init__(self, pos=[0, 0], destination=[0, 0],  parent=None):
        self.pos = pos
        self.parent = parent
        self.h = distance(self.pos, destination)
        
        if self.parent == None:
            self.g = 0
        else:
            self.g = self.parent.g + 1
        self.f = self.g + self.h


class AStar:
    def __init__(self, mapa):
        self.mapa = mapa

    def get_path_from_a_to_b(self, pos_a, pos_b):
        """
        This method returns a list of nodes as a path from pos_a to pos_b
        """
        # Nodes from start to end
        self.start = Node(pos_a, pos_b)
        self.end = Node(pos_b, pos_b)
        
        # Creates open and closed lists.
        self.open_list = []
        self.closed_list = []
        
        # Adds initial node to the closed list.
        self.closed_list.append(self.start)
        
        # Adds neighbors to the open list
        self.open_list += self.neighbors(self.start)
        
        # As long as the objective is not in the closed list, we keep searching
        while self.objective():
            self.search()
            
        self.path = self.get_path()
        
        return self.path
            
            
    def neighbors(self, node):
        """
        Returns a list of neighbors reachables from node 
        """
        
        #neighbors = []
        #for i in [-1, 1]:
            #if self.mapa.mapa[node.pos[0]+i][node.pos[1]] == 0:
                #neighbors.append(Node([node.pos[0]+i, node.pos[1]], self.end.pos, node))
                
        #for i in [-1, 1]:
            #if self.mapa.mapa[node.pos[0]][node.pos[1]+i] == 0:
                #neighbors.append(Node([node.pos[0], node.pos[1]+i], self.end.pos, node))
                  
        #return neighbors
    
        # To allow walking in diagonal, comment the upper part of this method
        # and uncomment the following
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0 :
                    continue
                try:
                    if self.mapa.mapa[node.pos[0]+i][node.pos[1]+j] == 0:
                        neighbors.append(Node([node.pos[0]+i, node.pos[1]+j], self.end.pos, node))
                except:
                    pass
                  
        return neighbors
          
    def move_lower_f(self):
        """
        Moves an element with the lower f, from the open list to the closed one
        """
        a = self.open_list[0]
        for i in self.open_list:
            if i.f < a.f:
                a = i
        self.closed_list.append(a)
        del self.open_list[self.open_list.index(a)]
        
    
    # Comprueba si un nodo está en una lista.   
    def en_lista(self, nodo, lista):
        for i in lista:
            if nodo.pos == i.pos:
                return True
        return False
    
    
    # Gestiona los vecinos del nodo seleccionado.   
    def route(self):
        """
        Manages the neighbors for the selected node
        """
        for i in self.nodes:
            if self.en_lista(i, self.closed_list):
                continue
            elif not self.en_lista(i, self.open_list):
                self.open_list.append(i)
            else:
                if self.select.g + 1 < i.g:
                    for j in self.open_list:
                        if i.pos == j.pos:
                            del self.open_list[self.open_list.index(j)]
                            self.open_list.append(i)
                            break
                    
    def search(self):
        """
        Analizes the last element of the closed list
        """
        self.move_lower_f()
        self.select = self.closed_list[-1]
        self.nodes = self.neighbors(self.select)
        self.route()
    
    def objective(self):
        """
        Checks if the objective is in the open list
        """
        for i in self.open_list:
            if self.end.pos == i.pos:
                return False
        return True
        
    
    def get_path(self):
        """
        Returns a list with positions for the path to follow
        """
        for i in self.open_list:
            if self.end.pos == i.pos:
                objective = i
        
        path = []
        while objective.parent != None:
            path.append(objective.pos)
            objective = objective.parent
            
        path.reverse()
        return path
            
    
def distance(a, b):
    """
    Distance between two points
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------------------------------------------

def main():
    bitmap_mask = []
    for row in png.Reader('data/Test_Collition.png').asDirect()[2]:
        bitmap_mask.append(row[3::4])

    mapa = Mapa(bitmap_mask)
    A = AStar(mapa)
    
    while True:
        valid = False
        while not valid:
            origen = map(int, raw_input("Origen: ").split(','))
            valid = mapa.valid_point(origen)
        
        valid = False
        while not valid:
            destino = map(int, raw_input("Destino: ").split(','))
            valid = mapa.valid_point(origen)
        
        A.get_path_from_a_to_b(origen, destino)
        
        mapa.camino(A.path)
        print mapa
    return 0

if __name__ == '__main__':
    main()
