#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

int best[14];

void
bestsave (int x1, int x2, int x3, int x4, int x5, int x6, int x7,
          int y1, int y2, int y3, int y4, int y5, int y6, int y7)
{
 best[ 0] = x1;
 best[ 1] = x2;
 best[ 2] = x3;
 best[ 3] = x4;
 best[ 4] = x5;
 best[ 5] = x6;
 best[ 6] = x7;
 best[ 7] = y1;
 best[ 8] = y2;
 best[ 9] = y3;
 best[10] = y4;
 best[11] = y5;
 best[12] = y6;
 best[13] = y7;
 return;
}

float
obj (int x1, int x2, int x3, int x4, int x5, int x6, int x7,
     int y1, int y2, int y3, int y4, int y5, int y6, int y7)
{
 return 48.7 *x1 + 52.0 *x2 + 61.3 *x3 + 72.0 *x4 + 48.7 *x5 + 52.0 *x6 + 64.0 *x7
	       + 48.7 *y1 + 52.0 *y2 + 61.3 *y3 + 72.0 *y4 + 48.7 *y5 + 52.0 *y6 + 64.0 *y7;
}

float
objfrombest (int array[14])
{
	return obj(array[ 0],
               array[ 1],
               array[ 2],
               array[ 3],
               array[ 4],
               array[ 5],
               array[ 6],
               array[ 7],
               array[ 8],
               array[ 9],
               array[10],
               array[11],
               array[12],
               array[13]);
}

/* please compile with c99 compiler */
/* c99 -Wall -O2 *.c */
int y1 = 0;
int y2 = 0;
int y3 = 0;
int y4 = 0;
int y5 = 0;
int y6 = 0;
int y7 = 0;

int
main(void)
{
 /* bounds of x1 - x7 */
 for (int x1 = 0; x1 <= 8; x1++) {
 for (int x2 = 0; x2 <= 7; x2++) {
 for (int x3 = 0; x3 <= 9; x3++) {
 for (int x4 = 0; x4 <= 6; x4++) {
 for (int x5 = 0; x5 <= 6; x5++) {
 for (int x6 = 0; x6 <= 4; x6++) {
 for (int x7 = 0; x7 <= 8; x7++) {
  /* bounds of y1 - y7 */
  #pragma omp parallel for num_threads(4) private(y1,y2,y3,y4,y5,y6,y7)
  for (y1 = 0; y1 <= 8; y1++) {
  for (y2 = 0; y2 <= 7; y2++) {
  for (y3 = 0; y3 <= 9; y3++) {
  for (y4 = 0; y4 <= 6; y4++) {
  for (y5 = 0; y5 <= 6; y5++) {
  for (y6 = 0; y6 <= 4; y6++) {
  for (y7 = 0; y7 <= 8; y7++) {
   /* constraint group 1 : no exceed max number */
   if (x1 + y1 <= 8) {
   if (x2 + y2 <= 7) {
   if (x3 + y3 <= 9) {
   if (x4 + y4 <= 6) {
   if (x5 + y5 <= 6) {
   if (x6 + y6 <= 4) {
   if (x7 + y7 <= 8) {
    /* constraint group 2 : no exceed max length */
    if (48.7 *x1 + 52.0 *x2 + 61.3 *x3 + 72.0 *x4 + 48.7 *x5 + 52.0 *x6 + 64.0 *x7 <= 1020.0) {
    if (48.7 *y1 + 52.0 *y2 + 61.3 *y3 + 72.0 *y4 + 48.7 *y5 + 52.0 *y6 + 64.0 *y7 <= 1020.0) {
    /* constraint group 3 : no exceed max load */
    if (2000.0 *x1 + 3000.0 *x2 + 1000.0 *x3 +  500.0 *x4 + 4000.0 *x5 + 2000.0 *x6 + 1000.0 *x7 <= 40000.0) {
    if (2000.0 *y1 + 3000.0 *y2 + 1000.0 *y3 +  500.0 *y4 + 4000.0 *y5 + 2000.0 *y6 + 1000.0 *y7 <= 40000.0) {
     /* constraint group 4 : special */
     if (48.7 *x5 + 52.0 *x6 + 64.0 *x7 <= 302.7) {
     if (48.7 *y5 + 52.0 *y6 + 64.0 *y7 <= 302.7) {
	  /* save if better, then print it out */
      if (obj (x1,x2,x3,x4,x5,x6,x7,y1,y2,y3,y4,y5,y6,y7) >= objfrombest(best) ) {
       bestsave (x1,x2,x3,x4,x5,x6,x7,y1,y2,y3,y4,y5,y6,y7);
       printf("%d %d %d %d %d %d %d | %d %d %d %d %d %d %d | %4.2f\n",
             x1,x2,x3,x4,x5,x6,x7,
             y1,y2,y3,y4,y5,y6,y7,
			 obj (x1,x2,x3,x4,x5,x6,x7,
                  y1,y2,y3,y4,y5,y6,y7)
	        );
	  }
     }}
	}}
    }}
   }}}}}}}
  }}}}}}}
 }}}}}}}
 return 0;
}
