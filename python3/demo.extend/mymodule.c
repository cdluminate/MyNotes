/** 
 * Python3 extension 
 */
#include <stdio.h>
#include <Python.h>

static PyObject *
my_hello (PyObject *self, PyObject *args)
{
  const char *message = "my_hello()";
  int status = printf("%s\n", message);
  return PyLong_FromLong(status);
}

static PyObject *
my_echo (PyObject *self, PyObject *args)
{
  const char *command;
  int status;

  if (!PyArg_ParseTuple(args, "s", &command))
    return NULL;
  status = printf("%s\n", command);
  return PyLong_FromLong(status);
}

static PyMethodDef MyMethods[] = {
  {"hello", my_hello, METH_VARARGS, "print a msg"},
  {"echo", my_echo, METH_VARARGS, "echo a msg"},
  {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef mymodule = {
  PyModuleDef_HEAD_INIT,
  "my", /* name of module */
  NULL, /* module documentation */
  -1,   /* module keeps state in global variable */
  MyMethods
};

/*
  Essential for python module initialization
  PyObject * PyInit_modulename(void)
 */
PyMODINIT_FUNC
PyInit_my (void)
{
  return PyModule_Create (&mymodule);
}
