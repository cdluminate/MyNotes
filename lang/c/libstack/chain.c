/* libstack
   2015 Lumin <cdluminate@gmail.com>
   BSD-2-Clause
 */
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

struct CHAIN {
	struct CHAIN * prev;
	long   id;
	char * label;
	void * blob; /* extentions */
	struct CHAIN * next;
};

void
chain_print (struct CHAIN * node)
{
	/* check if node is valid */
	if (NULL == node) {
		printf ("* NODE (NULL) : NULL\n");
		return;
	}
	/* print the node */
	printf ("* NODE # (%ld) @ %p\n"
			"       : prev  = %p , next = %p\n"
			"       : label = %s , blob = %p\n",
			node -> id, node,
			node -> prev, node -> next,
			node -> label, node -> blob);
	return;
}

struct CHAIN *
_chain_tail (struct CHAIN * head)
{
	/* check if head is valid */
	if (NULL == head) {
		printf ("E: _chain_tail(): NULL == head\n");
		exit (EXIT_FAILURE);
	}
	/* move to the last node */
	struct CHAIN * _cp;
	_cp = head;
	while (NULL != 	_cp -> next) {
		_cp = _cp -> next;
	}
	return _cp;
}

struct CHAIN *
_chain_head (struct CHAIN * node)
{
	/* check if head is valid */
	if (NULL == node) {
		printf ("E: _chain_head(): NULL == node\n");
		exit (EXIT_FAILURE);
	}
	/* move to the last node */
	struct CHAIN * _cp;
	_cp = node;
	while (NULL != 	_cp -> prev) {
		_cp = _cp -> prev;
	}
	return _cp;
}

/* Create a node of a chain, which can be a head or middle one */
struct CHAIN *
chain_create (int id, char * label, void * blob)
{
	struct CHAIN * _cp;
	_cp = malloc (sizeof (struct CHAIN) );
	if (NULL == _cp) {
		perror ("malloc");
		exit (EXIT_FAILURE);
	}
	/* assign value as expected */
	bzero (_cp, sizeof (struct CHAIN) );
	_cp -> id = id;
	_cp -> label = label;
	_cp -> blob = blob;
	return _cp;
}

struct CHAIN *
chain_kill (struct CHAIN * node)
{
	struct CHAIN * cp;
	cp = NULL;
	/* check if node is NULL */
	if (NULL == node)
		return NULL;
	/* if prev is not NULL, clean the bind */
	if (NULL != node -> prev) {
		cp = node -> prev;
		node -> prev -> next = NULL;
	}
	/* free node -> blob first, if not NULL */
	if (NULL != node -> blob)
		free (node -> blob);
	bzero (node, sizeof (struct CHAIN));
	free (node);
	return cp;
}

/* Initialize a new chain */
struct CHAIN *
chain_init (char * label, void * blob)
{
	struct CHAIN * head;
	head = chain_create(0, label, blob);
	/* fill in init values */
	head -> prev = NULL;
	head -> next = NULL;
	/* chain_init returns the head pointer of a new chain */
	return head;
}

struct CHAIN *
chain_append (struct CHAIN * head, struct CHAIN * tailnew)
{
	/* check if the tailnew is valid */
	if (NULL == tailnew) {
		printf ("E: chain_append(): invalid tailnew\n");
		exit (EXIT_FAILURE);
	}
	/* move to the last node */
	struct CHAIN * _cp;
	_cp = _chain_tail (head);
	/* append the tailnew after the last node */
	tailnew -> next = NULL;
	tailnew -> prev = _cp;
	_cp -> next = tailnew;
	/* chain_append returns * of tailnew */	
	return tailnew;
}

struct CHAIN *
chain_fastappend (struct CHAIN * head, char * label, void * blob)
{
	/* move to tail of chain */
	struct CHAIN * _cp, * _cursor;
	_cursor = _chain_tail (head);
	_cp = chain_create ( (_cursor -> id) + 1, label, blob );
	/* create and append a new chain */
	chain_append (head, _cp);
	return _cp;
}

void
chain_dump (struct CHAIN * node)
{
	struct CHAIN * cp;
	cp = _chain_head (node);
	do {
		chain_print (cp);
		cp = cp -> next;
	} while (NULL != cp);
	return;
}

void *
chain_destroy (struct CHAIN * head)
{
	struct CHAIN * _cp;
	_cp = _chain_tail (head);
	/* free until NULL == prev */
	struct CHAIN * _prev;
	do {
		_prev = _cp -> prev;
		if (NULL != _cp -> blob)
			free (_cp -> blob);
		free (_cp);
		_cp = _prev;
	} while (NULL != _cp);
	return NULL;
}

struct CHAIN *
chain_cat (struct CHAIN * dest, struct CHAIN * src)
{
	/* check if the tailnew is valid */
	if (NULL == dest || NULL == src) {
		printf ("E: chain_cat(): invalid dest or src\n");
		return NULL;
	}
	/* append the src after the  dest */
	dest -> next = src;
	src -> prev = dest;
	/* returns head of the whole chain */	
	return _chain_head (dest);
}

struct CHAIN *
chain_genindex (struct CHAIN * node)
{
	if (NULL == node)
		return NULL;

	/* find the head of the chain */
	struct CHAIN * cp;
	cp = _chain_head (node);

	if (0 != cp -> id) {
		printf ("E: chain_genindex(): Wow ! the id of head is not 0.\n");
		exit (EXIT_FAILURE);
	}
	while (NULL != cp -> next) {
		cp -> next -> id = cp -> id + 1;
		cp = cp -> next;
	}
	return _chain_head (node);
}

struct CHAIN *
chain_pick (struct CHAIN * node, long id)
{
	struct CHAIN * cp;
	cp = _chain_head (node);
	while (NULL != cp && id != cp -> id) {
		cp = cp -> next;
	}
	if (NULL == cp) {
		printf ("E: chain_pick(): id requested not found.\n");
		return NULL;
	}
	return cp;
}

struct CHAIN *
chain_insert (struct CHAIN * dest, struct CHAIN * node)
{
	if (NULL == node || NULL == dest)
		return NULL;
	/* save dest -> next */
	struct CHAIN * cp;
	cp = dest -> next;
	/* change node */
	node -> prev = dest;
	node -> next = dest -> next;
	/* put node in chain */
	dest -> next = node;
	cp -> prev = node;
	/* regenerate the index of chain */
	chain_genindex (dest);
	return dest -> next;
}

struct CHAIN *
chain_remove (struct CHAIN * node)
{
	if (NULL == node)
		return NULL;
	struct CHAIN * cp;
	cp = _chain_head (node);
	chain_cat (node -> prev, node -> next);
	chain_kill (node);
	chain_genindex (node);
	return _chain_head (node);
}

struct CHAIN *
chain_idremove (struct CHAIN * node, long id)
{
	return chain_remove (chain_pick (node, id));
	/*chain_cat (chain_pick (node, id-1), chain_pick (node, id+1));
	chain_kill (node);
	chain_genindex (node);
	return _chain_head (node); */ /* XXX: double free bug */
}

struct CHAIN *
chain_fastinsert (struct CHAIN * dest, char * label, void * blob)
{
	struct CHAIN * cp;
	cp = chain_create (dest -> id + 1, label, blob);
	return chain_insert (dest, cp);
}

struct CHAIN *
chain_idfastinsert (struct CHAIN * node, long id, char * label, void * blob)
{
	return chain_fastinsert (chain_pick(node, id), label, blob);
}

/* vim : set ts = 4 */
