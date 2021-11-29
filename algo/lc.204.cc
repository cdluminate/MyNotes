class Solution {
public:
    int countPrimes(int n) {
        if (n <= 1) return 0;
        
        vector<bool> isprime (n, true); // isPrime[0..n-1]
        isprime[0] = false;
        isprime[1] = false;
        for (int i = 2; i < n; i++) {
            if (isprime[i])
                for (int j = 2*i; j < n; j+=i) {
                    isprime[j] = false;
                }
        }
        return count(isprime.begin(), isprime.end(), true);
    }
    /*
        int count = 0;
        for (int i = 1; i < n; i++) {
            if (isPrime(i)) {
                count++;
            }
        }
        return count;
    }
    bool isPrime(int n) {
        if (n <= 1) return false;
        else {
            for (int i = 2; i <= sqrt(n); i++) {
                if (n % i == 0) return false;
            }
            return true;
        }
    }
    */ // naive implementation, too slow
};
