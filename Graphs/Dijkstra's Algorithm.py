import math

def dijkstra_algorithm(start_node,end_node,graph_obj):

    '''
    Takes a dictionary object with a list of node:{neighbors} key:value pairs,
    along with a start node and end node, and returns a shortest path
    between them, if one exists

    Example input: 'c','b',{'a':{'b','c','d'},'b':{'a','d'},'c':{'a'},'d':{'a','b'}}
    Example output: ['c', 'a', 'b']
    '''

    # set up unpopulated dictionaries
    unvisited_nodes = dict()
    node_dict = dict()

    # populate dictionaries with nodes and values
    # node_dict has two values: a distance from start, initialized as inf,
    # and the previous node in the path, initialized as None
    # unvisited_nodes only contains the distance
    for node in graph_obj.keys():

        unvisited_nodes[node] = math.inf
        node_dict[node] = [math.inf,None]

    # set the distance for the starting node as 0
    node_dict[start_node][0] = 0
    unvisited_nodes[start_node] = 0

    # set the start node as current
    current_node = start_node

    # initialize loop
    while len(unvisited_nodes)>0:

        # check if the distance for the current node is inf
        if unvisited_nodes[current_node] == math.inf:
            return []

        # check if the path is complete
        # if so, construct the path using reverse iteration, and return
        if current_node == end_node:
            path = []
            u = end_node
            if node_dict[u][1] is not None or u == start_node:
                while u is not None:
                    path = [u] + path
                    u = node_dict[u][1]
        
            return path

        # iterate through the neighbors of the current node
        for neighbor in graph_obj[current_node]:
            # skip over any visited neighbors
            if neighbor not in unvisited_nodes:
                pass
            else:
                # calculate the distance from the current node to the neighbor
                alt_path = node_dict[current_node][0] + 1
                # if the new distance is less than the initial distance,
                # replace it in the dictionary values
                if alt_path < node_dict[neighbor][0]:
                    node_dict[neighbor][0] = alt_path
                    unvisited_nodes[neighbor] = alt_path
                    # assign the current node as the neighbor's previous node
                    node_dict[neighbor][1] = current_node
        # remove the current node from the unvisited dictionary                    
        del unvisited_nodes[current_node]
        # set the current node as the unvisited node with the shortest distance
        current_node = min(unvisited_nodes, key=unvisited_nodes.get)

# tests

assert(dijkstra_algorithm('c','b',{'a':{'b','c','d'},'b':{'a','d'},'c':{'a'},'d':{'a','b'}})) == ['c', 'a', 'b']
assert(dijkstra_algorithm('c','i',{'a':{'b','c','d'},'b':{'a','d'},'c':{'a'},'d':{'a','b'},'i':{'j'},'j':{'i'}})) == []

# these should run without error
