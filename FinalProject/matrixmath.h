# ifndef MATRIXMATH_H
# define MATRIXMATH_H

double** multiplyMatrix(double **matrix1, int row1, int col1, double **matrix2, int row2, int col2);
double **transposeMatrix(double **matrix, int row, int col);
double frobNorm(double **matrix, int row, int col);

# endif