#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "matrixmath.h"

double **multiplyMatrix(double **matrix1, int row1, int col1, double **matrix2, int row2, int col2) /* multiplying two matrices */
{
    double **result;
    int i, j, k;
    if(col1 != row2){
        printf("An Error Has Occurred\n");
        exit(1);
    }
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

double **transposeMatrix(double **matrix, int row, int col) /* transposing a matrix */
{
    double **result;
    int i, j;
    result = calloc(col, sizeof(double*));
    if(result == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < col; i++){
        result[i] = calloc(row, sizeof(double));
        if(result[i] == NULL) {
            printf("An Error Has Occurred\n");
            exit(1);
        }
    }
    for(i = 0; i < row; i++){
        for(j = 0; j < col; j++){
            result[j][i] = matrix[i][j];
        }
    }
    return result;
}

double frobNorm(double **matrix, int row, int col) /* calculating the Frobenius norm of a matrix */
{
    double sum = 0;
    int i, j;
    for(i = 0; i < row; i++){
        for(j = 0; j < col; j++){
            sum += matrix[i][j] * matrix[i][j];
        }
    }
    sum = sqrt(sum);
    return sum;
}