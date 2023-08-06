#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "levmar_mle.h"
#include "gfit.h"


// define rotated gaussian function
// m, number of parameters
// n, number of data points
// pass pointer to coord_data struct which contains vectorized mesh coordinates
// of x,y coordinates
void rotated_gaussian_f(double* p, double* f, int m, int n, void* adata) {
  // given parameters p, store result in f
  double a, b, c, xc, yc, A, bg;
  double xarg, yarg;
  double wrk;
  // cast adata back into coord_data struct
  coord_data* coord = (coord_data*) adata;

  // assign parameters into more meaningful name
  a	= p[0];
  b	= p[1];
  c	= p[2];
  xc	= p[3];
  yc	= p[4];
  A	= p[5];
  bg	= p[6];

  for (int i=0; i<n; i++) {
    xarg = coord->x[i] - xc;
    yarg = coord->y[i] - yc;
    wrk = a*xarg*xarg + 2*b*xarg*yarg + c* yarg*yarg;
    f[i] = A * exp(-wrk) + bg;
  }
}

// jacobian for rotated gaussian function
void rotated_gaussian_df(double* p, double* jac, int m, int n, void* adata) {
  // given parameters p, store result in f
  double a, b, c, xc, yc, A;
  double xarg, yarg;
  double wrk;
  // cast adata back into coord_data struct
  coord_data* coord = (coord_data*) adata;
    
  // assign parameters into more meaningful name
  a	= p[0];
  b	= p[1];
  c	= p[2];
  xc	= p[3];
  yc	= p[4];
  A	= p[5];

  // there are m number of parameters (7 in our case)
  // we populate the n x m jacobian matrix
  for (int i = 0; i < n; i++) {
    xarg = coord->x[i] - xc;
    yarg = coord->y[i] - yc;
    wrk = a*xarg*xarg + 2*b*xarg*yarg + c*yarg*yarg;
    
    // partial a
    jac[i * m] = -A * xarg * xarg * exp(-wrk);
    // partial b
    jac[i * m + 1] = -2 * A * xarg * yarg * exp(-wrk);
    // partial c
    jac[i * m + 2] = -A * yarg * yarg * exp(-wrk);
    // partial xc
    jac[i * m + 3] = A * (2*a*xarg + 2*b*yarg) * exp(-wrk);
    // partial yc
    jac[i * m + 4] = A * (2*b*xarg + 2*c*yarg) * exp(-wrk);
    // partial A
    jac[i * m + 5] = exp(-wrk);
    // partial bg
    jac[i * m + 6] = 1.0;
  }
    
}

void gaussian_f(double* p, double* f, int m, int n, void* adata) {
  double xc, yc, sigma, A, bg;
  double xarg, yarg, wrk;

  // 'adata' will be a pointer to coord_data
  // cast to a pointer to `coord_data` to access the struct
  coord_data* coord = (coord_data*) adata;
  xc	= p[0];
  yc	= p[1];
  sigma = p[2];
  A	= p[3];
  bg	= p[4];

  double sigma2 = sigma * sigma;
  
  for (int i=0; i<n; i++) {
    xarg = coord->x[i] - xc;
    yarg = coord->y[i] - yc;
    wrk = (xarg*xarg)/(2*sigma2) + (yarg*yarg)/(2*sigma2);
    f[i] = A * exp(-wrk) + bg;
  }
}

// jacobian for symmetric gaussian function
void gaussian_df(double* p, double* jac, int m, int n, void* adata) {
  double xc, yc, sigma, A;
  double xarg, yarg, wrk;
  coord_data* coord = (coord_data*) adata;
  xc	= p[0];
  yc	= p[1];
  sigma = p[2];
  A	= p[3];

  double sigma2 = sigma * sigma;
  double sigma3 = sigma2 * sigma;
  
  for (int i=0; i<n; i++) {
    xarg = coord->x[i] - xc;
    yarg = coord->y[i] - yc;
    wrk  = (xarg*xarg)/(2*sigma2) + (yarg*yarg)/(2*sigma2);

    //partial xc
    jac[i * m] = A * xarg * exp(-wrk) / sigma2;
    //partial yc
    jac[i * m + 1] = A * yarg * exp(-wrk) / sigma2;
    //partial sigma
    jac[i * m + 2] = A * exp(-wrk) * ((xarg*xarg)/sigma3 + (yarg*yarg)/sigma3);
    //partial A
    jac[i * m + 3] = exp(-wrk);
    //partial bg
    jac[i * m + 4] = 1.0;
  }
  
}


/*
  Function definition for LM minimizer

  int dlevmar_mle_der(
  void (*func)(double *p, double *hx, int m, int n, void *adata),
  void (*jacf)(double *p, double *j, int m, int n, void *adata),
  double *p, double *x, int m, int n, int itmax, double *opts,
  double *info, double *work, double *covar, void *adata, int fitType);

  double compute_chisq_measure(double *e, double *x, double *hx, int n, int fitType);
*/

/*
  Function for debugging / learning writing C function for calling from Python
  using `ctypes` module
*/
void print_rois(
		double* image, int* ylocs, int *xlocs, 
		int img_height, int img_width, int nlocs, int boxsize
		) 
{
  // This function should extract the region of interest
  // from the image using the x, y coordinate and the box size.
  int s = boxsize / 2;

  // allocate working array for ROI
  double* roi = malloc(boxsize * boxsize * sizeof(double));

  for (int i = 0; i < nlocs; i++) {
    int xc = xlocs[i];
    int yc = ylocs[i];

    if (xc - s < 0 || xc + s >= img_width || yc - s < 0 || yc + s >= img_height) {
      printf("ROI %d is out of boundaries.\n", i);
      continue;
    }

    // copy pixels of ROI into 'roi'
    for (int i = -s; i <= s; i++) {
      for (int j= -s; j <= s; j++) {
	roi[(i + s) * boxsize + (j + s)] = image[(yc + i) * img_width + (xc + j)];
      }
    }

    // for debugging, print out 'roi' value row-by-row
    printf("ROI %d @ (%d, %d): \n", i, yc, xc);
    for (int i=0; i<boxsize; i++) {
      for (int j=0; j<boxsize; j++) {
	printf("%6.0f|", roi[i * boxsize + j]);
      }
      printf("\n");
    }

  }

  // free memory
  free(roi);

}

coord_data meshgrid2d(int boxsize) {
  int s = boxsize / 2;
  int coord_size = boxsize * boxsize;

  coord_data data;
  data.x = malloc(sizeof(double) * coord_size);
  data.y = malloc(sizeof(double) * coord_size);
  data.num_coords = coord_size;

  for (int i = 0; i < boxsize; i++) {
    for (int j = 0; j < boxsize; j++) {
      data.x[i * boxsize + j] = j - s;
      data.y[i * boxsize + j] = i - s;
    }
  }

  return data;
}

void free_coord_data(coord_data* data) {
  free(data->x);
  free(data->y);
}

void free_results(double* results) {
  free(results);
}


void fit_rotated_gaussian(
	       double* image, int* ylocs, int *xlocs, 
	       int img_height, int img_width, int nlocs, int boxsize, int itermax,
	       double* results
	       ) 
{
  /*
    Perform Gaussian fitting to localize to single-molecule intensities
    using MLE.

   */
  double roi_min_val, roi_max_val, pixval;

  double sigma0 = 1.4;
  
  int s = boxsize / 2;
  
  double* roi = malloc(boxsize * boxsize * sizeof(double));

  int npars = 7;
  int nresults = 10;
  int ndata = boxsize * boxsize;

  // define box coordinates
  coord_data coords = meshgrid2d(boxsize);
  
  // loop through each maxima
  for (int n=0; n < nlocs; n++) {
    // extract ROI from image
    int yc = ylocs[n];
    int xc = xlocs[n];
    
    // copy pixels of ROI into 'roi'
    for (int i = -s; i <= s; i++) {
      for (int j= -s; j <= s; j++) {
	pixval = image[(yc + i) * img_width + (xc + j)];
	roi[(i + s) * boxsize + (j + s)] = pixval;
      }
    }

    // compute initial estimates
    // Amplitude and background is initially max(roi) and min(roi)
    roi_min_val = roi[0];
    roi_max_val = roi[0];

    for (int i = 0; i < boxsize; i++) {
      for (int j= 0; j < boxsize; j++) {
	pixval = roi[i * boxsize + j];
	if (pixval < roi_min_val) roi_min_val = pixval;
	if (pixval > roi_max_val) roi_max_val = pixval;
      }
    }

    double weight = 0.0;
    double weighted_sum_x = 0.0;
    double weighted_sum_y = 0.0;
    // compute first moment to estimate x,y position
    for (int i = 0; i < coords.num_coords; i++) {
      weight += (roi[i] - roi_min_val);
      weighted_sum_x += coords.x[i] * (roi[i] - roi_min_val);
      weighted_sum_y += coords.y[i] * (roi[i] - roi_min_val);
    }
    double xc0 = weighted_sum_x / weight;
    double yc0 = weighted_sum_y / weight;

    // scale parameters a, b, c
    double a0 = 1 / (2 * sigma0 * sigma0);
    double c0 = 1 / (2 * sigma0 * sigma0);
    
    // at the moment start with the same parameters for all
    // todo: get better estimate with first/second moments
    double pars[7] = {a0, 1e-4, c0, xc0, yc0, roi_max_val - roi_min_val, roi_min_val};
    double info[LM_INFO_SZ];

    dlevmar_mle_der(&rotated_gaussian_f, &rotated_gaussian_df,
		    pars, roi, npars, ndata, itermax, NULL, info,
		    NULL, NULL, &coords, 0);

    // printf("Peak fit #%d ==> A,%.2f \t bg,%.2f\n", n, pars[5], pars[6]);
    /* printf("x0,y0 @ #%d ==> %.3f, %.3f\n", n, xc0, yc0); */

    // theta = 0.5 * arctan( 2b / (a - c) )  
    double theta = 0.5 * atan((2 * pars[1]) / (pars[0] - pars[2]));
    double cos2theta = cos(theta)*cos(theta);
    double sin2theta = sin(theta)*sin(theta);
    double xtermtheta = cos(theta)*sin(theta);
    double sigma_x = 1/(2*(pars[0]*cos2theta + 2*pars[1]*xtermtheta + pars[2]*sin2theta));
    double sigma_y = 1/(2*(pars[0]*sin2theta + 2*pars[1]*xtermtheta + pars[2]*cos2theta));
    // populate results
    // A, bg, xc, yc, sigma_x, sigma_y, theta, asymm; niter, 
    results[n * nresults] = pars[5]; // Amplitude
    results[n * nresults + 1] = pars[6]; // background
    results[n * nresults + 2] = (double) xc + pars[3]; // xc
    results[n * nresults + 3] = (double) yc + pars[4]; // yc
    results[n * nresults + 4] = sigma_x; // sigma_x
    results[n * nresults + 5] = sigma_y; // sigma_y
    results[n * nresults + 6] = theta;
    // asymmetry ratio; >= 1
    results[n * nresults + 7] = (sigma_x >= sigma_y) ? (sigma_x / sigma_y) : (sigma_y / sigma_x);
    // diagnostic values
    results[n * nresults + 8] = info[5]; // number of iterations
    results[n * nresults + 9] = info[1]; // norm2 of error
    
  }

  free(roi);
  free_coord_data(&coords);
  
}


void fit_gaussian(
		   double* image, int* ylocs, int *xlocs, 
		   int img_height, int img_width, int nlocs, int boxsize, int itermax,
		   double* results
		   ) 
{
  /*
    Perform Gaussian fitting to localize to single-molecule intensities
    using MLE.

   */
  double roi_min_val, roi_max_val, pixval;

  double sigma0 = 1.4;
  
  int s = boxsize / 2;
  
  double* roi = malloc(boxsize * boxsize * sizeof(double));

  int npars = 5;
  int nresults = 7;
  int ndata = boxsize * boxsize;

  // define box coordinates
  coord_data coords = meshgrid2d(boxsize);
  
  // loop through each maxima
  for (int n=0; n < nlocs; n++) {
    // extract ROI from image
    int yc = ylocs[n];
    int xc = xlocs[n];
    
    // copy pixels of ROI into 'roi'
    for (int i = -s; i <= s; i++) {
      for (int j= -s; j <= s; j++) {
	pixval = image[(yc + i) * img_width + (xc + j)];
	roi[(i + s) * boxsize + (j + s)] = pixval;
      }
    }

    // compute initial estimates
    // Amplitude and background is initially max(roi) and min(roi)
    roi_min_val = roi[0];
    roi_max_val = roi[0];

    for (int i = 0; i < boxsize; i++) {
      for (int j= 0; j < boxsize; j++) {
	pixval = roi[i * boxsize + j];
	if (pixval < roi_min_val) roi_min_val = pixval;
	if (pixval > roi_max_val) roi_max_val = pixval;
      }
    }

    double weight = 0.0;
    double weighted_sum_x = 0.0;
    double weighted_sum_y = 0.0;
    // compute first moment to estimate x,y position
    for (int i = 0; i < coords.num_coords; i++) {
      weight += (roi[i] - roi_min_val);
      weighted_sum_x += coords.x[i] * (roi[i] - roi_min_val);
      weighted_sum_y += coords.y[i] * (roi[i] - roi_min_val);
    }
    double xc0 = weighted_sum_x / weight;
    double yc0 = weighted_sum_y / weight;

    // at the moment start with the same parameters for all
    double pars[5] = {xc0, yc0, sigma0, roi_max_val - roi_min_val, roi_min_val};
    double info[LM_INFO_SZ];

    dlevmar_mle_der(&gaussian_f, &gaussian_df,
		    pars, roi, npars, ndata, itermax, NULL, info,
		    NULL, NULL, &coords, 0);

    // populate results
    // A, bg, xc, yc, sigma_x, sigma_y, theta, asymm; niter, 
    results[n * nresults] = pars[3]; // Amplitude
    results[n * nresults + 1] = pars[4]; // background
    results[n * nresults + 2] = (double) xc + pars[0]; // xc
    results[n * nresults + 3] = (double) yc + pars[1]; // yc
    results[n * nresults + 4] = pars[2]; // sigma
    results[n * nresults + 5] = info[5]; // niter
    results[n * nresults + 6] = info[1]; // norm2 of error
   
  }

  free(roi);
  free_coord_data(&coords);
  
}

