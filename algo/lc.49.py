class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hash2group = dict()  # defaultdict is better.
        for item in strs:
            k = ''.join(list(sorted(list(item))))
            if k not in hash2group:
                hash2group[k] = [item]
            else:
                hash2group[k].append(item)
        return list(hash2group.values())
