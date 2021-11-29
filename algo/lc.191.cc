class Solution {
public:
    int hammingWeight(uint32_t n) {
        int ret = 0;
        for (int i = 0; i < 32; i++) {
            ret += (0x1 & n >> i);
        }
        return ret;
    }
};
