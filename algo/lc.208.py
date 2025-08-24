class Trie:

    def __init__(self):
        self.tree = dict()

    def insert(self, word: str) -> None:
        cursor = self.tree
        for char in word:
            if char not in cursor:
                cursor[char] = dict()
            cursor = cursor[char]
        cursor['_is_end'] = True

    def search(self, word: str) -> bool:
        # full match
        cursor = self.tree
        for char in word:
            if char not in cursor:
                return False
            cursor = cursor[char]
        return cursor.get('_is_end', False)

    def startsWith(self, prefix: str) -> bool:
        # partial match
        cursor = self.tree
        for char in prefix:
            if char not in cursor:
                return False
            cursor = cursor[char]
        return True

# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)

class Trie:

    def __init__(self):
        self.tree = dict()

    def insert(self, word: str) -> None:
        for i in range(len(word)):
            # locate the tree node
            cursor = self.tree
            for j in range(i):
                cursor = cursor[word[j]]
            # insert the tree node
            if word[i] not in cursor:
                cursor[word[i]] = dict()
            # mark end flag
            if i == len(word) - 1:
                cursor[word[i]]['_is_end'] = True
        #print('insert', word, self.tree)

    def search(self, word: str) -> bool:
        cursor = self.tree
        for char in word:
            if char not in cursor:
                return False
            else:
                cursor = cursor[char]
        return cursor.get('_is_end', False)

    def startsWith(self, prefix: str) -> bool:
        # partial match
        def match(word, subtree):
            if not word:
                return True
            elif not subtree:
                return False
            elif word[0] not in subtree:
                return False
            else:
                return match(word[1:], subtree[word[0]])
        return match(prefix, self.tree)



# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)

class Trie:

    def __init__(self):
        self.tree = dict()
        self.vocab = dict()

    def insert(self, word: str) -> None:
        for i in range(len(word)):
            # locate the tree node
            cursor = self.tree
            for j in range(i):
                cursor = cursor[word[j]]
            # insert the tree node
            if word[i] not in cursor:
                cursor[word[i]] = dict()
        #print('insert>', word, self.tree)
        self.vocab[word] = True

    def search(self, word: str) -> bool:
        # full match
        return word in self.vocab
         
    def startsWith(self, prefix: str) -> bool:
        # partial match
        def match(word, subtree):
            if not word:
                return True
            elif not subtree:
                return False
            elif word[0] not in subtree:
                return False
            else:
                return match(word[1:], subtree[word[0]])
        return match(prefix, self.tree)
        


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
