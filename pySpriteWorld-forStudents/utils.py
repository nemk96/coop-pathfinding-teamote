import numpy as np
### Heuristics
def manhattan(c_1,c_2):
     return abs(c_1[0]-c_2[0])+ abs(c_1[1]-c_2[1])

def euclidian(c_1,c_2):
    return np.sqrt((c_1[0]-c_2[0])**2+ (c_1[1]-c_2[1])**2)

def true(c_1,c_2):
    return max(abs(c_1[0]-c_2[0]),abs(c_1[1]-c_2[1]))


## A star
class Position():
    def __init__(self,
                 coords,
                 parent=None,
                 g=0,
                 h=0):
        self.coords = coords
        self.parent = parent
        self.g = g
        self.h = h
        self.f = h+g

    def __eq__(self, position):
        return self.coords == position.coords

    def replace(self, position):
        self.parent = position.parent
        self.g = position.g
        self.h = position.h
        self.f = position.f

def wall_to_matrix(wallStates):
    matrix = np.zeros((20,20), dtype=int)
    for pos in wallStates:
        matrix[pos[0],pos[1]] =1
    return matrix




def check_move(coords, wallStates):
    x,y = coords
    test_1 = (x>=0) and (x<20)
    test_2 = (y>=0) and (y<20)
    if test_1 and test_2:
        if type(wallStates) == list:
            return not(coords in wallStates)
        else:
            return (wallStates[x,y] == 0)
    else:
        return False

def check_closed(closed, position):
    tests = list(map(lambda aux: aux == position, closed))
    return any(tests)

def check_open(open, position):
    tests = list(map(lambda aux: aux == position, open))
    if any(tests):
        return open[tests.index(True)]
    else:
        return None

def get_children(parent, destination, wallStates, distance):
    children = []
    for action in [(0,1),(0,-1),(1,0),(-1,0)]:
        coords = (parent.coords[0]+action[0], parent.coords[1]+action[1])
        if check_move(coords, wallStates):
            g = parent.g+1
            h = distance(coords,parent.coords)
            child = Position(g=g,h=h,coords=coords,parent=parent)
            children.append(child)
    return children

def a_search(start, destination, wallStates, distance=manhattan):
    start = Position(start)
    destination = Position(destination)
    open, closed = [start], []
    num_iter = 0
    while len(open) != 0:
        num_iter += 1
        actual_idx = sorted(range(len(open)), key=lambda idx: open[idx].f)[0]
        actual_pos = open[actual_idx]
        open.pop(actual_idx)
        closed.append(actual_pos)
        if actual_pos.coords == destination.coords:
            path = []
            while actual_pos != start:
                path.append(actual_pos.coords)
                actual_pos = actual_pos.parent
            return path[::-1], num_iter
        else:
            children = get_children(actual_pos, destination, wallStates, distance)
            for child in children:
                if check_closed(closed, child):
                    continue
                other_position = check_open(open, child)
                if other_position is None:
                    open.append(child)
                else:
                    if child.f < other_position.f:
                        other_position.replace(child)
    print('Pas de chemin possible')

## Temporal A star
def check_move_bis(coords, wallStates, timetable, prev_coords=None):
    x,y,t = coords

    test_1 = (x,y) not in wallStates
    if prev_coords is not None:
        prev_x, prev_y, prev_t = prev_coords
        add_test = ((x,y,prev_t) in timetable) and ((prev_x,prev_y,t) in timetable)
        test_1 = test_1 and (not add_test)
    test_2 = (x>=0) and (x<20)
    test_3 = (y>=0) and (y<20)
    return test_1 and test_2 and test_3

def get_children_bis(parent, destination, wallStates, timetable, distance=manhattan):
    children = []
    for action in [(0,1),(0,-1),(1,0),(-1,0),(0,0)]:
        coords = (parent.coords[0]+action[0], parent.coords[1]+action[1], parent.coords[2]+1)
        if action == (0,0):
            prev_coords = None
        else:
            prev_coords = parent.coords
        if check_move_bis(coords, wallStates, timetable, prev_coords):
            g = parent.g +1
            h = distance(coords,parent.coords)
            child = Position(g=g,h=h,coords=coords,parent=parent)
            children.append(child)
    coords = (parent.coords[0], parent.coords[1], parent.coords[2]+1)
    return children

def a_search_bis(start, destination, wallStates, timetable, max_length=None):
    start = Position(start)
    destination = Position(destination)
    open, closed = [start], []
    t = 0
    maximas = []
    while len(open) != 0:
        t += 1
        actual_idx = sorted(range(len(open)), key=lambda idx: open[idx].f)[0]
        actual_pos = open[actual_idx]
        open.pop(actual_idx)
        closed.append(actual_pos)
        if actual_pos.coords[:2] == destination.coords[:2]:
            path = []
            while actual_pos != start:
                path.append(actual_pos.coords)
                timetable.append(actual_pos.coords)
                actual_pos = actual_pos.parent
            path.append(start.coords)

            return path[::-1], timetable, t,True
        else:
            if max_length is not None:
                if actual_pos.coords[-1] == max_length:
                    maximas.append(actual_pos)
                    continue
            children = get_children_bis(actual_pos, destination, wallStates, timetable)
            for child in children:
                if check_closed(closed, child):
                    continue
                other_position = check_open(open, child)
                if other_position is None:
                    open.append(child)
                else:
                    if child.f < other_position.f:
                        other_position.replace(child)
    maximas = sorted(maximas, key=lambda pos: pos.f)
    actual_pos = maximas[-1]
    path = []
    while actual_pos != start:
        path.append(actual_pos.coords)
        timetable.append(actual_pos.coords)
        actual_pos = actual_pos.parent
    path.append(start.coords)
    return path[::-1], timetable, t, False
