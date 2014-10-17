matrix = [[3, 4, 1, 2, 0],
          [0, 1, 0, 4, 2],
          [2, 2, 3, 1, 4],
          [2, 0, 4, 2, 1],
          [1, 2, 0, 3, 4]]
size = 5
value = {1, 2, 3}

p = (3,0)
q = (1,4)

N4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
N8 = [(1, 0), (1, 1), (-1, 0), (-1, 1), (0, 1), (1, 1), (0, -1), (1, -1)]
Nm = [(1, 0), (1, 1), (-1, 0), (-1, 1), (0, 1), (1, 1), (0, -1), (1, -1)]



def getN(x, y, d):
    nd = filter(lambda xy: x + xy[0] >= 0 and x + xy[0] < size and y + xy[1] >= 0 and y + xy[1] < size, d)
    return map(lambda xy: (x + xy[0], y + xy[1]), nd)

def bfs(x, y, n):
    queue = [(x, y)]
    component = set()
    source = {}
    print queue, component
    print '-----------------'
    while len(queue) != 0:
        here = queue[0]
        ns = getN(here[0], here[1], n)
        ns = filter(lambda xy: matrix[xy[0]][xy[1]] in value, ns)
        ns = filter(lambda xy: xy not in component, ns)
        print ns
        for xy in ns:
            source[xy] = here

        queue += ns
        print queue
        component.add(queue.pop(0))
        print component
        print '-------------'
        print source
        if q in component:
            print "found"
            cur = q
            print q,
            while cur != p:
                old = cur
                print '<-', source[cur],
                cur = source[cur]
                del source[old]

            break