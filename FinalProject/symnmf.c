#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "symnmf.h"
#include "matrixmath.h"

double euclidean(double *x, double *y, int d) /* calulating the euclidean distance between two points */
{
    double sum = 0;
    int i;
    for(i = 0; i < d; i++){
        sum += (x[i] - y[i]) * (x[i] - y[i]);
    }
    sum = sqrt(sum);
    return sum;
}

double** sym(double** points, int N, int d) {
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
            else{ /* Calculate Gaussion RBF */
                distance = euclidean(points[i], points[j], d);
                symmetric[i][j] = exp(-(distance * distance)/2);
                
            }
        }
    }
    return symmetric;
}

double **ddg(double **points, int N, int d) /* calculating the degrees of the sym matrix */
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
    /* free memory */
    for(i = 0; i < N; i++){
        free(symmetric[i]);
    }
    free(symmetric);
    return diag;
}

double **norm(double **points, int N, int d) /* normalization is defined by: normMat = diag^(-1/2) * sym * diag^(-1/2) */
{
    double **symmetric, **diag, **normMat, **ddg_1_2, **tmp;
    int i;
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
        ddg_1_2[i][i] = 1/sqrt(diag[i][i]);
    }
    tmp = multiplyMatrix(ddg_1_2, N, N, symmetric, N, N);
    normMat = multiplyMatrix(tmp, N, N, ddg_1_2, N, N);
    /* free memory */
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

double** fullSymnmf(double **W, int N, int k, double** initMat, int max_iter, double eps) /* symnmf algorithm */
{
    int i, j, iter = 0;
    const double beta = 0.5;
    double **H, **next_H, **Ht, **WH, **HHt, **HHtH, **diff;
    H = initMat;
    diff = calloc(N, sizeof(double*));
    if(diff == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < N; i++){
        diff[i] = calloc(k, sizeof(double));
        if(diff[i] == NULL) {
            printf("An Error Has Occurred\n");
            exit(1);
        }
    }
    next_H = calloc(N, sizeof(double*));

    if(next_H == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < N; i++){
        next_H[i] = calloc(k, sizeof(double));
        if(next_H[i] == NULL) {
            printf("An Error Has Occurred\n");
            exit(1);
        }
    }
    while(iter < max_iter){
        Ht = transposeMatrix(H, N, k);
        WH = multiplyMatrix(W, N, N, H, N, k);
        HHt = multiplyMatrix(H, N, k, Ht, k, N);
        HHtH = multiplyMatrix(HHt, N, N, H, N, k);
        for(i = 0; i < N; i++){
            for(j = 0; j < k; j++){
                next_H[i][j] = H[i][j] * (1 - beta + beta * (WH[i][j]/HHtH[i][j]));
            }
        }
        for(i = 0; i < N; i++){
            for(j = 0; j < k; j++){
                diff[i][j] = next_H[i][j] - H[i][j];
            }
        }
        for(i = 0; i < N; i++){
            for(j = 0; j < k; j++){
                H[i][j] = next_H[i][j];
            }
        }
        if(frobNorm(diff, N, k) < eps){
            break;
        }
        /* free auxilary matrices */
        for(i = 0; i < N; i++){
            if(i < k){
                free(Ht[i]);
            }
            free(WH[i]);
            free(HHt[i]);
            free(HHtH[i]);
        }
        free(Ht);
        free(WH);
        free(HHt);
        free(HHtH);

        iter++;
    }
    for(i = 0; i < N; i++){
        free(diff[i]);
        free(next_H[i]);
    }
    free(diff);
    free(next_H);
    return H;



}

double** readDataPoints(char *filename, int *numPoints, int *dimension) /* reading the data points from the file */
{
    char *line = NULL, *token;
    size_t bufferSize = 60000;
    int i, j, commaCounter = 0, lineCounter = 0, length;
    double **points;
    FILE *file;
    file = fopen(filename, "r");
    if(file == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    line = malloc(bufferSize * sizeof(char));
    if(line == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }

    if(fgets(line, bufferSize, file) == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    length = strlen(line);
    for(i = 0; i < length; i++){
        if(line[i] == ','){
            commaCounter++;
        }
    }
    *dimension = commaCounter + 1;
    lineCounter++;

    while(fgets(line, bufferSize, file) != NULL){
        lineCounter++;
    }
    *numPoints = lineCounter;
    rewind(file);
    points = calloc(*numPoints, sizeof(double*));
    if(points == NULL) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < *numPoints; i++){
        points[i] = calloc(*dimension, sizeof(double));
        if(points[i] == NULL) {
            printf("An Error Has Occurred\n");
            exit(1);
        }
    }

    i = 0;
    while(fgets(line, bufferSize, file) != NULL){
        token = strtok(line, ",");
        j = 0;
        while(token != NULL){
            points[i][j] = atof(token);
            token = strtok(NULL, ",");
            j++;
        }
        i++;
    }
    fclose(file);
    free(line);
    return points;
    
}

int main(int argc, char **argv)
{
    char *goal, *filename;
    int numPoints = 0, dimension = 0, i, j;
    double **points, **res;

    if(argc != 3)
    {
        printf("An Error Has Occurred");
        exit(1);
    }

    goal = argv[1];
    filename = argv[2];
    points = readDataPoints(filename, &numPoints, &dimension);

    if(strcmp(goal, "sym") == 0){
        res = sym(points, numPoints, dimension);
    }
    else if(strcmp(goal, "ddg") == 0){
        res = ddg(points, numPoints, dimension);
    }
    else if(strcmp(goal, "norm") == 0){
        res = norm(points, numPoints, dimension);
    }
    else{
        printf("An Error Has Occurred\n");
        exit(1);
    }

    for(i = 0; i < numPoints; i++){
        for(j = 0; j < numPoints; j++){
            printf("%.4f", res[i][j]);
            if(j != numPoints - 1){
                printf(",");
            }
        }
        printf("\n");
    }

    for(i = 0; i < numPoints; i++){
        free(points[i]);
        free(res[i]);
    }
    free(points);
    free(res);
    return 0;
}
