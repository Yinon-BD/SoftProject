#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int isNatural(char* str) {
    int i=0;
    for(; str[i] != 0; i++) {
        if(str[i] < '0' || str[i] > '9') {
            return 0;
        }
    }
    return 1;

}

double calcDist(double x[], double centroid[], int d){
    double sum = 0;
    int i=0;
    for (i=0; i<d; i++){
        sum += (x[i]-centroid[i])*(x[i]-centroid[i]);
    }
    sum = sqrt(sum);
    return sum;
}


int main(int argc, char **argv)
{
    int K, givenN, d, iter;
    double epsilon = 0.001;

    int counter=0;
    int x;
    char delim;
    double number=0;
    int i=0, j=0, k=0, l=0;
    int N;
    int convCount = 0;
    double **newCentroidsMeans;
    double **centroidsMean;
    double **dps;
    int *howManyInCen;
    int *dp2c;
    if(argc < 4 || argc > 5) {
        fprintf(stderr, "An Error Has Occurred\n");
        exit(1);
    }
    if (argc == 4){
        iter = 200;
    }
    else {
        iter = (int)strtol(argv[4], NULL, 10);
        if( !isNatural(argv[4])) {
            fprintf(stderr, "Invalid maximum iteration!\n");
            exit(1);
        }
    }
    /* Error Typing Handling */
    if( !isNatural(argv[1])) {
        fprintf(stderr, "Invalid number of clusters!\n");
        exit(1);
    }
    K = (int)strtol(argv[1], NULL, 10);
    if( !isNatural(argv[2])) {
        fprintf(stderr, "Invalid number of points!\n");
        exit(1);
    }
    givenN = (int)strtol(argv[2], NULL, 10);

    if( !isNatural(argv[3])) {
        fprintf(stderr, "Invalid dimension of point!\n");
        exit(1);
    }
    d = (int)strtol(argv[3], NULL, 10);

    /*  Error Value Handling... */
    if(K <= 1 || K >= givenN) {
        fprintf(stderr, "Invalid number of clusters!\n");
        exit(1);
    }
    if(givenN <= 1) {
        fprintf(stderr, "Invalid number of points!\n");
        exit(1);
    }
    if(iter <= 1 || iter >= 1000) {
        fprintf(stderr, "Invalid maximum iteration!\n");
        exit(1);
    }

    dps = calloc(givenN, sizeof(double*));
    if(dps == NULL) {
        fprintf(stderr, "An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < givenN; i++){
        dps[i] = calloc(d, sizeof(double));
        if(dps[i] == NULL) {
            fprintf(stderr, "An Error Has Occurred\n");
            exit(1);
        }
    }

    for (i=0; i<givenN; i++){
        for (j=0; j<d; j++) {
            x = scanf("%lf%c", &number, &delim);
            if(x != 2) {
                fprintf(stderr, "An Error Has Occurred\n");
                exit(1);
            }
            dps[i][j] = number;
            if (x == -1) {
                break;
            }
        }
        if (x == -1){
            break;
        }
        counter++;
    }
    if (counter < givenN){
        N = counter;
        dps = realloc(dps, sizeof(double*) * N);
        if(dps == NULL) {
            fprintf(stderr, "An Error Has Occurred\n");
            exit(1);
        }
    }
    else{
        N = givenN;
    }

    newCentroidsMeans = calloc(K, sizeof(double*));
    if(newCentroidsMeans == NULL) {
        fprintf(stderr, "An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < K; i++){
        newCentroidsMeans[i] = calloc(d, sizeof(double));
        if(newCentroidsMeans[i] == NULL) {
            fprintf(stderr, "An Error Has Occurred\n");
            exit(1);
        }
    }

    centroidsMean = calloc(K, sizeof(double*));
    if(centroidsMean == NULL) {
        fprintf(stderr, "An Error Has Occurred\n");
        exit(1);
    }
    for(i = 0; i < K; i++){
        centroidsMean[i] = calloc(d, sizeof(double));
        if(centroidsMean[i] == NULL) {
            fprintf(stderr, "An Error Has Occurred\n");
            exit(1);
        }
    }

    howManyInCen = calloc(K, sizeof(int));
    if(howManyInCen == NULL) {
        fprintf(stderr, "An Error Has Occurred\n");
        exit(1);
    }

    dp2c = calloc(N, sizeof(int));
    if(dp2c == NULL) {
        fprintf(stderr, "An Error Has Occurred\n");
        exit(1);
    }

    for (i=0; i<N; i++){
        dp2c[i] = -1;
    }

    for (i=0; i<K; i++){
        dp2c[i] = i;
        howManyInCen[i] = 1;
        for (j=0; j<d; j++){
            centroidsMean[i][j] = dps[i][j];
        }
    }

    for (i=0; i<iter; i++){

        for (j=0; j<N; j++){

            double minVal=calcDist(dps[j], centroidsMean[0], d);
            int minIdx=0;

            for (k=1; k<K; k++){
                double dist = calcDist(dps[j], centroidsMean[k], d);
                if (dist <= minVal){
                    minVal = dist;
                    minIdx = k;
                }
            }

            if (minIdx != dp2c[j]){
                if (dp2c[j] != -1){
                    howManyInCen[dp2c[j]]--;
                }
                howManyInCen[minIdx]++;
                dp2c[j] = minIdx;
            }

        }

        for (k=0; k<K; k++){
            for (l=0; l<d; l++){
                newCentroidsMeans[k][l] = 0;
          }
        }

        for (j=0; j<N; j++){
            for (l=0; l<d; l++){
                newCentroidsMeans[dp2c[j]][l] += dps[j][l];
            }
        }

        for (k=0; k<K; k++){
            for (l=0; l<d; l++){
                newCentroidsMeans[k][l] = newCentroidsMeans[k][l] / howManyInCen[k];
            }
        }

        convCount = 0;

        for (k=0; k<K; k++){
            double dist = calcDist(newCentroidsMeans[k], centroidsMean[k], d);
            if (dist < epsilon){
                convCount++;
            }
        }
        if (convCount == k){
            break;
        }
        for (k=0; k<K; k++){
            for (l=0; l<d; l++){
                centroidsMean[k][l] = newCentroidsMeans[k][l];
            }
        }
    }
    delim = ',';
    for (k=0; k<K; k++){
        for (l=0; l<d; l++){
            if (l == d-1){
                delim = '\0';
            }
            printf("%.4f%c", centroidsMean[k][l], delim);
            delim = ',';
        }
        printf("\n");
    }

    /* freeing all allocated memory: */
    for (i=0; i<K; i++){
        free(newCentroidsMeans[i]);
    }
    free(newCentroidsMeans);

    for (i = 0; i < K; i++){
        free(centroidsMean[i]);
    }
    free(centroidsMean);

    for (i = 0; i < N; i++){
        free(dps[i]);
    }
    free(dps);

    free(howManyInCen);

    free(dp2c);

    return 0;
}
