import numpy as np
import pandas as pd
from .liblm_mle_de import load_library


lib = load_library()


def mle_rotated_gaussian(
    image: np.ndarray,
    yxlocs: tuple,
    boxsize: int,
    itermax: int,
) -> pd.DataFrame:
    """
    Perform maximum likelihood estimation (MLE) fitting of a rotated Gaussian function on an image.

    The function calls a C library function that performs the MLE fitting, and returns the results in a pandas DataFrame.

    Parameters
    ----------
    image : np.ndarray
        The image data as a 2D numpy array.
    yxlocs : tuple of np.ndarray
        A tuple of two 1D numpy arrays containing the y and x coordinates of the peaks to fit, respectively.
    boxsize : int
        The size of the box to extract around each peak for fitting.
    itermax : int
        The maximum number of iterations for the MLE fitting algorithm.

    Returns
    -------
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
    """

    image = np.ascontiguousarray(image.astype(np.double))
    ylocs = np.ascontiguousarray(yxlocs[0].astype(np.intc))
    xlocs = np.ascontiguousarray(yxlocs[1].astype(np.intc))
    npeaks = len(ylocs)

    # preallocate results
    fitres = np.empty((npeaks, 10), dtype=np.double)

    # call C library
    lib.fit_rotated_gaussian(
        image,
        ylocs,
        xlocs,
        image.shape[0],
        image.shape[1],
        npeaks,
        boxsize,
        itermax,
        fitres,
    )

    dfres = pd.DataFrame(
        fitres,
        columns=[
            "A",
            "bg",
            "x",
            "y",
            "sx",
            "sy",
            "theta",
            "asymmetry",
            "niter",
            "norm2_error",
        ],
    )

    dfres["niter"] = dfres["niter"].astype(int)

    return dfres


def mle_gaussian(
    image: np.ndarray,
    yxlocs: tuple,
    boxsize: int,
    itermax: int,
) -> pd.DataFrame:
    """
    Perform maximum likelihood estimation (MLE) fitting of a Gaussian function on an image.

    The function calls a C library function that performs the MLE fitting, and returns the results in a pandas DataFrame.

    Parameters
    ----------
    image : np.ndarray
        The image data as a 2D numpy array.
    yxlocs : tuple of np.ndarray
        A tuple of two 1D numpy arrays containing the y and x coordinates of the peaks to fit, respectively.
    boxsize : int
        The size of the box to extract around each peak for fitting.
    itermax : int
        The maximum number of iterations for the MLE fitting algorithm.

    Returns
    -------
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
    """

    image = np.ascontiguousarray(image.astype(np.double))
    ylocs = np.ascontiguousarray(yxlocs[0].astype(np.intc))
    xlocs = np.ascontiguousarray(yxlocs[1].astype(np.intc))
    npeaks = len(ylocs)

    # preallocate results
    fitres = np.empty((npeaks, 7), dtype=np.double)

    # call C library
    lib.fit_gaussian(
        image,
        ylocs,
        xlocs,
        image.shape[0],
        image.shape[1],
        npeaks,
        boxsize,
        itermax,
        fitres,
    )

    dfres = pd.DataFrame(
        fitres,
        columns=[
            "A",
            "bg",
            "x",
            "y",
            "sigma",
            "niter",
            "norm2_error",
        ],
    )

    dfres["niter"] = dfres["niter"].astype(int)

    return dfres
