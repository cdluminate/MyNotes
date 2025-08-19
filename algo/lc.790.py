class Solution:
    def numTilings(self, n: int) -> int:
        # dpf: the i-th position is fully filled
        dpf = [1, 1, 2]
        MOD = (10**9) + 7
        if n < 3:
            return dpf[n]
        else:
            for i in range(3, n+1):
                dpf_i = 2 * dpf[i-1] + dpf[i-3]
                dpf.append(dpf_i)
            return dpf[-1] % MOD

class Solution:
    def numTilings(self, n: int) -> int:
        # dpp: the i-th position is partially filled
        # dpf: the i-th position is fully filled
        dpp = [None, None, 2]
        dpf = [0, 1, 2]
        MOD = (10**9) + 7
        if n < 3:
            return dpf[n]
        else:
            for i in range(3, n+1):
                dpp_i = 2* dpf[i-2] + dpp[i-1]
                dpf_i = dpf[i-1] + dpf[i-2] + dpp[i-1]
                dpp.append(dpp_i)
                dpf.append(dpf_i)
            return dpf[-1] % MOD
