#ifndef GFIT_H
#define GFIT_H

typedef struct {
    double* x;
    double* y;
    int num_coords;
} coord_data;

coord_data meshgrid2d(int boxsize);

void free_coord_data(coord_data* data);

void rotated_gaussian_f(double* p, double* f, int m, int n, void* adata);

void rotated_gaussian_df(double* p, double* jac, int m, int n, void* adata);

void print_rois(double* image, int* ylocs, int *xlocs, int img_height,
		int img_width, int nlocs, int boxsize);

void fit_peaks(double* image, int* ylocs, int *xlocs, int img_height,
	       int img_width, int nlocs, int boxsize, int itermax,
	       double* results);

#endif // GFIT_H
