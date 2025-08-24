class Solution:

    def trie(self, products: List[str]) -> None:
        self.tree = dict()
        for word in products:
            self.insert(word)

    def insert(self, word) -> None:
        cursor = self.tree
        for char in word:
            if char not in cursor:
                cursor[char] = dict()
            cursor = cursor[char]
        cursor['is_end'] = True

    def match(self, word, cursor = None) -> Optional[dict]:
        # return the subtree matching with word
        cursor = self.tree if cursor is None else cursor
        for char in word:
            if char not in cursor:
                return None
            cursor = cursor[char]
        return cursor

    def suggest(self, prefix: str) -> List[str]:
        subtree = self.match(prefix)
        if subtree is None:
            return []
        # DFS and collect suggestions
        results = []
        def dfs(cursor, word='') -> None:
            if not cursor or len(results) > 2:
                return
            # is the current word complete?
            #print('debug>', isinstance(cursor, dict), cursor)
            if 'is_end' in cursor:
                results.append(prefix + word)
                print('debug>', prefix, results)
            # traverse next character
            for k in sorted(cursor.keys()):
                if k == 'is_end': continue
                dfs(cursor[k], word+k)
        dfs(subtree, '')
        return results #[:3]

    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        self.trie(products)
        #print('trie>', self.tree)
        results = []
        for i in range(len(searchWord)):
            word = searchWord[:i+1]
            result = self.suggest(word)
            results.append(result)
        return results
