file = 'lambda-NFA.in'

# Get input data out of file
with open(file, 'rt') as f:
    content = f.readlines()
    content = [line.strip('\n') for line in content]
    content = [line.split(' ') for line in content]
    # print(content)

    num_of_nodes = int(content[0][0])
    num_of_transitions = int(content[0][1])

    # keys are STATES, values are dictionaries of {connection_to : letter}
    automata = {int(x): {} for x in range(num_of_nodes)}

    # create the GRAPH with the connections
    for i in range(1, num_of_transitions+1):
        first = int(content[i][0])
        second = int(content[i][1])
        transition = content[i][2]
        automata[first].update({second: transition})

    # get the START state
    start = int(content[num_of_transitions + 1][0])

    # get the END states as a list
    end = []
    for i in range(int(content[num_of_transitions + 2][0])):
        end.append(int(content[num_of_transitions + 2][i+1]))

    # get numbers of tests from INPUT
    num_of_tests = int(content[num_of_transitions + 3][0])

    # get WORDS which will be tested from INPUT
    words = content[len(content) - num_of_tests: len(content)]
    words = [word[0] for word in words]

    print(automata, "\nSTART:", start, "END:", end, sep='\n')
    print()

# define Automata class
class Automata:
    # it will be initialized using the GRAPH constructed before
    def __init__(self, graph):
        self.graph = graph
        self.nodes = {key: '' for key in self.graph.keys()}
        self.num_nodes = int(content[0][0])

    # set START state
    def set_start_node(self, node):
        self.nodes[node].set_start(node)

    # set END states
    def set_end_node(self, node):
        self.nodes[node].set_end(node)

    # returns the states of all NODES as a dictionary {NODE: state} (state will be '' if START/END have not been set)
    def get_node_state(self, node):
        return self.nodes[node]

    # adds a NODE to the GRAPH
    def add_node(self, node):
        self.num_nodes += 1
        self.graph.update({node: {}})
        self.nodes[node] = ''

    # removes a NODE from the GRAPH
    def remove_node(self, node):
        del self.graph[node]
        self.num_nodes -= 1

    # adds a connection between 2 adjacent nodes and assigns a weight to it
    def add_connection(self, node, neighbour, weight):
        self.num_nodes += 1
        self.nodes[node] = ''
        self.graph[neighbour] = {}
        self.graph[int(node)].update({int(neighbour): weight})
        self.nodes[neighbour] = ''

    # returns the
    def get_connections(self, node):
        if node in self.graph.keys():
            return self.graph[node]
        else:
            return None

    # returns the ADJACENT NODE which is connected to the PARENT node by specified WEIGHT
    # (none if node does not exist, or there is no connection)
    def connected_by_weight(self, node, weight):
        if node in self.graph.keys():
            for neighbour, w in self.graph[node].items():
                if weight == self.graph[node][neighbour]:
                    return neighbour
        return None

    # REMOVES CONNECTION between 2 NODES
    def remove_connection(self, node, neighbour):
        del self.graph[node][neighbour]

    # returns the WEIGHT which connects 2 nodes
    def get_weight(self, node, neighbour):
        return self.graph[node][neighbour]

    # sets START STATE
    def set_start(self, start_node):
        self.nodes[start_node] = 'start'

    # sets END STATE
    def set_end(self, end_node):
        self.nodes[end_node] = 'end'

    # verifies of node is START STATE
    def is_start(self, node):
        return True if self.nodes[node] == 'start' else False

    # verifies of node is END STATE
    def is_end(self, node):
        return True if self.nodes[node] == 'end' else False


# initialize the l-NFA graph using the input data
l_NFA = Automata(automata)

# set START state
l_NFA.set_start(start)

# set END states
for i in end:
    l_NFA.set_end(i)


''' The method will verify if there is a path from the NODE to the adjacent node
using a connection which has the WEIGHT equal to the first LETTER of the WORD or equal to "#".
If there is such a path, we remove the first letter of the word and perform a check from the current node
using the remaining letters in the word.
The search is finished when WORD = ''.
If the l_NFA.is_end(next) is TRUE 
(which means there is a path form the current node to the END state using the last letter of the word),
the word will be ACCEPTED, otherwise it will NOT BE ACCEPTED
'''

# CHECK method to verify if word is ACCEPTED / NOT ACCEPTED by l-NFA
def check_L_NFA(node, word):
    global path                                         # stores the PATH used to verify the word
    path.append(node)                                   # add the start node and next nodes
    letter = word[0]
    if letter in l_NFA.get_connections(node).values():  # if the first letter of the word
        next = l_NFA.connected_by_weight(node, letter)
        word = word[1:]
        if len(word) == 0:
            if l_NFA.is_end(next):
                path.append(next)
                print("DA")
                print('Traseu:', *path, '\n')
            else:
                print("NU", '\n')
        else:
            check_L_NFA(next, word)
    elif "#" in l_NFA.get_connections(node).values():
        next = l_NFA.connected_by_weight(node, '#')
        if len(word) == 0:
            if l_NFA.is_end(next):
                path.append(next)
                print("DA")
                print('Traseu:', *path, '\n')
            else:
                print("NU", '\n')
        else:
            check_L_NFA(next, word)
    else:
        print("NU", '\n')


print("SOLUTII")
# Check the words in the test sample
for word in words:
    path = []
    print(f'Cuvantul: {word}')
    check_L_NFA(0, word)











