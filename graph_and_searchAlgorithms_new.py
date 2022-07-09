import sys
from queue import PriorityQueue
graph = {}
def create_ghraph_for_map():
    add_node_to_graph('0', ['8', '1'])
    add_node_to_graph('1', ['0', '2'])
    add_node_to_graph('2', ['10', '1'])
    add_node_to_graph('3', ['11', '4'])
    add_node_to_graph('4', ['3', '5'])
    add_node_to_graph('5', ['4', '6'])
    add_node_to_graph('6', ['5'])
    add_node_to_graph('7', ['15'])
    add_node_to_graph('8', ['0', '16', '9'])
    add_node_to_graph('9', ['8'])
    add_node_to_graph('10', ['2', '18'])
    add_node_to_graph('11', ['3', '19'])
    add_node_to_graph('12', ['13'])
    add_node_to_graph('13', ['12', '14', '21'])

    add_node_to_graph('14', ['13', '15'])
    add_node_to_graph('15', ['7', '14', '23'])
    add_node_to_graph('16', ['8', '17', '24'])
    add_node_to_graph('17', ['16'])
    add_node_to_graph('18', ['10', '19'])
    add_node_to_graph('19', ['11', '20', '18'])
    add_node_to_graph('20', ['19', '28'])
    add_node_to_graph('21', ['13', '22'])
    add_node_to_graph('22', ['21'])
    add_node_to_graph('23', ['15', '31'])
    add_node_to_graph('24', ['16', '25'])
    add_node_to_graph('25', ['24', '26'])
    add_node_to_graph('26', ['25', '27'])
    add_node_to_graph('27', ['26', '35'])
    add_node_to_graph('28', ['20', '29'])
    add_node_to_graph('29', ['28', '30'])
    add_node_to_graph('30', ['29', '31'])
    add_node_to_graph('31', ['30', '23'])
    add_node_to_graph('32', ['40', '33'])
    add_node_to_graph('33', ['32', '34'])
    add_node_to_graph('34', ['33', '35'])
    add_node_to_graph('35', ['27', '34', '36'])
    add_node_to_graph('36', ['35', '37'])
    add_node_to_graph('37', ['36'])

    add_node_to_graph('38', ['46', '39'])
    add_node_to_graph('39', ['38', '47'])
    add_node_to_graph('40', ['32', '48'])
    add_node_to_graph('41', ['49', '42'])
    add_node_to_graph('42', ['41', '50', '43'])
    add_node_to_graph('43', ['42', '51', '44'])
    add_node_to_graph('44', ['43', '45'])
    add_node_to_graph('45', ['44', '46', '53'])
    add_node_to_graph('46', ['45', '38'])
    add_node_to_graph('47', ['39', '55'])
    add_node_to_graph('48', ['40', '56'])
    add_node_to_graph('49', ['41', '50'])
    add_node_to_graph('50', ['49', '42'])
    add_node_to_graph('51', ['43', '59'])
    add_node_to_graph('52', ['53'])
    add_node_to_graph('53', ['61', '52', '45'])
    add_node_to_graph('54', ['62'])
    add_node_to_graph('55', ['47', '63'])
    add_node_to_graph('56', ['48', '57'])
    add_node_to_graph('57', ['56', '58'])
    add_node_to_graph('58', ['57', '59'])
    add_node_to_graph('59', ['58', '51', '60'])
    add_node_to_graph('60', ['59'])
    add_node_to_graph('61', ['53'])
    add_node_to_graph('62', ['54', '63'])
    add_node_to_graph('63', ['55', '62'])

    return graph


def add_node_to_graph(node, neighbours):
    graph_list = []
    for x in neighbours:
        if x is not None and not x == '':
            graph_list.append(str(x))
    graph[str(node)] = graph_list

def ucs(graph, start, goal):
    final_path = []
    explored_path = list()
    if start == goal:
        return final_path, explored_path
    final_path.append(start)
    path_cost = 0
    frontier = [(path_cost, final_path)]
    while len(frontier) > 0:
        g, path = pop_of_front(frontier)
        current_node = path[-1]
        explored_path.append(current_node)
        if current_node == goal:
            return path, explored_path
        n = graph[current_node]
        list_neighbors = [int(n) for n in n]
        list_neighbors.sort(reverse=False)
        neighbours_list_str = [str(n) for n in list_neighbors]
        for neighbour in neighbours_list_str:
            path_to_neighbour = path.copy()
            path_to_neighbour.append(neighbour)
            extra_cost = 1
            neighbour_cost = extra_cost + g
            new_element = (neighbour_cost, path_to_neighbour)
            is_there, indexx, neighbour_old_cost, _ = read_new_from_frontier(neighbour, frontier)
            if (neighbour not in explored_path) and not is_there:
                frontier.append(new_element)
            elif is_there:
                if neighbour_old_cost > neighbour_cost:
                    frontier.pop(indexx)
                    frontier.append(new_element)

    return None, None


def bfs(graph, start, goal):
    explored_path = []
    queue = [[start]]
    if start == goal:
        return "Start = goal"
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored_path:
            neighbours = graph[node]
            for neighbour in neighbours:
                final_path = list(path)
                final_path.append(neighbour)
                # print("neighbour : ", neighbour)
                queue.append(final_path)
                if neighbour == goal:
                    return final_path, explored_path
            explored_path.append(node)
    return "a connecting path doesn't exist"

def dfs(graph, start, goal):
    explored_path = []
    my_stack = [(start, [start])]
    visited_nodes = []
    while my_stack:
        (node, final_path) = my_stack.pop()
        if node not in visited_nodes:
            if node == goal:
                visited_nodes.append(node)
                return final_path, visited_nodes
            visited_nodes.append(node)
            for v in graph[node]:
                my_stack.append((v, final_path + [v]))
            explored_path.append(node)


def exist_in_frontier(node, frontier):
    for path in frontier:
        if node == path[-1]:
            return True
    return False

def read_new_from_frontier(node, frontier):
    for i in range(len(frontier)):
        current = frontier[i]
        cost, path = current
        if path[-1] == node:
            return True, i, cost, path
    return False, None, None, None


def calculate_huristic_manhattan(node, goal):
    current_cell_x, current_cell_y = divmod(int(node), 8)
    goal_x, goal_y = divmod(int(goal), 8)
    delta_x = abs(current_cell_x - goal_x)
    delta_y = abs(current_cell_y - goal_y)
    return delta_x + delta_y

def astar(graph, start, goal):
    final_path = []
    explored_nodes = list()
    if start == goal:
        return final_path, explored_nodes
    final_path.append(start)
    path_cost = calculate_huristic_manhattan(start, goal)
    frontier = [(path_cost, final_path)]
    while len(frontier) > 0:
        pathCost, path = pop_of_front(frontier)
        current_node = path[-1]
        pathCost = pathCost - calculate_huristic_manhattan(current_node, goal)
        explored_nodes.append(current_node)
        if current_node == goal:
            return path, explored_nodes
        neighbours = graph[current_node]
        node_list_integer = [int(n) for n in neighbours]
        node_list_integer.sort(reverse=False)
        str_node_list = [str(n) for n in node_list_integer]
        for node in str_node_list:
            node_path = path.copy()
            node_path.append(node)
            neighbour_cost = 1 + pathCost + calculate_huristic_manhattan(node, goal)
            node_new = (neighbour_cost, node_path)
            exist, x, neighbour_old_cost, _ = read_new_from_frontier(node, frontier)
            if (node not in explored_nodes) and not exist:
                frontier.append(node_new)
            elif exist:
                if neighbour_old_cost > neighbour_cost:
                    frontier.pop(x)
                    frontier.append(node_new)

    return None, None



def pop_of_front(frontier):
    if len(frontier) == 0:
        return None
    minimum_val = sys.maxsize
    maximums = []
    for val, path in frontier:
        if val == minimum_val:
            maximums.append(path)
        elif val < minimum_val:
            minimum_val = val
            maximums.clear()
            maximums.append(path)
    maximums = sorted(maximums, key=lambda x: x[-1])
    value = maximums[0]
    frontier.remove((minimum_val, maximums[0]))
    return minimum_val, value




if __name__ == '__main__':
    graph = create_ghraph_for_map()

    print("UCS >>>>>>>>")
    ucs_final_path, explored_path = ucs(graph, str(0), str(61))
    print("Final Path UCS:", ucs_final_path)
    print("Explored Path In UCS: ", explored_path)


    print("BFS >>>>>>>>")
    bfs_final_path, explored_path = bfs(graph, str(0), str(61))
    print("Final Path BFS:", bfs_final_path)
    print("Explored Path In BFS: ", explored_path)


    print("DFS >>>>>>>>")
    dfs_final_path, explored_path = dfs(graph, str(0), str(61))
    print("Final Path DFS:", dfs_final_path)
    print("Explored Path In DFS: ", explored_path)

    print("AStar >>>>>>>>")
    astar_final_path, explored_astar = astar(graph,  str(0), str(61))
    print("Path_astar:", astar_final_path)
    print("Explored Nodes A Star: ", explored_astar)
