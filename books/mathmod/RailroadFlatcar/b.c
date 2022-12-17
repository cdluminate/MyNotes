#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

float
obj (float x1, float x2, float x3, float x4, float x5, float x6, float x7,
     float y1, float y2, float y3, float y4, float y5, float y6, float y7)
{
 return 48.7 *x1 + 52.0 *x2 + 61.3 *x3 + 72.0 *x4 + 48.7 *x5 + 52.0 *x6 + 64.0 *x7
	       + 48.7 *y1 + 52.0 *y2 + 61.3 *y3 + 72.0 *y4 + 48.7 *y5 + 52.0 *y6 + 64.0 *y7;
}

/* please compile with c99 compiler */
/* c99 -Wall -O2 *.c */
int
main(void)
{
 /* bounds of x1 - x7 */
 for (float x1 = 0.0; x1 <= 8.0; x1++) {
 for (float x2 = 0.0; x2 <= 7.0; x2++) {
 for (float x3 = 0.0; x3 <= 9.0; x3++) {
 for (float x4 = 0.0; x4 <= 6.0; x4++) {
 for (float x5 = 0.0; x5 <= 6.0; x5++) {
 for (float x6 = 0.0; x6 <= 4.0; x6++) {
 for (float x7 = 0.0; x7 <= 8.0; x7++) {
  /* bounds of y1 - y7 */
  for (float y1 = 0.0; y1 <= 8.0; y1++) {
  for (float y2 = 0.0; y2 <= 7.0; y2++) {
  for (float y3 = 0.0; y3 <= 9.0; y3++) {
  for (float y4 = 0.0; y4 <= 6.0; y4++) {
  for (float y5 = 0.0; y5 <= 6.0; y5++) {
  for (float y6 = 0.0; y6 <= 4.0; y6++) {
  for (float y7 = 0.0; y7 <= 8.0; y7++) {
   /* constraint group 1 : no exceed max number */
   if (x1 + y1 <= 8.0) {
   if (x2 + y2 <= 7.0) {
   if (x3 + y3 <= 9.0) {
   if (x4 + y4 <= 6.0) {
   if (x5 + y5 <= 6.0) {
   if (x6 + y6 <= 4.0) {
   if (x7 + y7 <= 8.0) {
    /* constraint group 2 : no exceed max length */
    if (48.7 *x1 + 52.0 *x2 + 61.3 *x3 + 72.0 *x4 + 48.7 *x5 + 52.0 *x6 + 64.0 *x7 <= 1020.0) {
    if (48.7 *y1 + 52.0 *y2 + 61.3 *y3 + 72.0 *y4 + 48.7 *y5 + 52.0 *y6 + 64.0 *y7 <= 1020.0) {
    /* constraint group 3 : no exceed max load */
    if (2000.0 *x1 + 3000.0 *x2 + 1000.0 *x3 +  500.0 *x4 + 4000.0 *x5 + 2000.0 *x6 + 1000.0 *x7 <= 40000.0) {
    if (2000.0 *y1 + 3000.0 *y2 + 1000.0 *y3 +  500.0 *y4 + 4000.0 *y5 + 2000.0 *y6 + 1000.0 *y7 <= 40000.0) {
     /* constraint group 4 : special */
     if (48.7 *x5 + 52.0 *x6 + 64.0 *x7 <= 302.7) {
     if (48.7 *y5 + 52.0 *y6 + 64.0 *y7 <= 302.7) {
      printf("%1.0f %1.0f %1.0f %1.0f %1.0f %1.0f %1.0f | %1.0f %1.0f %1.0f %1.0f %1.0f %1.0f %1.0f | %4.0f\n",
             x1,x2,x3,x4,x5,x6,x7,
             y1,y2,y3,y4,y5,y6,y7,
			 obj (x1,x2,x3,x4,x5,x6,x7,
                  y1,y2,y3,y4,y5,y6,y7)
	        );
     }}
	}}
    }}
   }}}}}}}
  }}}}}}}
 }}}}}}}
 return 0;
}
