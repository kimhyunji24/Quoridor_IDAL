basic_operations = 0

def BFS(maze, start, end):
    '''"Brute-Force Search"
    :param maze(list): the maze to be navigated
    :param start(tuple): the starting coordinates (row, col)
    :param end(tuple): the end coordinates (row, col)
    :return: shortest path from start to end
    '''
    queue = [start]
    visited = set()

    while len(queue) != 0:
        if queue[0] == start:
            path = [queue.pop(0)]  # Required due to a quirk with tuples in Python
        else:
            path = queue.pop(0)
        front = path[-1]
        if front == end:
            return len(path)
        elif front not in visited:
            for adjacentSpace in getAdjacentSpaces(maze, front, visited):
                newPath = list(path)
                newPath.append(adjacentSpace)
                queue.append(newPath)
                global basic_operations
                basic_operations += 1
            visited.add(front)
    return 0


def getAdjacentSpaces(maze, space, visited):
    ''' Returns all legal spaces surrounding the current space
    :param space: tuple containing coordinates (row, col)
    :return: all legal spaces
    '''
    spaces = list()
    spaces.append((space[0]-1, space[1]))  # Up
    spaces.append((space[0]+1, space[1]))  # Down
    spaces.append((space[0], space[1]-1))  # Left
    spaces.append((space[0], space[1]+1))  # Right

    final = list()
    for i in spaces:
        if maze[i[0]][i[1]] != 1 and i not in visited:
            final.append(i)
    return final