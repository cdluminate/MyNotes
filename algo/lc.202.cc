class Solution {
public:
    bool isHappy(int n) {
        map<int, bool> visited;
        visited[n] = true;
        int prev = n, next = 0;
        while (prev != 1) {
            while (prev > 0) {
                next += (prev%10)*(prev%10);
                prev /= 10;
            }
            // next == 1 ?
            if (next == 1) return true;
            // visited next ?
            if (visited.find(next) != visited.end()) {
                return false; // cycle detected
            }
            // add to map and clean up
            visited[next] = true;
            prev = next;
            next = 0;
        }
        return true;
    }
};
