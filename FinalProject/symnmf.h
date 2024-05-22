# ifndef SYM_NMF_H
# define SYM_NMF_H

double euclidean(double *x, double *y, int d);
double** sym(double** points, int N, int d);
double** ddg(double **points, int N, int d);
double** norm(double **points, int N, int d);
double** fullSymnmf(double **W, int N, int k, double** initMat, int max_iter, double eps);
double** readDataPoints(char *filename, int *numPoints, int *dimension);

# endif