import xml.etree.ElementTree as ET
from py2neo import Graph, Node, Relationship

def make_graph(child, nodes, relationships, parent = None):
    node = None
    for subchild in child:
        tag = subchild.tag.replace('{http://uniprot.org/uniprot}', '')
        if tag != 'protein':
            node = Node(tag, **{**subchild.attrib, "text": tag,"content": subchild.text})
            nodes.append(node)

        if parent:
            rel = Relationship(parent, f'has_{tag}', node)
            relationships.append(rel)
        make_graph(subchild,nodes=nodes,relationships=relationships,parent=node)

# Define function to create a batch of nodes and relationships
def create_batch(graph, nodes, relationships):
    for node in nodes:
        graph.create(node)
    for rel in relationships:
        graph.create(rel)

# Define function to process XML file and create nodes and relationships in batches
def process_xml_file(filename, batch_size, host, port, login, password):

    graph = Graph(f'bolt://{host}:{port}', auth=(login, password))
    print("glubs 2")

    nodes = []
    relationships = []
    parent_stack = []

    print("glubs 3")

    graph.delete_all()
    print("glubs 4")
    for event, elem in ET.iterparse(filename, events=("start","end")):
        tag = elem.tag.replace('{http://uniprot.org/uniprot}','')
        if tag  == "protein":
            node = Node(tag, **{**elem.attrib, "text": tag,"content": elem.text})
            parent_stack.append(node)
            break
    print("glubs 5")
    # Iterate through the XML file in chunks using iterparse
    entry = None
    for event, elem in ET.iterparse(filename, events=("start","end")):
        if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "start":
            entry = True
            continue
        elif elem.tag == "{http://uniprot.org/uniprot}entry" and event == "end":
            entry = False
            continue
        if entry:   
            tag = elem.tag.replace('{http://uniprot.org/uniprot}','')
            if event == 'start' and tag != 'protein':
                node = Node(tag, **{**elem.attrib, "text": tag,"content": elem.text})
                nodes.append(node)
                parent_stack.append(node)
            elif event == 'end' and tag != 'protein':
                node = parent_stack.pop()
                rel = Relationship(parent_stack[-1], f'has_{tag}', node)
                relationships.append(rel)
        
    create_batch(graph, nodes, relationships)
