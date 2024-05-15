#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "cap.h"


static PyObject* fit(PyObject *self, PyObject *args) {
    PyObject *PythonVectors;
    PyObject *PythonCentroids;
    PyObject *PythonDP2C;
    PyObject *PythonResults;
    PyObject *PythonSingleResult;
    double **vectors;
    double **centroids;
    int *dp2c;
    int k, N, d, max_iter;
    double eps;
    double **result;
    if(!PyArg_ParseTuple(args, "OOOiiiid", &PythonVectors, &PythonCentroids, &PythonDP2C, &k, &N, &d, &max_iter, &eps)) {
        return NULL;
    }
    vectors = calloc(N, sizeof(double*));
    if(vectors == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(int i=0; i<N; i++) {
        vectors[i] = calloc(d, sizeof(double));
        if(vectors[i] == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(int j=0; j<d; j++) {
            vectors[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(PythonVectors, i), j));
        }
    }
    centroids = calloc(k, sizeof(double*));
    if(centroids == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(int i=0; i<k; i++) {
        centroids[i] = calloc(d, sizeof(double));
        if(centroids[i] == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(int j=0; j<d; j++) {
            centroids[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(PythonCentroids, i), j));
        }
    }
    dp2c = calloc(N, sizeof(int));
    if(dp2c == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(int i=0; i<N; i++) {
        dp2c[i] = PyLong_AsLong(PyList_GetItem(PythonDP2C, i));
    }
    result = getKmeans(vectors, centroids, dp2c, k, N, d, max_iter, eps);
    PythonResults = PyList_New(k);
    if(PythonResults == NULL) {
        printf("An Error Has Occurred\n");
        return NULL;
    }
    for(int i=0; i<k; i++) {
        PythonSingleResult = PyList_New(d);
        if(PythonSingleResult == NULL) {
            printf("An Error Has Occurred\n");
            return NULL;
        }
        for(int j=0; j<d; j++) {
            PyList_SET_ITEM(PythonSingleResult, j, Py_BuildValue("d", result[i][j]));
        }
        PyList_SetItem(PythonResults, i, Py_BuildValue("O", PythonSingleResult));
    }

    /* Freeing all alocated memory...*/
    for(int i=0; i<N; i++) {
        free(vectors[i]);
    }
    free(vectors);
    for(int i=0; i<k; i++) {
        free(centroids[i]);
    }
    free(centroids);
    free(dp2c);
    return PythonResults;

}

static PyMethodDef mykmeanssp_methods[] = {
    {"fit", (PyCFunction) fit, METH_VARARGS, PyDoc_STR("The fit function of the kmeans algorithm.\n\
    It gets 8 arguments: vectors, centroids, dp2c, k, N, d, max_iter, eps. It returns a list of the new centroids.\n\
    vectors - a list of lists of the vectors to be clustered\n\
    centroids - a list of lists of the initial centroids\n\
    dp2c - a list of the initial assignment of the vectors to the centroids\n\
    k - the number of clusters\n\
    N - the number of vectors\n\
    d - the number of dimensions of the vectors\n\
    max_iter - the maximum number of iterations\n\
    eps - the minimum change in the centroids to indicate convergence\n")},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cap_module = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp",
    "Kmeans algorithm",
    -1,
    mykmeanssp_methods
};

PyMODINIT_FUNC PyInit_mykmeanssp(void) {
    PyObject *m;
    m = PyModule_Create(&cap_module);
    if(!m) {
        return NULL;
    }
    return m;
}

