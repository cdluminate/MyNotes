/* Brainfuck language

 @ref http://blog.csdn.net/redraiment/article/details/7483062

 Brainfuck contains an array of size 30000, and a data pointer
 pointing to the elements in array.

 + : INC                                  : ++(*ptr)
 - : DEC                                  : --(*ptr)
 > : Move pointer to next                 : ++ptr
 < : Move pointer to previous             : --ptr
 . : Print Character (ASCII)              : putchar(*ptr)
 , : Read Character                       : *ptr = getchar()
 [ : Go forward to ] in case of 0         : while(*ptr) {
 ] : Go backward to [ in case of non-zero : }

 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define TOKENS "><+-.,[]"

#define CODE_SEGMENT_SIZE 30000
#define STACK_SEGMENT_SIZE 1000
#define DATA_SEGMENT_SIZE 30000

typedef void (*Callback)(void);

struct {
  char cs[CODE_SEGMENT_SIZE];   /* Code Segment */
  long ip;                      /* Instruction Pointer */

  char ss[STACK_SEGMENT_SIZE];  /* Stack Segment */
  long sp;                      /* Stack Pointer */

  char ds[DATA_SEGMENT_SIZE];   /* Data Segment */
  long bp;                      /* Base Pointer */

  Callback fn[128];
} vm;

void vm_forward() {
  vm.bp = (vm.bp + 1) % DATA_SEGMENT_SIZE;
}

void vm_backward() {
  vm.bp = (vm.bp + DATA_SEGMENT_SIZE - 1) % DATA_SEGMENT_SIZE;
}

void vm_increment() {
  vm.ds[vm.bp]++;
}

void vm_decrement() {
  vm.ds[vm.bp]--;
}

void vm_input() {
  vm.ds[vm.bp] = getchar();
}

void vm_output() {
  putchar(vm.ds[vm.bp]);
}

void vm_while_entry() {
  if (vm.ds[vm.bp]) { // update stack if non-zero
    vm.ss[vm.sp] = vm.ip - 1; // push the instruction pointer onto stack
    vm.sp++; // stack pointer increment
  } else { // seek to ] if zero
    int c = 1;
    for (vm.ip++; vm.cs[vm.ip] && c; vm.ip++) {
      if (vm.cs[vm.ip] == '[') {
        c++; // enter another layer of nested [ loop
      } else if (vm.cs[vm.ip] == ']') {
        c--; // exit nested loop
      }
    }
    // when 1. CS[IP] is NULL or 2. get out from loop, this for loop ends.
  }
}

void vm_while_exit() {
  if (vm.ds[vm.bp]) { // go back to [ if non-zero
    vm.sp--; // move stack pointer to the new top
    vm.ip = vm.ss[vm.sp]; // restore instruction pointer from stack top
  }
  // do nothing is zero
}

void vm_setup() {
  int c;
  int i;

  // flush VM memory space
  memset(&vm, 0, sizeof(vm));
  // initialize callbacks
  vm.fn['>'] = vm_forward;
  vm.fn['<'] = vm_backward;
  vm.fn['+'] = vm_increment;
  vm.fn['-'] = vm_decrement;
  vm.fn['.'] = vm_output;
  vm.fn[','] = vm_input;
  vm.fn['['] = vm_while_entry;
  vm.fn[']'] = vm_while_exit;
  // read code in lexical manner
  for (i = 0; (c = getchar()) != EOF;) {
    if (strchr(TOKENS, c)) {
      vm.cs[i] = c;
      i++;
    }
  }
}

void vm_run() {
  while (vm.cs[vm.ip]) { // while instruction is not 0
    vm.fn[vm.cs[vm.ip]](); // execute the instruction at IP
    vm.ip++; // move IP to next one
  }
}

int main(int argc, char* argv[]) {
  if (argc > 1) {
    freopen(argv[1], "r", stdin);
  }
  // create VM, initialize callbacks, and read the code into CS
  vm_setup();
  // actually run the code
  vm_run();

  return 0;
}

/* Code example

++++++ [ > ++++++++++ < - ] > +++++ .
  this one prints A

++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.  
  this one prints hello world

 */
