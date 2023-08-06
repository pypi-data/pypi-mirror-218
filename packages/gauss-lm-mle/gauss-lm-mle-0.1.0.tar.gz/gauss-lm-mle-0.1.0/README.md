# gauss_lm_mle

Python wrapper around small C library from https://pubmed.ncbi.nlm.nih.gov/20431544/ (Laurence & Chromy, 2010).

# Example

```

import tifffile
import gauss_lm_mle

import matplotlib.pyplot as plt

# read tiff file and use the first frame only
img = tifffile.imread("tests/test_data.tif")[0]
yxlocs = gauss_lm_mle.utils.find_spots(img, sigma=1.5, threshold=6.0)

# do spot check
plt.imshow(img)
plt.plot(yxlocs[1], yxlocs[0], 'r+')
plt.show()

# do fitting
boxsize = 11
max_iter = 200
fitres = gauss_lm_mle.mle_rotated_gaussian(img, yxlocs, boxsize, max_iter)

# `fitres` should be a DataFrame of the fitted coordinates

```

The returned DataFrame `fitres` returned by `mle_rotated_gaussian()`:
```
pd.DataFrame
        A DataFrame containing the MLE fitting results. Each row corresponds to one peak, and the columns are:
        'A' - Amplitude of the Gaussian.
        'bg' - Background offset.
        'x' and 'y' - Coordinates of the Gaussian's peak.
        'sx' and 'sy' - Standard deviations of the Gaussian along the x and y axes, respectively.
        'theta' - Rotation angle of the Gaussian (in radians).
        'asymmetry' - Asymmetry parameter of the Gaussian.
        'niter' - The number of iterations performed by the fitting algorithm.
        'norm2_error' - The squared error norm of the fit.
```


