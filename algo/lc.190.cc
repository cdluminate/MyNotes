class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        /*
        stack<uint32_t> bits;
        // collect the bits
        for (int i = 0; i < 32; i++) {
            bits.push(n & (0x1 << i));
        }
        // get the reversed bits
        uint32_t ret = 0;
        uint32_t base = 0x1;
        while (!bits.empty()) {
            if (bits.top()) ret |= base;
            bits.pop();
            base <<= 1;
        }
        return ret;
        */ // accepted but naive
        uint32_t ret = 0;
        for (int i = 0; i < 32; i++) {
            ret |= (0x1 & n);
            n >>= 1;
            if (i != 31) ret <<= 1;
        }
        return ret;
    }
};
