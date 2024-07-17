import pickle
import fitz
import time
from additional_structures.graph import Graph
from additional_structures.trie import Trie


def load_pdf_to_graph(pdf_path):
    document = fitz.open(pdf_path)
    graph = Graph()

    for page_num in range(len(document)):
        graph.insert_vertex(page_num + 1)

    return graph, document

def create_trie_for_page(page_text):
    words = page_text.split()
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie

# Serialize the graph and document
def serialize_graph(graph, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(graph, file)

# Deserialize the graph and document
def deserialize_graph(file_name):
    with open(file_name, 'rb') as file:
        graph = pickle.load(file)
    return graph

# Example usage
"""pdf_path = './Data_Structures_and_Algorithms_Using_Python.pdf'
graph, document = load_pdf_to_graph(pdf_path)

# Create a trie for each page and store it in the graph
for page_num in range(len(document)):
    page = document.load_page(page_num)
    text = page.get_text("text")
    trie = create_trie_for_page(text)
    vertex = next(v for v in graph.vertices() if v.element() == page_num)
    vertex.trie = trie  # Add trie to vertex
    vertex.content = text  # Add text content to vertex

# Serialize the graph
serialize_graph(graph, 'pdf_graph.pkl')
"""






def data_init():
    graph, document = load_pdf_to_graph('./Data_Structures_and_Algorithms_Using_Python.pdf')
    

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")
        trie = create_trie_for_page(text.lower())
        vertex = graph.get_v_bynum(page_num + 1)
        vertex.trie = trie
        vertex.content = text
    
    graph.populate_links()
    serialize_graph(graph, 'pdf_graph.pkl')



# Deserialize the graph
def data_preload():
    start = time.time()
    deserialized_graph = deserialize_graph('pdf_graph.pkl')
    end = time.time()
    print(end-start)

    

    return deserialized_graph