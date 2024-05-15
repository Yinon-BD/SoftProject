#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "symnmf.h"

double euclidean(double *x, double *y, int d) //calulating the euclidean distance between two points
{
    double sum = 0;
    int i;
    for(i = 0; i < d; i++){
        sum += (x[i] - y[i]) * (x[i] - y[i]);
    }
    sum = sqrt(sum);
    return sum;
}

double **multiplyMatrix(double **matrix1, int row1, int col1, double **matrix2, int row2, int col2) // multiplying two matrices
{
    double **result;
    int i, j, k;
    result = calloc(row1, sizeof(double*));
    if(result == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < row1; i++){
        result[i] = calloc(col2, sizeof(double));
        if(result[i] == NULL) {
            printf("An Error Has Occurred\n");
            exit(1);
        }
    }
    for(i = 0; i < row1; i++){
        for(j = 0; j < col2; j++){
            result[i][j] = 0;
            for(k = 0; k < col1; k++){
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
    return result;
}

double** sym(double** points, int N, int d)
{
    double **symmetric, distance;
    int i, j;
    symmetric = calloc(N, sizeof(double*));
    if(symmetric == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < N; i++){
        symmetric[i] = calloc(N, sizeof(double));
        if(symmetric[i] == NULL) {
            printf("An Error Has Occurred\n");
            exit(1);
        }
    }
    for(i = 0; i < N; i++){
        for(j = 0; j < N; j++){
            if(i == j){
                symmetric[i][j] = 0;
            }
            else{ // Calculate Gaussion RBF
                distance = euclidean(points[i], points[j], d);
                symmetric[i][j] = exp(-(distance * distance)/2);
                
        }
    }
    }
    return symmetric;
}

double **ddg(double **points, int N, int d) // calculating the degrees of the sym matrix
{
    double **symmetric, **diag, sum;
    int i, j;
    symmetric = sym(points, N, d);
    diag = calloc(N, sizeof(double*));
    if(diag == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < N; i++){
        diag[i] = calloc(N, sizeof(double));
        if(diag[i] == NULL) {
            printf("An Error Has Occurred\n");
            exit(1);
        }
    }
    for(i = 0; i < N; i++){
        sum = 0;
        for(j = 0; j < N; j++){
            sum += symmetric[i][j];
        }
        diag[i][i] = sum;
    }
    // free memory
    for(i = 0; i < N; i++){
        free(symmetric[i]);
    }
    free(symmetric);
    return diag;
}

double **norm(double **points, int N, int d) // normalization is defined by: normMat = diag^(-1/2) * sym * diag^(-1/2)
{
    double **symmetric, **diag, **normMat, **ddg_1_2, **tmp, sum;
    int i, j;
    symmetric = sym(points, N, d);
    diag = ddg(points, N, d);
    ddg_1_2 = calloc(N, sizeof(double*));
    if(ddg_1_2 == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < N; i++){
        ddg_1_2[i] = calloc(N, sizeof(double));
        if(ddg_1_2[i] == NULL) {
            printf("An Error Has Occurred\n");
            exit(1);
        }
    }
    for(i = 0; i < N; i++){
        ddg_1_2[i][i] = 1/sqrt(ddg[i][i]);
    }
    tmp = multiplyMatrix(ddg_1_2, N, N, symmetric, N, N);
    normMat = multiplyMatrix(tmp, N, N, ddg_1_2, N, N);
    // free memory
    for(i = 0; i < N; i++){
        free(ddg_1_2[i]);
        free(tmp[i]);
        free(diag[i]);
        free(symmetric[i]);
    }
    free(ddg_1_2);
    free(tmp);
    free(diag);
    free(symmetric);
    
    return normMat;
}