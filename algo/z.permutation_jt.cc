/*
  @file permutation in Johnson Trotter
 */
#include <iostream>
#include <cassert>
#include <vector>

#define DEBUG 0
#include "helper.hpp"

using namespace std;

static bool
isMobile(int cur, vector<int> terms, vector<int> arrow)
{
    if (cur+arrow.at(cur) >= terms.size() || cur+arrow.at(cur) < 0)
		// cursor+offset shouldn't be out of bound
		return false;
	else if (terms.at(cur) > terms.at(cur+arrow.at(cur)))
		// bigger than the adjacent element
		return true;
	else
		return false;
}

static bool
hasMobile(vector<int> terms, vector<int> arrow)
{
  for (unsigned int i = 0; i < terms.size(); i++) {
	  if (isMobile(i, terms, arrow)) return true;
  }
  return false;
}

static int
getCurMaxMobile(vector<int> terms, vector<int> arrow)
{
	int cur = -1;
	int curvalue = -1;
	if (!hasMobile(terms, arrow)) {
		cout << "no mobile!" << endl;
		return cur;	
	}
	for (unsigned int i = 0; i < terms.size(); i++) {
		if (isMobile(i, terms, arrow)) {
			if (DEBUG) cout << "term " << i << " is mobile" << endl;
			if (terms.at(i) > curvalue) {
				cur = i;
				curvalue = terms.at(i);	
			}
		}
	}
	return cur;
}

static vector<vector<int> >
johnsonTrotter(int n)
{
  vector<vector<int> > res;
  vector<int> terms;
  vector<int> arrow;
  // initialize vectors
  for (int i = 0; i < n; i++) {
    terms.push_back(i+1);
    arrow.push_back(-1);
  }
  // save the first permutation
  res.push_back(vector<int>(terms));
  if (DEBUG) xvdump<int>(terms);
  if (DEBUG) xvdump<int>(arrow);
  while(hasMobile(terms, arrow)) {
	  // find the max mobile element
	  int cur = getCurMaxMobile(terms, arrow);
	  if (cur == -1) cout << "error" << endl;
	  int curvalue = terms.at(cur);
	  if (DEBUG) cout << "mobile value " << curvalue << " at " << cur << endl;
	  // swap it with its adjacent element
	  int tmp1 = terms.at(cur);
	  int tmp2 = arrow.at(cur);
	  int tmpa = arrow.at(cur);
	  terms.at(cur) = terms.at(cur+tmpa);
	  arrow.at(cur) = arrow.at(cur+tmpa);
	  terms.at(cur+tmpa) = tmp1;
	  arrow.at(cur+tmpa) = tmp2;
	  // reverse direction of all the elements larger than curvalue
	  for (unsigned int i = 0; i < terms.size(); i++) {
		  if (terms.at(i) > curvalue) {
			arrow.at(i) = -arrow.at(i);
		  }
	  }
	  // add the new permutation to list
	  res.push_back(vector<int>(terms));
	  if (DEBUG) xvdump<int>(terms);
	  if (DEBUG) xvdump<int>(arrow);
  }
  return res;
}

static int
factorial(int n)
{
	if (n == 0 || n == 1) {
		return 1;    
	} else {
		return n * factorial(n-1);
	}
}

int
main(void)
{
#define ORDER 3
	vector<vector<int> > res = johnsonTrotter(ORDER);
	// do permutation check
	assert(res.size() == factorial(ORDER));
	for (unsigned int i = 0; i < res.size(); i++) {
		vector_dump<int>(res.at(i));
	}
	return 0;
}
