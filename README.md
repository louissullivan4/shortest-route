# shortest-route
Algorithms and Data Structues assessment that implements AdaptablePriorityQueue ADT, Graph ADT and Dijsktras shortest path algorithm to find the shortest distance between two points in cork city.

QUESTION ASKED:

1. Dijkstra's algorithm on simple weighted graphs
Implement Dijkstra's algorithm for finding the shortest paths  from a given source vertex to all other reachable vertices in a weighted graph. You should use a graph implementation based on adjacency maps or adjacency lists, and the graph should maintain a dictionary of all vertices as its top-level structure (so for an adjacency list graph, a vertex is a key, and its value is the list of edges incident on that vertex, while for an adjacency map graph, a vertex is a key, and its value is a sub-dictionary with other vertices as keys with values the edge that connects the two vertices). You can extend you own solution to Lab03/04, or you can build on the published sample solution to Lab 03. To implement Dijkstra's algorithm, you must use an Adaptable Priority Queue to maintain the open vertices, and the APQ must be implemented using a Binary Heap. You have to implement that yourself, and cannot use any python library implementation of a heap or a priority queue. Your implementation of Dijkstra should return a dictionary where a vertex is a key, and its value is a pair consisting of the path length from the source and the preceding vertex.

 

Test your implementation on the two graphs below:

simplegraph1.txt  download, which has 5 vertices and 7 edges. The shortest path from V1 to V4 should have length 8, and the preceding vertex should be v3.

simplegraph2.txt,  downloadwhich has 28 vertices, and represents the graph from Lecture 14, with the names of the vertices changed from a,b,c ... to 1,2,3, ... The shortest path from 14 to 5 should have length 16, and the preceding vertex on its path should be 8.

 

You will need to read the graphs in from the textfiles. You can write the code to read the textfiles yourself, or you can use the method supplied in graphreader.txt  download. This method assumes you have an implementation of the Graph ADT with the same method signatures as given in the solutions to previous labs. You will need to find the internal reference to a vertex - you can write your own method, or you can use the get_vertex_by_label() method from the Lab 03 solution. You will also need to print out the shortest path results in some sensible format - the simplest thing to do is print out every vertex followed by two pieces of data: the cost of the shortest path to this vertex from the source, and preceding vertex in that path.

 

2. Extending Dijkstra to route finding in road maps
 

Adapt your code from part (i) to handle weighted graphs which represent road maps. Create a new class called RouteMap - you can either inherit from Graph or copy-and-paste your Graph implementation into a new class which you can then modify.  For now, you only need to handle undirected graphs.

Each vertex, which will represent a junction, will be associated with a pair of (latitude,longitude) coordinates, which will be floating point numbers with 6 decimal places. You should maintain a new datastructure in your class to associate each vertex with a pair of coordinate values, which should be floats.

The value for each edge represents the expected time to cross the edge while driving in a car in normal traffic conditions. Note that there are two values in the text file -- one for 'length' and one for 'time'. It is the time we are interested in for this exercise.  You can discard the length, or store it in some other structure for later use.

The graphs to be processed could be large, so you will need to pay attention to the efficiency of your methods. First of all, place a test in your RouteMap.__str__(self) method so that you only represent all the vertices and edges in the output string if the number of vertices and the number of edges is less than 100. Secondly, the method for getting a vertex by its label in the lab 03 solution uses a simple linear search, which will be too slow if we are creating a graph with 1000s of vertices. Instead, add a new dictionary to your class in which the keys are the elements and the values are references to the vertex objects, and use that dictionary to find a vertex by label (so we have one dictionary indexed by object reference pointing to elements, and another dictionary indexed by element pointing to object references). Modify your add_vertex(...) method so that it adds the correct entries into both dictionaries.

Modify the method to read graphs from file to handle the new format, which can be seen in simpleroute.txt  download. For now, read in but discard the line which describes the one-way status of the edges.

Your implementation of Dijkstra's algorithm from part (i) should now work without modification.

Write a new method sp(self,v,w) for the class which will call your implementation of Dijkstra's method for source v and receive the table structure in return (this should tell us, for each vertex, what the cost of the path from v was, and what the preceding vertex was on that path. From this structure, your method should create a list of the vertices and their costs in the path from v to w. Build the list by traversing backwards from the entry for w, appending each vertex, until you reach v. Then reverse the list.

 

Write a method to print out the path, one vertex per line. The output should start with the line of (tab-separated) text

        type  latitude  longitude  element cost

and then each line should be in the format (tab-separated)

        W  51.893785  -8.499404  1669466540 27.5

 where the numbers are replaced by the two parts of the coordinate pair for the vertex, followed by the vertex element, and then its cost. The first character should always be W.

 

Once you have tested that your implementation works on simpleroute.txt, try it on corkCityData.txt  download  which is a processed file of the road network, cycle paths and pedestrian ways of Cork City and the surrounding area, extracted from OpenStreetMaps. You should get 56641 vertices and 59378 edges. Note that most of these vertices have degree 2 and so do not offer any choice in path planning - they are there so that the routes can be displayed easily on a map. (and there are 48 vertices with degree 0, and approximately 5000 with degree 1 that represent dead-ends in the road network). If your graph does not appear to load while Python continues to run, then either (i) you have an error in your code that is sending it into an infinite loop, or (ii) you have used inefficient data structures and algorithms, and it is simply taking a very long time to build the initial graph.

Some specific places include:

Western Gateway: 1669466540
Turner's Cross: 348809726
Neptune stadium: 1147697924
Cork University Hospital: 860206013
The Old Oak: 358357
The City Gaol: 3777201945
Mahon Point: 330068634
To visualise your path, you can copy and paste the entire output (including the first line of tab-separated text) into the GPS Visualizer (Links to an external site.)  text box. Before clicking 'Draw map', you should select 'Leaflet' from the Format dropdown menu on the left under General Map Parameters (because using the default Google setting give nag messages about the Maps API key)

Test your implementation on shortest paths from:

Western Gateway to Neptune Stadium
The Old Oak to Cork University Hospital 
Cork City Gaol to Mahon Point 
 

My test routines look something like the following:

routemap = RouteMap('corkCityData.txt')

ids = {}

ids['wgb'] = 1669466540

ids['turnerscross'] = 348809726

ids['neptune'] = 1147697924

ids['cuh'] = 860206013

ids['oldoak'] = 358357

ids['gaol'] = 3777201945

ids['mahonpoint'] = 330068634

sourcestr = 'wgb'

deststr='neptune'

source = routemap.get_vertex_by_label(ids[sourcestr])

dest = routemap.get_vertex_by_label(ids[deststr])

tree = routemap.sp(source,dest)

routemap.printvlist(tree)

(with additional locations and routes).

 

The output I get on GPSVisualiser for that test is shown in sample output showing route from WGB to Neptune  download  . Note that the path is generated from an undirected graph, and so the route might not be legal.
