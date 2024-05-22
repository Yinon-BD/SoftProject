#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "symnmf.h"
#include "matrixmath.h"

static PyObject* symnmf(PyObject *self, PyObject *args) {
    PyObject *PythonNormMatrix;
    PyObject *PythonInitial;
    int N, d, k, max_iter = 300;
    double **normMatrix, **initial, eps = 1e-4;
    double **result;
    if(!PyArg_ParseTuple(args, "OiiiO", &PythonNormMatrix, &N, &d, &k, &PythonInitial)) {
        return NULL;
    }
    normMatrix = calloc(N, sizeof(double*));
    if(normMatrix == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(int i=0; i<N; i++) {
        normMatrix[i] = calloc(N, sizeof(double));
        if(normMatrix[i] == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(int j=0; j<N; j++) {
            normMatrix[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(PythonNormMatrix, i), j));
        }
    }
    initial = calloc(N, sizeof(double*));
    if(initial == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(int i=0; i<N; i++) {
        initial[i] = calloc(k, sizeof(double));
        if(initial[i] == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(int j=0; j<k; j++) {
            initial[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(PythonInitial, i), j));
        }
    }
    result = fullSymnmf(normMatrix, N, k, initial, max_iter, eps);
    PyObject *PythonResult = PyList_New(N);
    if(PythonResult == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(int i=0; i<N; i++) {
        PyObject *PythonRow = PyList_New(k);
        if(PythonRow == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(int j=0; j<k; j++) {
            PyList_SET_ITEM(PythonRow, j, Py_BuildValue("d", result[i][j]));
        }
        PyList_SetItem(PythonResult, i, Py_BuildValue("O", PythonRow));
    }

    /* Free allocated memory */
    for(int i=0; i<N; i++) {
        free(normMatrix[i]);
        free(initial[i]);
    }
    free(normMatrix);
    free(initial);
    return PythonResult;
    
}

static PyObject* PySym(PyObject *self, PyObject *args) {
    PyObject *PythonPoints;
    double **points;
    int N, d, i, j;
    double **result;
    if(!PyArg_ParseTuple(args, "Oii", &PythonPoints, &N, &d)) {
        return NULL;
    }
    points = calloc(N, sizeof(double*));
    if(points == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(i=0; i<N; i++) {
        points[i] = calloc(d, sizeof(double));
        if(points[i] == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(j=0; j<d; j++) {
            points[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(PythonPoints, i), j));
        }
    }
    result = sym(points, N, d);
    PyObject *PythonResult = PyList_New(N);
    if(PythonResult == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(i=0; i<N; i++) {
        PyObject *PythonRow = PyList_New(N);
        if(PythonRow == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(j=0; j<N; j++) {
            PyList_SET_ITEM(PythonRow, j, Py_BuildValue("d", result[i][j]));
        }
        PyList_SetItem(PythonResult, i, Py_BuildValue("O", PythonRow));
    }

    /* Free allocated memory */
    for(i=0; i<N; i++) {
        free(points[i]);
    }
    free(points);
    return PythonResult;
}

static PyObject* PyDdg(PyObject *self, PyObject *args) {
    PyObject *PythonPoints;
    double **points;
    int N, d, i, j;
    double **result;
    if(!PyArg_ParseTuple(args, "Oii", &PythonPoints, &N, &d)) {
        return NULL;
    }
    points = calloc(N, sizeof(double*));
    if(points == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(i=0; i<N; i++) {
        points[i] = calloc(d, sizeof(double));
        if(points[i] == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(j=0; j<d; j++) {
            points[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(PythonPoints, i), j));
        }
    }
    result = ddg(points, N, d);
    PyObject *PythonResult = PyList_New(N);
    if(PythonResult == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(i=0; i<N; i++) {
        PyObject *PythonRow = PyList_New(N);
        if(PythonRow == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(j=0; j<N; j++) {
            PyList_SET_ITEM(PythonRow, j, Py_BuildValue("d", result[i][j]));
        }
        PyList_SetItem(PythonResult, i, Py_BuildValue("O", PythonRow));
    }

    /* Free allocated memory */
    for(i=0; i<N; i++) {
        free(points[i]);
    }
    free(points);
    return PythonResult;
}

static PyObject* PyNorm(PyObject *self, PyObject *args) {
    PyObject *PythonPoints;
    double **points;
    int N, d, i, j;
    double **result;
    if(!PyArg_ParseTuple(args, "Oii", &PythonPoints, &N, &d)) {
        return NULL;
    }
    points = calloc(N, sizeof(double*));
    if(points == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(i=0; i<N; i++) {
        points[i] = calloc(d, sizeof(double));
        if(points[i] == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(j=0; j<d; j++) {
            points[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(PythonPoints, i), j));
        }
    }
    result = norm(points, N, d);
    PyObject *PythonResult = PyList_New(N);
    if(PythonResult == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(i=0; i<N; i++) {
        PyObject *PythonRow = PyList_New(N);
        if(PythonRow == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(j=0; j<N; j++) {
            PyList_SET_ITEM(PythonRow, j, Py_BuildValue("d", result[i][j]));
        }
        PyList_SetItem(PythonResult, i, Py_BuildValue("O", PythonRow));
    }

    /* Free allocated memory */
    for(i=0; i<N; i++) {
        free(points[i]);
    }
    free(points);
    return PythonResult;
}

static PyMethodDef mysymnmf_methods[] = {
    {"symnmf", (PyCFunction) symnmf, METH_VARARGS, PyDoc_STR("The full NMF algorithm. \n\
    It return a matrix H such that (||W - HHt||_F)^2 is minimal.")},
    {"sym", (PyCFunction) PySym, METH_VARARGS, PyDoc_STR("Returns the similarity matrix of the given points.")},
    {"ddg", (PyCFunction) PyDdg, METH_VARARGS, PyDoc_STR("Returns the diagonal degree matrix of the given points.")},
    {"norm", (PyCFunction) PyNorm, METH_VARARGS, PyDoc_STR("Returns the normalized similarity matrix of the given points.")},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef mysymnmf_module = {
    PyModuleDef_HEAD_INIT,
    "mysymnmf",
    "The full NMF algorithm.",
    -1,
    mysymnmf_methods
};

PyMODINIT_FUNC PyInit_mysymnmf(void) {
    PyObject *m;
    m = PyModule_Create(&mysymnmf_module);
    if(!m) {
        return NULL;
    }
    return m;
}
