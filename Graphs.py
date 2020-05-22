def dijkstra(a, start, finish):
    ways = list()
    for i in range(len(a)):
        ways.append(list())
        ways[i].append(1000)
    ways[start][0] = 0
    ways = rec_dijkstra(a, start, ways)
    ways[finish].append(finish)
    print("Найкращий шлях з", start, "до", finish, ":")
    print(ways[finish][1:])


def rec_dijkstra(a, point, ways):
    for i in range(len(a)):
        if (a[point][i]) and (ways[i][0] > ways[point][0] + a[point][i]):
            ways[i][0] = ways[point][0] + a[point][i]
            ways[i][1:] = ways[point][1:]
            ways[i].append(point)
            ways = rec_dijkstra(a, i, ways)
    return (ways)



def floydUorshall(x):
    for i in range(len(x)):
        for j in range(len(x)):
            if x[i][j]==0:
                x[i][j]=1000
    for k in range(len(x)):
        for l in range(len(x)):
            for m in range(len(x)):
                x[l][m]=min(x[l][m], x[l][k]+x[k][m])
    return x


def BellmanFord(x,k):
    a=list()
    for i in range(len(x)):
        a.append(1000)
    a[k]=0
    for l in range(len(x)-1):
        for i in range(len(x)):
            for j in range(len(x)):
                if(x[j][i]!=0):
                    a[i]=min(a[i], a[j]+x[j][i])
    for i in range(len(x)):
        for j in range(len(x)):
            if x[j][i]!=0 and a[i] > a[j] + x[j][i]:
                print("Graph have negative weight cycle")
                return a
    return a

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def Astar(x, start, end):
    start = Node(None, start)
    end = Node(None, end)
    open = [start]
    closed = []
    while open:
        current = open[0]
        currentInd = 0
        for index, item in enumerate(open):
            if item.f < current.f:
                current = item
                currentInd = index
        open.pop(currentInd)
        closed.append(current)
        if current == end:
            path = []
            current = current
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        children = []
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nodePos = (current.position[0] + newPos[0], current.position[1] + newPos[1])
            if nodePos[0] > (len(x) - 1) or nodePos[0] < 0 or nodePos[1] > (len(x[len(x)-1]) -1) or nodePos[1] < 0:
                continue
            if x[nodePos[0]][nodePos[1]] != 0:
                continue
            newNode = Node(current, nodePos)
            children.append(newNode)
        for child in children:
            for closedChild in closed:
                if child == closedChild:
                    continue
            child.g = current.g + 1
            child.h = ((child.position[0] - end.position[0]) ** 2) + ((child.position[1] - end.position[1]) ** 2)
            child.f = child.g + child.h
            for openNode in open:
                if child == openNode and child.g > openNode.g:
                    continue
            open.append(child)


x = [[6, 1, 3, 1, 0], [1, 0, 1, 3, 4], [1, 1, 0, 1, 1], [1, 1, 3, 0, 0], [0, 1, 1, 4, 1]]
dijkstra(x, 1, 4)
x = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
     [1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
print("Найкоротший шлях по вказаних точках в таблиці :")
print(Astar(x, (0, 0), (9, 9)))
x = [[6, 1, 3, 1, 0], [-1, 0, 1, 3, 4], [1, 1, 0, 1, 1], [1, 1, 3, 0, 0], [0, 1, 1, 4, 1]]
print("Найкоротші довжини шляхів від кожної вершини до кожної :")
print(floydUorshall(x))
x = [[6, 1, 3, 1, 0], [-1, 0, 1, 3, 4], [-1, -1, 0, 1, -1], [1, 1, 3, 0, 0], [0, 1, 1, 4, 1]]
print("Найкоротші довжини шляхів від 1 вершини до кожної :")
print(BellmanFord(x,0))