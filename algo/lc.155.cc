class MinStack {
public:
    /** initialize your data structure here. */
    stack<int> st_;
    stack<int> min_;
    
    void push(int x) {
        st_.push(x);
        if (min_.empty() || x <= min_.top())
            min_.push(x);
    }
    
    void pop() {
        if (st_.top() == min_.top()) {
            min_.pop();
            st_.pop();
        } else {
            st_.pop();
        }
    }
    
    int top() {
        return st_.top();
    }
    
    int getMin() {
        return min_.top();
    }
};

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack obj = new MinStack();
 * obj.push(x);
 * obj.pop();
 * int param_3 = obj.top();
 * int param_4 = obj.getMin();
 */
