/**
 * @source topological sorting by source removal method
 * @ref book pp.142
 */
#include <cstdlib>
#include <cassert>
#include <iostream>
#include <vector>
#include "helper.hpp"
using namespace std;

#define DEBUG 1

static int G[7][7] = {
// a b c d e f g
  {0,1,1,0,0,0,0},
  {0,0,0,0,1,0,1},
  {0,0,0,0,0,1,0},
  {1,1,1,0,0,1,1},
  {0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0},
  {0,0,0,0,1,1,0} }; // dabcgef, 4123756, 3012645

/*
  @info calculate colomn sum of a matrix
  mat: mat pointer
  cur: cursor, 0-based
  row: 1-based
  col: 1-based
 */
template <typename TP>
static TP matAddCol(TP* mat, int cur, int row, int col)
{
  assert(cur < col);
  TP colSum = (TP)0;
  for (int i = 0; i < row; i++) {
    //colSum += mat[i][cur];
    colSum += *((mat+i*col)+cur);
  }
  return colSum;
}

/*
  @info get the in-degree of a node
 */
template <typename TP>
static TP getInDegree(TP* Graph, int cur, int size)
{
  return matAddCol(Graph, cur, size, size);
}

/*
  @info remove a row in a matrix
 */
template <typename TP>
static void matZeroRow(TP* mat, int cur, int row, int col)
{
  assert(cur < row);
  for (int i = 0; i < col; i++) {
    *((mat+cur*col)+i) = (TP)0;
  }
  return;
}

/*
  @info do topological sort, destructive to input data
 */
template <typename TP>
static vector<TP> sourceRemoval(TP *G, int size)
{
  vector<TP> bits;
  vector<TP> seq;
  for (int i = 0; i < size; i++) bits.push_back((TP)1);
  while (xvasum<int>(bits) > 0) {
    if (DEBUG) xvdump(bits);
    for (int i = 0; i < size; i++) { // scan all nodes
      if (bits.at(i) == 0) continue; // except for those been removed
      if (getInDegree(G, i, size) == (TP)0 && bits.at(i) == 1) {
        // can be removed
        if (DEBUG) cout<< "removing " << i << endl;
        seq.push_back((TP)i);
        bits.at(i) = 0;
        matZeroRow(G, i, size, size);
        break;
      }
    }
  }
  return seq;
}

int
main(void)
{
  for (int i = 0; i < 7; i++) {
    //cout<< matAddCol<int>((int*)G, i, 7, 7) << endl;
    cout << getInDegree((int*)G, i, 7);
  } // 1220232
  vector<int> seq = sourceRemoval((int*)G, 7);
  xvdump<int>(seq); // dabcgef
  return 0;
}
