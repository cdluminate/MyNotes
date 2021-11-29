#include <unistd.h>
#include "lumin_log.h"

int
main (void)
{
  LOG_INFO ("hello, this is a demo of rainbowlog, originated from libcdalog");

  LOG_DEBUG ("Debug");
  LOG_INFO ("Info");
  LOG_WARN ("Warning");
  LOG_ERROR ("Error");
  
  LOG_DEBUGF ("Formatted debug %s", "string");
  LOG_INFOF ("Formatted info %s", "string");
  LOG_WARNF ("Formatted warnning %s", "string");
  LOG_ERRORF ("Formatted error %s", "string");
  LOG_WARNF ("You should have noticed that error messages are followed by"
             " a backtrace.");

  LOG_INFOF ("%s", "Happy hacking!");

  return 0;
}
