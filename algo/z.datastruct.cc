/*
 * Data Structure. Tsinghua Pub.
 *
 * The interface definition is not quite beautiful,
 * but the list is a bit useful.
 */

/* --- Linear List : Sequential list --- */

typedef struct _SqList {
	ElemType *elem;
	int length;
	int listsize;
} SqList; // Sequential list.

InitList(&L);
DestroyList(&L);
ClearList(&L);
ListEmpty(L);
ListLength(L);
GetElem(L, i, &e);
LocateElem(L, e, compare());
PriorElem(L, e, &pre);
NextElem(L, e, &next);
ListInsert(&L, i, e);
ListDelete(&L, i, &e);
ListTraverse(L, visit());

UniteList(List &a, List &b); // A \cup B
MergeList(List a, List b, List &c); // a, b sorted.

/* --- Linear List : Linked list --- */

typedef struct _LNode {
	ElemType data;
	struct _LNode *next;
} LNode, *LinkList; // Linked list.
// variants: Circular linked list.
// variants: linked list with head/tail node.

typedef struct _DoLNode {
	ElemType data;
	struct _DoLNode *prev;
	struct _DoLNode *next;
} DoLNode, *DoLinkList; // Double linked list.

MakeNode(&p, e);
FreeNode(&p);
InitList(&L);
DestroyList(&L);
ClearList(&L);
InsFirst(h, s);
DelFirst(h, &q);
Append(&L, s);
Remove(&L, &q);
InsBefore(&L, &p, s);
InsAfter(&L, &p, s);
SetCurElem(&p, e);
GetCurElem(&p);
ListEmpty(L);
ListLength(L);
GetHead(L);
GetLast(L);
PriorPos(L, p);
NextPos(L, p);
LocateElem(L, e, compare());
ListTraverse(L, visit());

MergeList(L a, L b, L &c); // a, b sorted.

/* --- Linear list application --- */
// Polynomial evaluation

/* --- Stack --- */

typedef struct {
	ElemType *base;
	ElemType *top;
	int stacksize;
} SqStack;

// variant: using linked list as stack.

InitStack(&S);
DestroyStack(&S);
ClearStack(&S);
StackEmpty(S);
StackLength(S);
GetTop(S, &e);
Push(&S, e);
Pop(&S, &e);
StackTraverse(S, visit());

//app: number system conversion
//app: parenthesis matching check
//app: line edition.
//app: solving a maze.
//app: expression evaluation
//app: Hanoi

/* --- Queue --- */

typedef struct QNode {
	ElemType data;
	struct QNode *next;
} QNode, *QueuePtr;

typedef struct {
	QueuePtr front;
	QueuePtr rear;
} LinkQueue;

// variant: deque (double-end queue)
// variant: circular queue

InitQueue(&Q);
DestroyQueue(&Q);
ClearQueue(&Q);
QueueEmpty(Q);
QueueLength(Q);
GetHead(Q, &e);
EnQueue(&Q, e);
DeQueue(&Q. &e);
QueueTraverse(Q, visit());

/* --- String --- */

typedef unsigned char String[STR_LEN];

typedef struct {
	char *ch; // On heap. managed by malloc() and free()
	int length;
}

// variant: string by chunked list

StrAssign(&T, chars);
StrCopy(&T, S);
StrEmpty(S);
StrCompare(S, T);
StrLength(S);
ClearString(&S);
Concat(&T, S1, S2);
SubString(&Sub, S, pos, len);
Index(S, T, pos); // strstr
Replace(&S, T, V);
StrInsert(&S, pos, T);
StrDelete(&S, pos, len);
DestroyString(&S);

//app: KMP algo (strstr)

/* --- Array --- */

typedef struct {
	ElemType *base;
	int dim;
	int *bounds;
	int *constants;
}
//Note: column major and row major

InitArray(&A, n, bounds);
DestroyArray(&A);
Value(A, &e, indexes);
Assign(&A, e, indexes);

// variant: special matrix

typedef struct {
	int i, j;
	ElemType e;
} Triple;
typedef struct {
	Triple data[SIZE];
	int col, row, non-zero;
} SparseMatrix ;

// create, destroy, print, copy, add, sub, mult, transpose
// Better interface: see BLAS and LAPACK

/* --- General List --- */

Init, Create, Destroy, Copy, Length, Depth, Empty, Head, Tail,
InsertFirst, DeleteFirst, Traverse.

/* --- Trees --- */

Init, Destroy, Create, Clear, Empty, Depth, Root, Value, Assign,
Parent, LeftChild, RightSibling, InsertChild, DeleteChild, TraverseTree.

// variant: Binary Tree
// + PreOrderTraversal, InOrderTraversal, PostOrderTraversal, LevelOrderTraversal
// variant: Threaded binary tree
// storage structure: parent pointer
// storage structure: child pointer

//app: convertion between binary tree and forest.
//app: Huffman Tree and Huffman coding
//app: searching with backtracking
//app: 4-queen / 8-queen
//app: in-order sequence X pre-order sequence -> binary tree

/* --- Graph --- */

Create, Destroy, LocateVex, GetVex, PutVex, FirstAdjVex, NextAdjVex,
InsertVex, DeleteVex, InsertArc, DeleteArc, DFSTraverse, BFSTraverse.

// graph type: UG, DN, UDG, UDN, DAG, (network has weights)
// storage structure: adjacent matrix
// storage structure: adjacency list
// storage structure: orthogonal list
// storage structure: adjacency multilist
// app: Minimum Cost Spanning Tree, Prim algo, Kruskal algo.
// app: Topological sort. (DAG)
// app: shortest path. Dijkstra algo.

/* --- Dynamic storage management --- */
// e.g. Garbage collection

/* --- searching --- */
// Algorithm performance: Average search length (ASL).
// sequential search.
// binary search for ordered list.
// static optimal search tree
// dynamic searching: Binary Sort Tree
// dynamic searching: balanced Binary Tree
// dynamic searching: B- Tree and B+ Tree
// dynamic searching: Digitla Search Trees
// Hash Table, hash function

/* --- sorting --- */
// Ref: TAOCP Volume 3
// insertion sort, e.g. shell's sort, namely Diminishing Increment Sort
// swapping sort, bubble sort, quick sort
// selection sort: simple sel sort, tree sel sort, heap sort
// merging sort
// radix sort

// sorting with external storage

/* --- file system --- */
...
