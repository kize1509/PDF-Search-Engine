class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        for i in range(len(word)):
            current = self.root
            for letter in word[i:]:
                if letter not in current.children:
                    current.children[letter] = TrieNode()
                current = current.children[letter]
            current.end_of_word = True

    def search(self, substring):
        substring = substring.lower()
        current = self.root
        for char in substring:
            if char not in current.children:
                return False
            current = current.children[char]
        return True

    def starts_with(self, prefix):
        current = self.root
        for letter in prefix:
            if letter not in current.children:
                return False
            current = current.children[letter]
        return True
    


    def bfs(self):
        queue = [(self.root, "")]
        while queue:
            current, word = queue.pop(0)
            if current.end_of_word:
                print(word)
            for letter, node in current.children.items():
                queue.append((node, word + letter))
        
    def dfs(self):
        def dfs_helper(current, word):
            if current.end_of_word:
                print(word)
            for letter, node in current.children.items():
                dfs_helper(node, word + letter)
        dfs_helper(self.root, "")