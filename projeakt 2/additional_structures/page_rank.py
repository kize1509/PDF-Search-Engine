import numpy as np
from additional_structures.algorithms import Algorithms

class PageRank:
    def __init__(self, graph, damping_factor=0.85, max_iterations=100, tol=1.0e-6):
        self.graph = graph.body  # Adjacency list representation of the graph
        self.damping_factor = damping_factor
        self.max_iterations = max_iterations
        self.tol = tol
        self.num_pages = graph.length
        self.ranks = np.ones(self.num_pages) / self.num_pages
        self.algs = Algorithms()

    def rank(self, term=None, query=False, tokens=None):
        freq_res = []
        
        
        if query:
            freq_res = [page.complex_frequency(tokens) for page in self.graph.values()]
        else:
            freq_res = [page.term_frequency(term) for page in self.graph.values()]
        
        if term:
            term_frequencies = []
            for res in freq_res:
                sum = 0
                for single in term:
                    if single in res.keys():
                        sum += res[single][1]
                term_frequencies.append(sum)
            term_frequencies = np.array(term_frequencies)
            max_freq = term_frequencies.max() if term_frequencies.max() > 0 else 1
            term_frequencies = term_frequencies / max_freq
        else:
            term_frequencies = np.ones(self.num_pages)

        for iteration in range(self.max_iterations):
            new_ranks = np.zeros(self.num_pages)
            i = 0
            for page in self.graph.values():
                rank_sum = 0
                for in_link in page.in_links:
                    rank_sum += self.ranks[in_link] / len(self.graph[in_link].out_links)
                new_ranks[i] = (1 - self.damping_factor) / self.num_pages + self.damping_factor * rank_sum
                i += 1
            new_ranks = new_ranks * term_frequencies  # Incorporate term frequency

            if np.linalg.norm(new_ranks - self.ranks, ord=1) < self.tol:
                break

            self.ranks = new_ranks
            
        ret_lits = []
        for page in self.graph.values():
            if self.ranks[page.element()-1] == 0:
                continue


            new_el = {}
            new_el['RANK'] = self.ranks[page.element()-1]
            new_el['CONTENT'] = page.content

            for single in term:

                new_el[single] = freq_res[page.element()-1][single]

            new_el['NUMBER'] = page.element()
            



            ret_lits.append(new_el)
        self.algs.quickSort(ret_lits, 0, len(ret_lits)-1)
        return ret_lits
    


    def sorted_ranks(self, term):
        ranks = self.rank(term)
        if len(term) == 1:
            if len(ranks) == 0:
                print('\n')
                print("No results found.")
                suggested = self.suggest_term(term[0])
                return suggested, False

        for i in range(len(ranks)):
            self.graph[i+1].rank = ranks[i]
        return ranks, True
    


    def complex_query(self, query):

        tokens = self.algs.tokenize(query)
        postfix_tokens = self.algs.infix_to_postfix(tokens)

        for_processing = []
        for token in postfix_tokens:
            if token in ['AND', 'OR', 'NOT']:
                continue
            for_processing.append(token)
        
        print("FOR PROCESSING: ", postfix_tokens)
        res = self.rank(for_processing, True, postfix_tokens)

        return res, for_processing
    
    def suggest_term(self, term):

        posibilities = {}
        for page in self.graph.values():
            for word in page.content.split(" "):
                if word[-1:] == '.' or word[-1:] == ',' or word[-1:] == ';' or word[-1:] == ':':
                    word = word[:-1]
               
                similarity = self.jaccard_similarity(term.lower(), word.lower())
                posibilities[word] = similarity
        
        
        posibilities = sorted(posibilities.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)
        
        print("Did you mean:")
        
        possible = []
        j = 0
        for i in range(len(posibilities)):
            word = posibilities[i][0]
            print( f"{i+1}.", word)
            possible.append(i+1)
            j += 1
            if j == 3:
                break   
        print("\n")
        i = eval(input("Enter the number of the word you meant: "))
        while i not in possible:
            print("Invalid input. Please enter a number from the list.")
            i = eval(input("Enter the number of the word you meant: "))
        print("\n")
        return posibilities[i-1][0]


    def jaccard_similarity(self, word1, word2):
        set1 = set(word1)
        set2 = set(word2)

        intersection = set1.intersection(set2)
        union = set1.union(set2)

        if not union:
            return 0.0  # To handle the case when both sets are empty

        return len(intersection) / len(union)


    def autocomplete(self, search_query):

        words = []

        for page in self.graph.values():
            content = page.content.split(" ")
            for word in content:
                if word[-1:] == '.' or word[-1:] == ',' or word[-1:] == ';' or word[-1:] == ':' or word[-1:] == '!' or word[-1:] == '?' or word[-1:] == ')' or word[-1:] == ']' or word[-1:] == '}' or word[-1:] == '"' or word[-1:] == "'":
                    word = word[:-1]
                if word.startswith(search_query):
                    if word not in words:
                        words.append(word)
        return words