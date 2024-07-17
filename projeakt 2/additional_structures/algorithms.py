
class Algorithms:

    def KMPSearch(self, pat, txt):
        M = len(pat)
        N = len(txt)
        txt = txt.lower()
        pat = pat.lower()
        # create lps[] that will hold the longest prefix suffix
        # values for pattern
        lps = [0]*M
        j = 0  # index for pat[]
    
        # Preprocess the pattern (calculate lps[] array)
        self.computeLPSArray(pat, M, lps)
    
        i = 0  # index for txt[]
        overall_counter = 0
        result = []
        while (N - i) >= (M - j):
            if pat[j] == txt[i]:
                i += 1
                j += 1
    
            if j == M:
                ind = i-j
                overall_counter += 1
                result.append(ind)
                j = lps[j-1]
    
            # mismatch after j matches
            elif i < N and pat[j] != txt[i]:
                # Do not match lps[0..lps[j-1]] characters,
                # they will match anyway
                if j != 0:
                    j = lps[j-1]
                else:
                    i += 1

        return (result, overall_counter)
    
    
    # Function to compute LPS array
    def computeLPSArray(self, pat, M, lps):
        len = 0  # length of the previous longest prefix suffix
    
        lps[0] = 0  # lps[0] is always 0
        i = 1
    
        # the loop calculates lps[i] for i = 1 to M-1
        while i < M:
            if pat[i] == pat[len]:
                len += 1
                lps[i] = len
                i += 1
            else:
                # This is tricky. Consider the example.
                # AAACAAAA and i = 7. The idea is similar
                # to search step.
                if len != 0:
                    len = lps[len-1]
    
                    # Also, note that we do not increment i here
                else:
                    lps[i] = 0
                    i += 1



    def partition(self, array, low, high):
 
        # choose the rightmost element as pivot
        pivot = array[high]['RANK']
    
        # pointer for greater element
        i = low - 1
    
        # traverse through all elements
        # compare each element with pivot
        for j in range(low, high):
            if array[j]['RANK'] >= pivot:
    
                # If element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1
    
                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
    
        # Swap the pivot element with the greater element specified by i
        (array[i + 1], array[high]) = (array[high], array[i + 1])
    
        # Return the position from where partition is done
        return i + 1
 
    # function to perform quicksort
 
    
    def quickSort(self, array, low, high):
        if low < high:
    
            # Find pivot element such that
            # element smaller than pivot are on the left
            # element greater than pivot are on the right
            pi = self.partition(array, low, high)
    
            # Recursive call on the left of pivot
            self.quickSort(array, low, pi - 1)
    
            # Recursive call on the right of pivot
            self.quickSort(array, pi + 1, high)




    def tokenize(self, query):
        import re
        tokens = re.findall(r'\(|\)|AND|OR|NOT|[^\s()]+', query)
        return tokens

    def infix_to_postfix(self, tokens):
        output = []
        operators = []
        precedence = {'OR': 1, 'AND': 2, 'NOT': 3}

        for token in tokens:
            if self.is_operand(token):
                output.append(token)
            elif token in precedence:
                while (operators and operators[-1] != '(' and
                    precedence[operators[-1]] >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Pop the '('

        while operators:
            output.append(operators.pop())
        
        return output




    def is_operand(self, token):
        # Check if the token is an operand (number/variable)
        return token not in ['AND', 'OR', 'NOT', '(', ')']
