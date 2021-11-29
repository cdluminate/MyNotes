/* libstack
   2015 Lumin
   this is a pseudo cpp extension in ANSI C, for libstack
 */

struct CHAINPP {
	void           (* print             )(struct CHAIN * node);
	struct CHAIN * (* _tail             )(struct CHAIN * head);
	struct CHAIN * (* _head             )(struct CHAIN * node);
	struct CHAIN * (* create            )(int id, char * label, void * blob);
	struct CHAIN * (* init              )(char * label, void * blob);
	struct CHAIN * (* append            )(struct CHAIN * head, struct CHAIN * tailnew);
	struct CHAIN * (* fastappend        )(struct CHAIN * head, char * label, void * blob);
	void           (* dump              )(struct CHAIN * node);
	void *         (* destroy           )(struct CHAIN * head);
} chainpp ;

void
chainpp_init (struct CHAINPP * p)
{
	p->print      = chain_print;
	p->_tail      = _chain_tail;
	p->_head      = _chain_head;
	p->create     = chain_create;
	p->init       = chain_init;
	p->append     = chain_append;
	p->fastappend = chain_fastappend;
	p->dump       = chain_dump;
	p->destroy    = chain_destroy;
	return;
}
