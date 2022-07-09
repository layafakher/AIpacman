import graph_and_searchAlgorithms


class Node:
    def __init__(self, u=0, r=0, d=0, l=0):
        self.u = u
        self.r = r
        self.d = d
        self.l = l


def createMap():
    nodes = []
    nodes.append(Node(-10, 8, 1, -10))
    nodes.append(Node(0, -10, 2, -10))
    nodes.append(Node(1, 10, -10, -10))
    nodes.append(Node(-10, 11, 4, -10))
    nodes.append(Node(3, -10, 5, -10))
    nodes.append(Node(4, -10, 6, -10))
    nodes.append(Node(5, -10, -10, -10))
    nodes.append(Node(-10, 15, -10, -10))

    nodes.append(Node(-10, 16, 9, 0))
    nodes.append(Node(8, -10, -10, -10))
    nodes.append(Node(-10, 18, -10, 2))
    nodes.append(Node(-10, 19, -10, 3))
    nodes.append(Node(-10, -10, 13, -10))
    nodes.append(Node(12, 21, 14, -10))
    nodes.append(Node(13, -10, 15, -10))
    nodes.append(Node(14, 23, -10, 7))

    nodes.append(Node(-10, 24, 17, 8))
    nodes.append(Node(16, -10, -10, -10))
    nodes.append(Node(-10, -10, 19, 10))
    nodes.append(Node(18, -10, 20, 11))
    nodes.append(Node(19, 28, -10, -10))
    nodes.append(Node(-10, -10, 22, 13))
    nodes.append(Node(21, -10, -10, -10))
    nodes.append(Node(-10, 31, -10, 15))

    nodes.append(Node(-10, -10, 25, 16))
    nodes.append(Node(24, -10, 26, -10))
    nodes.append(Node(25, -10, 27, -10))
    nodes.append(Node(26, 35, -10, -10))
    nodes.append(Node(-10, -10, 29, 20))
    nodes.append(Node(28, -10, 30, -10))
    nodes.append(Node(29, -10, 31, -10))
    nodes.append(Node(30, -10, -10, 23))

    nodes.append(Node(-10, 40, 33, -10))
    nodes.append(Node(32, -10, 34, -10))
    nodes.append(Node(33, -10, 35, -10))
    nodes.append(Node(34, -10, 36, 27))
    nodes.append(Node(35, -10, 37, -10))
    nodes.append(Node(36, -10, -10, -10))
    nodes.append(Node(-10, 46, 39, -10))
    nodes.append(Node(38, 47, -10, -10))

    nodes.append(Node(-10, 48, -10, 32))
    nodes.append(Node(-10, 49, 42, -10))
    nodes.append(Node(41, 50, 43, -10))
    nodes.append(Node(42, 51, 44, -10))
    nodes.append(Node(43, -10, 45, -10))
    nodes.append(Node(44, 53, 46, -10))
    nodes.append(Node(45, -10, -10, 36))
    nodes.append(Node(-10, 55, -10, 39))

    nodes.append(Node(-10, 56, -10, 40))
    nodes.append(Node(-10, -10, 50, 41))
    nodes.append(Node(49, -10, -10, 42))
    nodes.append(Node(-10, 59, -10, 43))
    nodes.append(Node(-10, -10, 53, -10))
    nodes.append(Node(52, 61, -10, 45))
    nodes.append(Node(-10, 62, -10, -10))
    nodes.append(Node(-10, 63, -10, 47))

    nodes.append(Node(-10, -10, 57, 48))
    nodes.append(Node(56, -10, 58, -10))
    nodes.append(Node(57, -10, 59, -10))
    nodes.append(Node(58, -10, 60, 51))
    nodes.append(Node(59, -10, -10, -10))
    nodes.append(Node(-10, -10, -10, 53))
    nodes.append(Node(-10, -10, 63, 54))
    nodes.append(Node(62, -10, -10, 55))
    return nodes

def findDirections(dir,algo):
    final_direction = []
    nodes = createMap()
    for i in range(0, len(dir)-1):
        el = nodes[int(dir[i])]
        next = int(dir[i+1])
        if el.u == next:
            final_direction.append('up')
        elif el.r == next:
            final_direction.append('right')
        elif el.d == next:
            final_direction.append('down')
        elif el.l == next:
            final_direction.append('left')
        else:
            # print("No adj ",int(dir[i]),int(dir[i+1]))
            p = elsePath(int(dir[i]),int(dir[i+1]), algo)
            final_direction = final_direction + p

    return final_direction

def elsePath(s,e,algo):
    path = []
    if algo=='bfs':
        path, explored_ucs = list(
            graph_and_searchAlgorithms.bfs(graph_and_searchAlgorithms.create_ghraph_for_map(), str(s), str(e)))
    if algo=='dfs':
        path, explored_ucs = list(graph_and_searchAlgorithms.dfs(graph_and_searchAlgorithms.create_ghraph_for_map(), str(s), str(e)))
    if algo=='ucs':
        path, explored_ucs = list(
            graph_and_searchAlgorithms.ucs(graph_and_searchAlgorithms.create_ghraph_for_map(), str(s), str(e)))
    if algo=='astar':
        path, explored_ucs = list(
            graph_and_searchAlgorithms.astar(graph_and_searchAlgorithms.create_ghraph_for_map(), str(s), str(e)))
    p = findDirections2(path)
    return p

def findDirections2(dir):
    path = []
    nodes = createMap()
    for i in range(0, len(dir)-1):
        el = nodes[int(dir[i])]
        next = int(dir[i+1])
        if el.u == next:
            path.append('up')
        elif el.r == next:
            path.append('right')
        elif el.d == next:
            path.append('down')
        elif el.l == next:
            path.append('left')
    return path

# def findDir2(dir):
#     path = []
#     nodes = createMap()
#     for i in range(0, len(dir)-1):
#         el = nodes[int(dir[i])]
#         next = int(dir[i+1])
#         if el.u == next:
#             path.append('up')
#         elif el.r == next:
#             path.append('right')
#         elif el.d == next:
#             path.append('down')
#         elif el.l == next:
#             path.append('left')
#         else:
#             print("return")
#             print(i)
#             x = i
#             for j in reversed(range(0,x+1)):
#                 print("j:",j)
#                 el2 = nodes[int(dir[j])]
#                 next2 = int(dir[j - 1])
#                 if next == el2.u or next == el2.r or next == el2.d or next == el2.l:
#                     print("to prev")
#                     if el2.u == next:
#                         path.append('up')
#                     elif el2.r == next:
#                         path.append('right')
#                     elif el2.d == next:
#                         path.append('down')
#                     elif el2.l == next:
#                         path.append('left')
#                     print(path)
#                     break
#
#                 else:
#                     print("to node",next2)
#                     print("current:",el2.r)
#                     print("next:",next2)
#
#                     if el2.u == next2:
#                         path.append('up')
#                         print("raft")
#                     elif el2.r == next2:
#                         path.append('right')
#                         print("raft")
#                     elif el2.d == next2:
#                         path.append('down')
#                         print("raft")
#                     elif el2.l == next2:
#                         path.append('left')
#                         print("raft")
#                     else:
#                         print("return")
#                         print(i)
#                         x1 = j-1
#                         for k in reversed(range(0, x1 + 1)):
#                             print("K:", k)
#                             el3 = nodes[int(dir[k])]
#                             next3 = int(dir[k - 1])
#                             if next2 == el3.u or next2 == el3.r or next2 == el3.d or next2 == el3.l:
#                                 print("to prev")
#                                 if el3.u == next2:
#                                     path.append('up')
#                                 elif el3.r == next2:
#                                     path.append('right')
#                                 elif el3.d == next:
#                                     path.append('down')
#                                 elif el3.l == next2:
#                                     path.append('left')
#                                 print(path)
#                                 break
#
#                             else:
#                                 print("to node", next2)
#                                 print("current:", el2.r)
#                                 print("next:", next2)
#
#                                 if el3.u == next3:
#                                     path.append('up')
#                                     print("raft")
#                                 elif el3.r == next3:
#                                     path.append('right')
#                                     print("raft")
#                                 elif el3.d == next3:
#                                     path.append('down')
#                                     print("raft")
#                                 elif el3.l == next3:
#                                     path.append('left')
#                                     print("raft")
#
#     print(path)
#     return path




