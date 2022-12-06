class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        template = strs[0]
        prefix = ""
        for i in range(len(template)+1):
            prefix = template[:i]
            if not all(x.startswith(prefix) for x in strs):
                prefix = prefix[:-1]
                break
            else:
                pass
        return prefix
