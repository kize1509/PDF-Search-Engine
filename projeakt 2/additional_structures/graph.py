import re
from additional_structures.algorithms import Algorithms
class Graph: 
    class Vertex:
        def __init__(self, x):
            self._element = x
            self.content = None
            self.out_links = []
            self.in_links = []

        def element(self):
            return self._element

        def __str__(self):
            return str(self._element)
        
        def term_frequency(self, term):
            collected = {}
        
            for single in term:
                collected[single] = ([], 0)


                if not self.content or (self.trie.search(single) == False and len(single.split(" ")) == 1) or (single not in self.content and len(single.split(" ")) > 1):
                    continue
                
                elif (self.trie.search(single) and len(single.split(" ")) == 1) or (single in self.content and len(single.split(" ")) > 1):
                    algs = Algorithms()
                    collected[single] = algs.KMPSearch(single, self.content) 
            return collected
        

        def complex_frequency(self, postfix_tokens):
            stack = []
            result = {}
            for token in postfix_tokens:
                if token not in ['AND', 'OR', 'NOT']:
                    stack.append(token)
                if token == 'NOT':
                    operand = stack.pop()
                    result[operand] = self.term_frequency([operand])[operand]
                    if len(result[operand][0]) != 0:
                        for token in postfix_tokens:
                            result[token] = ([], 0)
                        return result
                elif token in ['AND', 'OR']:
   
                    if len(stack) == 1:
                        el = stack.pop()
                        if token == 'AND':
                            result[el] = self.term_frequency([el])[el]
                            if len(result[el][0]) == 0:
                                for token in postfix_tokens:
                                    result[token] = ([], 0)
                                return result 
                        elif token == 'OR':
                            result[el] = self.term_frequency([el])[el]
                            
                    elif len(stack) != 0:
                        operand1 = stack.pop()
                        operand2 = stack.pop()
                        if token == 'AND':
                            result[operand1] = self.term_frequency([operand1])[operand1]
                            result[operand2] = self.term_frequency([operand2])[operand2]
                            if len(result[operand1][0]) == 0 or len(result[operand2][0]) == 0:
                                for token in postfix_tokens:
                                    result[token] = ([], 0)
                                return result
                            
                        elif token == 'OR':
                            result[operand1] = self.term_frequency([operand1])[operand1]
                            result[operand2] = self.term_frequency([operand2])[operand2]    
            if len(stack) == 1:
                el = stack.pop()
                result[el] = self.term_frequency([el])[el]     
            return result

        def apply_not(self, operand):    
            content = self.content
            for single in operand:
                if single in content.split(" "):
                    return 0
                    

    def __init__(self):
        self.body = {}
        self.length = 0


    def insert_vertex(self, x):
        v = self.Vertex(x)
        self.body[x] = v
        self.length += 1
        return v    
    
    def populate_links(self):
        # this regex patern is no good, it should be improved, needs to accept only the frazes like 'page X' and can hold any punctuation at the end and accepts 'pages X and Y'
        # add possible punctuation at the end of the fraze and add 'pages X and Y' to the regex
        pattern = re.compile(r'page\s(\d+)|pages\s(\d+)\sand\s(\d+)')



        for number in self.body:
            vertex = self.body[number]
            #extract all of the outgoing links from the content of the vertex
            matches = pattern.findall(vertex.content)

            out_links = []
            for match in matches:
                for num in match:
                    if num and int(num) not in out_links and num != "":
                        out_links.append(int(num)+22)
            for link in out_links:
                if int(link) in self.body:
                    vertex.out_links.append(int(link))
                    print("link: ", link, "number: ", number)
                    self.body[int(link)].in_links.append(number)

    def get_v_bynum(self, num):
        return self.body[num]