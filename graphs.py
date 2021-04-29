# Implements the graph as a map of (vertex,edge-map) pairs. Includes Dijkstra's algorithm on simple weighted graphs
# Louis Sullivan 119363083


from apq import *


class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, element):
        """ Create a vertex, with a data element.

        Args:
            element - the data or label to be associated with the vertex
        """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element


class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """

    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with a data element.

        Element can be an arbitrarily complex structure.

        Args:
            element - the data or label to be associated with the edge.
        """
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge.

        Args:
            v - a vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element


class Graph:
    """ Represent a simple graph.

    This version maintains only undirected graphs, and assumes no
    self loops.

    Implements the Adjacency Map style. Also maintains a top level
    dictionary of vertices.
    """

    # Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the sets of edges for the corresponding vertex.
    #    Each edge set is also maintained as a dictionary,
    #    with the opposite vertex as the key and the edge object as the value.

    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    # -----------------------------------------------------------------------#

    # ADT methods to query the graph

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])  # the dict of edges for v
        return num // 2  # divide by 2, since each edege appears in the
        # vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                # to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v - a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None.

        Args:
            v - a vertex object
            w - a vertex object
        """
        if (self._structure is not None
                and v in self._structure
                and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v.

        Args:
            v - a vertex object
        """
        return len(self._structure[v])

    # ----------------------------------------------------------------------#

    # ADT methods to modify the graph

    def add_vertex(self, element):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        """
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.
            
        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v - a vertex object
            w - a vertex object
            element - a label
        """
        if v not in self._structure or w not in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements.

        Args:
            elist - a list of pairs of vertex objects
        """
        for (v, w) in elist:
            self.add_edge(v, w, None)

    # ---------------------------------------------------------------------#

    # Additional methods to explore the graph

    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv

    # End of class definition

    # Search Methods:

    def depthfirstsearch(self, val):
        """
            Return all vertices that can be reached from the given value by marking ones
            it hs already been to.

        Args:
            val - a vertex that maybe in the graph

        """
        marked = {val: None}
        self._depthfirstsearch(val, marked)
        return marked

    def _depthfirstsearch(self, val, marked):
        for edge in self.get_edges(val):
            w = edge.opposite(val)
            if w not in marked:
                marked[w] = edge
                self._depthfirstsearch(w, marked)

    def breadthfirstsearch(self, val):
        """
            Returns all vertices that can be reached from the given value by first going to
            vertices one hop away and then to two hops, etc.

            Args:
            val - a vertex that maybe in the graph

        """
        queue = [val]
        marked = {val: None}

        while queue:  # Creating loop to visit each node
            head = queue.pop(0)
            for edge in self.get_edges(head):
                w = edge.opposite(head)
                if w not in marked:
                    marked[w] = edge
                    queue.append(w)
        return marked

    def dijkstra(self, s):
        # open starts as an empty APQ
        open = AdaptablePriorityQueue()
        # empty dict keys are vertices, values are location in open)
        locs = {}
        # empty dict
        closed = {}
        # dict where are source is key and none is value
        preds = {s: None}
        # add s to open with key 0 and add s and the element return to the addition dict locs
        locs[s] = open.add(0, s)
        # while open is not empty
        while not open.isEmpty():
            # remove min element v and its cost from open
            key, v = open.remove_min()
            # remove v from locs
            locs.pop(v)
            # remove v from preds and add v, the returned value from preds is added to closed
            closed[v] = (key, preds.pop(v))
            # for each edge e in v
            for e in self.get_edges(v):
                # get the edge opposite v and set it to w
                w = e.opposite(v)
                # while w is not in the closed dict
                if w not in closed:
                    # set newcost to v's keus plus e's cost
                    newcost = key + e.element()
                    # if w not in the dict locs
                    if w not in locs:
                        # add w:v to preds
                        preds[w] = v
                        # add newcost, w to open
                        p = open.add(newcost, w)
                        # add w:(elt returned from open) to locs
                        locs[w] = p
                    # else if newcost is better than w's oldcost
                    elif newcost < open.get_key(locs[w]):
                        # update w:v in preds
                        preds[w] = v
                        # update w's cost in open to newcost
                        open.update_key(locs[w], newcost)
        return closed


# ---------------------------------------------------------------------------#

def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline()  # either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline()  # either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length)
        file.readline()  # read the one-way data
        entry = file.readline()  # either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph


def main():
    # reads in graph file
    firstg = graphreader("simplegraph1.txt")
    # sets source vertex
    s = firstg.get_vertex_by_label(1)
    # returns dict of shortest path
    items = firstg.dijkstra(s)
    print("Vertex\tLength\tPreceding Vertex")
    # prints readable version of path
    for key, val in items.items():
        print(key, "\t\t", val[0], "\t\t", val[1])


# uncomment to run simple graphs
# if __name__ == '__main__':
#     main()
