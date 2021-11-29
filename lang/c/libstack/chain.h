void
chain_print (struct CHAIN * node);


struct CHAIN *
_chain_tail (struct CHAIN * head);


struct CHAIN *
_chain_head (struct CHAIN * node);


struct CHAIN *
chain_create (int id, char * label, void * blob);


struct CHAIN *
chain_kill (struct CHAIN * node);


struct CHAIN *
chain_init (char * label, void * blob);


struct CHAIN *
chain_append (struct CHAIN * head, struct CHAIN * tailnew);


struct CHAIN *
chain_fastappend (struct CHAIN * head, char * label, void * blob);


void
chain_dump (struct CHAIN * node);


void *
chain_destroy (struct CHAIN * head);


struct CHAIN *
chain_cat (struct CHAIN * dest, struct CHAIN * src);


struct CHAIN *
chain_genindex (struct CHAIN * node);


struct CHAIN *
chain_pick (struct CHAIN * node, long id);


struct CHAIN *
chain_insert (struct CHAIN * dest, struct CHAIN * node);


struct CHAIN *
chain_remove (struct CHAIN * node);


struct CHAIN *
chain_idremove (struct CHAIN * node, long id);


struct CHAIN *
chain_fastinsert (struct CHAIN * dest, char * label, void * blob);


struct CHAIN *
chain_idfastinsert (struct CHAIN * node, long id, char * label, void * blob);

