# Class that implements route finding in road maps of cork city
# Louis Sullivan 119363083

from graphs import Vertex
from graphs import Graph


class RouteMap(Graph):
    def __init__(self):
        super().__init__()
        # dict that has element as key and value as vertex pointer
        self._faststruct = dict()
        # dict where key is the element and value is lat, long of that element
        self._coords = dict()

    def __str__(self):
        """
        Return a visual of the graph if it has less than 100 vertices/edges
        """
        if self.num_vertices() < 100 and self.num_edges() < 100:
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
        else:
            return "The graph is too large to print."

    def add_vertex(self, element):
        """
        Add a element to dictionary with the vertex as a value

        @return: the element vertex
        """
        v = Vertex(element)
        # element is key and value is the vertex object of that key
        self._faststruct[element] = v
        self._structure[v] = dict()
        return v

    def get_vertex_by_label(self, element):
        """ Return the element from our dictionary """
        return self._faststruct[element]

    def add_coords(self, element, lat, longi):
        """
        A coordinates dictionary where key is the vertex and key is the latitude,
        longitude of that vertex

        @return: the element vertex

        """
        v = self.get_vertex_by_label(element)
        self._coords[v] = (lat, longi)
        return v

    def get_coords(self, element):
        """
        Get the coordinates of the given element

        @return: the coords or None
        """
        for key, v in self._coords.items():
            if key == element:
                return v[0], v[1]
        return None

    def sp(self, v, w):
        """
        Call the implementation of Dijkstra's method for source v
            and receive the table structure in return

        @return: list of vertices and their costs
        """
        verlist = []
        # table is set table structure returned from Dijkstra on source v
        table = self.dijkstra(v)
        # set destination as currentval
        currentval = w
        # while we are not at the end
        while currentval is not None:
            # get the tuple of the current value
            currentup = table[currentval]
            # append that tuple
            verlist.append(currentup)
            # set the new val to our predecessor
            currentval = currentup[1]
        # delete the none value at the end
        del verlist[-1]
        # reverse the list so source is at the top
        return verlist[::-1]


# -----------------------------------------------

def graphreader(filename):
    """ Read and return the route map in variable. """
    graph = RouteMap()
    file = open(filename, 'r')
    entry = file.readline()
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        # take in gps line
        gps = file.readline().split()
        # set latitude and longitude
        lat = float(gps[1])
        longi = float(gps[2])
        # add coords to dict
        coords = graph.add_coords(nodeid, lat, longi)
        entry = file.readline()
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        # length can be used later
        length = float(file.readline().split()[1])
        # takes in time
        time = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, time)
        # read one way data
        file.readline()
        entry = file.readline()
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph


def main():
    # uncomment this if you want to run the simple route
    # routemap = graphreader('simpleroute.txt')
    # source = routemap.get_vertex_by_label(1)
    # dest = routemap.get_vertex_by_label(4)
    # read in data for cork city
    routemap = graphreader('corkCityData.txt')
    ids = {'wgb': 1669466540, 'turnerscross': 348809726, 'neptune': 1147697924, 'cuh': 860206013, 'oldoak': 358357,
           'gaol': 3777201945, 'mahonpoint': 330068634}
    sourcestr = 'wgb'
    deststr = 'neptune'
    source = routemap.get_vertex_by_label(ids[sourcestr])
    dest = routemap.get_vertex_by_label(ids[deststr])
    tree = routemap.sp(source, dest)
    print("type\tlatitude\tlongitude\telement\tcost")
    for val in tree:
        coords = routemap.get_coords(val[1])
        print("W", "\t", coords[0], "\t", coords[1], "\t", val[1], "\t", val[0])


if __name__ == '__main__':
    main()
