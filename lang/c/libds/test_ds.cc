#include "ds.hpp"
#include <string>
#include <cassert>

using namespace std;

string _msg_;

#define TEST(msg) do { \
  cout << endl << msg << " ... [ -- ]" << endl; \
  _msg_ = msg; \
 } while (0)

#define OK do { \
  cout << _msg_ << " ... [ OK ]" << endl; \
 } while (0)

int
main (void)
{
  // _list_node tests

  TEST ("_list_node constructor");
    DS::_list_node<int> a (100);
    DS::_list_node<int> b (200);
  OK;

  TEST ("_list_node setnext and dump");
    a.setnext(&b);
    assert(a.next() != NULL);
    a.dump();
  OK;

  TEST ("_list_node setprev and dump");
    b.setprev(&a);
    assert(b.prev() != NULL);
    b.dump();
  OK;

  TEST ("_list_node data");
    assert(a.data());
    assert(b.data());
  OK;

  // list tests

  TEST ("list constructor and dump");
    DS::list<int> l;
    l.dump(1);
  OK;

  TEST ("list get");
    assert(l.get(0) == NULL);
    assert(l.get(1) == NULL);
  OK;

  TEST ("list _checklink");
    assert(l._checklink() == 0);
  OK;

  TEST ("list insert");
    assert(l.insert(1));
    assert(l.get(0) != NULL);
    assert(l.insert(2, 0));
    assert(l.insert(5, 1));
    assert(l.insert(10, -1));
    assert(l.size() == 4);
    l.dump(1);
  OK;
  
  TEST ("list dump and get");
    l.dump(1);
    cout << l.get(0) << endl;;
    cout << l.get(1) << endl;;
  OK;

  TEST ("list append");
    assert(l.append(6, -1));
    assert(l.append(8, 0));
    l.dump(1);
  OK;

  TEST ("list locate");
    assert(l.locate(10));
    assert(l.locate(10) == l.get(3));
  OK;

  TEST ("list remove");
    l.remove(1);
    l.dump(1);
  OK;

  TEST ("list remove by negative index");
    l.remove(-1);
    l.dump(1);
  OK;

  TEST ("list purge");
    l.purge();
    l.dump();
  OK;

  // stack tests

  TEST ("stack create");
    DS::stack<int> s;
  OK;

  TEST ("stack push and dump");
    for (int i = 1; i <= 5; i++) s.push(i);
    s.dump(1);
    assert(s.top());
  OK;

  TEST ("stack pop");
    for (int i = 1; i <= 5; i++) {
      cout << s.pop() << endl;
      s.dump(1);
    }
  OK;

  // queue tests

  TEST ("queue constructor");
    DS::queue<int> q;
  OK;

  TEST ("queue push and dump");
    for (int i = 1; i < 5; i++) q.push(i);
    assert(q.size() == 4);
    q.dump(1);
  OK;

  TEST ("queue pop");
    for (int i = 1; i < 5; i++) {
      cout << q.pop() << endl;
      q.dump(1);
    }
  OK;

  // _btree_node tests

  TEST ("_btree_node constructor");
    DS::_btree_node<int> root (0);
    DS::_btree_node<int> left (1);
    DS::_btree_node<int> right (2);
    DS::_btree_node<int> ll (11);
    DS::_btree_node<int> lr (12);
    DS::_btree_node<int> rl (21);
    DS::_btree_node<int> rr (22);
  OK;

  TEST ("_btree_node dump");
    root.dump();
    left.dump();
    right.dump();
    ll.dump();
    lr.dump();
    rl.dump();
    rr.dump();
  OK;

  TEST ("_btree_node setleft and setright and dump");
    root.setleft(&left); root.setright(&right);
    left.setleft(&ll);   left.setright(&lr);
    right.setleft(&rl);  right.setright(&rr);
    root.dump();
  OK;

  TEST ("_btree_node pdump, pretty dump");
    root.pdump();
  OK;

  TEST ("_btree_node itdump");
    root.itdump();
  OK;

  return 0;
}
