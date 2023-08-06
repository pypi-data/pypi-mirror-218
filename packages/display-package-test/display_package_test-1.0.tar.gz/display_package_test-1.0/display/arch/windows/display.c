#include <Python.h>
#include <windows.h>

static PyObject * resolution(PyObject* self, PyObject* args) {
    int x = GetSystemMetrics(SM_CXSCREEN);
    int y = GetSystemMetrics(SM_CYSCREEN);

    return Py_BuildValue("ii", x, y);
}

static PyMethodDef display_methods[] = {
    {"resolution", get_screen_resolution, METH_NOARGS, "Get the screen resolution"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef display_module = {
    PyModuleDef_HEAD_INIT,
    "display",
    NULL,
    -1,
    display_methods
};

PyMODINIT_FUNC PyInit_display(void) {
    return PyModule_Create(&display_module);
}
