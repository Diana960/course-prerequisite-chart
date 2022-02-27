import networkx as nx
from pyvis.network import Network
from typing import List

class Node:
    def __init__(self, node_name, color_label):
        self.node_name = node_name
        self.color_label = color_label
        
    def __str__(self):
        return f"Name: {self.node_name}, ColorLabel: {self.color_label}"
        
class Edge:
    def __init__(self, name=None, color_label=None):
        self.name = name
        self.color_label = color_label
        
    def __str__(self):
        return f"Name: {self.name}, ColorLabel: {self.color_label}"

class GraphVisualization:
    def __init__(self, edge_colors = dict(), node_colors = dict(), node_name_to_node_dict = dict()):
        self.graph_edges = []
        self.graph_nodes = []
        self.edge_colors = edge_colors
        self.node_colors = node_colors
        self.node_name_to_node_dict = node_name_to_node_dict
        
    def addEdge(self, first_node: Node, second_node: Node, edge: Edge = None):       
        if (edge == None):
            temp = {"node1": first_node, "node2": second_node}
        else:
            temp = {"node1": first_node, "node2": second_node, "edge": edge}
        
        self.graph_edges.append(temp)

    def addCourseRequisites(self, course: str, prereqs: List[str], coreqs: List[str]):
        course_node = self.node_name_to_node_dict[course]
        self.graph_nodes.append(course_node)
        for p in prereqs:
            self.addEdge(self.node_name_to_node_dict[p],
                      course_node,
                      Edge(color_label="prerequisite")) # prerequisitves
        for c in coreqs:
            self.addEdge(self.node_name_to_node_dict[c],
                      course_node,
                      Edge(color_label="corequisite")) # corequisitives (need to make line dotted)
        
    def visualize_pyvis(self, title):      
        net = Network(notebook=True, directed=True, layout=False)
        for n in self.graph_nodes:
            net.add_node(n.node_name, color=self.node_colors[n.color_label])
        for e in self.graph_edges:
            net.add_node(e['node1'].node_name, color=self.node_colors[e['node1'].color_label])
            net.add_node(e['node2'].node_name, color=self.node_colors[e['node2'].color_label])                
                
            if ('edge' not in e or e['edge'].color_label == None):
                net.add_edge(e['node1'].node_name, e['node2'].node_name)
            else:
                net.add_edge(e['node1'].node_name, e['node2'].node_name, color=self.edge_colors[e['edge'].color_label])
        
        net.width = '1000px'
        net.height = '1000px'
        net.toggle_physics(False)
        return net.show(f"pyvis_visuals/{title}.html")