class Solution {
public:
    int bulbSwitch(int n) {
        if (n <= 0) return 0;
        /*
        // naive: emulate. Time out
        vector<bool> bulbs (n, false); // round init
        for (int round = 1; round <= n; round++) { // round 1..n
            if (round == 1) { // round 1: turn on 1k for k in ...
                for (int i = 0; i < bulbs.size(); i++)
                    bulbs[i] = !bulbs[i];
            } else if (round == n) { // round n
                bulbs[n-1] = !bulbs[n-1];
                continue;
            } else { // round 2..n-1
                for (int k = 1; k*round <= n; k++) {
                    bulbs[k*round-1] = !bulbs[k*round-1];
                }
            }
        }
        return count(bulbs.begin(), bulbs.end(), true);
        */
        
        // a bulb will end up on if it is switched an odd number of times.
        // only the sqaure numbers have odd number of devisors.
        // so we just count the square numbers <= n
        // 4: 1,4 => 2, 9: 1,4,9 => 3, ..., n => int(sqrt(n))
        return (int)sqrt(n);
    }
};
