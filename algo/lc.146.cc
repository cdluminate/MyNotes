#include <iostream>
#include <list>
#include <map>
#include <unordered_map> // faster on lookup time
using namespace std;

class LRUCache {
private:
    struct CacheNode {
        int key;
        int value;
        CacheNode(int k, int v) : key(k), value(v) {}
    };

    int capacity_;
    list<CacheNode> cachelist_;
    unordered_map<int, list<CacheNode>::iterator> cachemap_;

public:
    LRUCache(int capacity) {
        this->capacity_ = capacity;
    }
    
    int get(int key) {
        // not found: -1
        if (cachemap_.find(key) == cachemap_.end())
            return -1;
        // found: step1: move the node to top
        cachelist_.splice(cachelist_.begin(), cachelist_, cachemap_[key]);
        // found: step2: update map
        cachemap_[key] = cachelist_.begin();
        // found: step3: return the value
        return cachemap_[key]->value;
    }
    
    void put(int key, int value) {
        if (cachemap_.find(key) == cachemap_.end()) {
            // not found: check capacity first
            if (cachelist_.size() >= capacity_) {
                cachemap_.erase(cachelist_.back().key);
                cachelist_.pop_back();
            }
            // insert to top, add to map
            cachelist_.push_front(CacheNode(key, value));
            cachemap_[key] = cachelist_.begin();
        } else {
            // found: move to top, update map
            cachemap_[key]->value = value;
            cachelist_.splice(cachelist_.begin(), cachelist_, cachemap_[key]);
            cachemap_[key] = cachelist_.begin();
        }
    }
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache obj = new LRUCache(capacity);
 * int param_1 = obj.get(key);
 * obj.put(key,value);
 */

int
main(void)
{
	LRUCache cache = LRUCache( 2 /* capacity */ );

	cache.put(1, 1);
	cache.put(2, 2);
	cout << cache.get(1) << endl;      // returns 1
	cache.put(3, 3);    // evicts key 2
	cout << cache.get(2) << endl;       // returns -1 (not found)
	cache.put(4, 4);    // evicts key 1
	cout << cache.get(1) << endl;       // returns -1 (not found)
	cout << cache.get(3) << endl;       // returns 3
	cout << cache.get(4) << endl;       // returns 4

	return 0;
}
