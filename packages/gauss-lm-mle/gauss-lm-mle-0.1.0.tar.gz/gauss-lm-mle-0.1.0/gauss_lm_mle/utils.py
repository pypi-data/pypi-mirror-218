import scipy.ndimage as ndi
import numpy as np


def find_spots(img, sigma=1.5, threshold=5.0):
    img = img.astype(float)
    gauss_laplace_img = -ndi.gaussian_laplace(img, sigma=sigma)
    maxfilt_img = ndi.maximum_filter(gauss_laplace_img, size=3)
    local_maxima = np.where(maxfilt_img == gauss_laplace_img)
    intensities = gauss_laplace_img[local_maxima]
    cond1 = intensities > threshold
    return (local_maxima[0][cond1], local_maxima[1][cond1])


def crop_boxes(yxlocs, img, boxsize=7):
    spots = []
    nlocs = len(yxlocs[0])
    s = boxsize // 2

    for n in range(nlocs):
        yc, xc = yxlocs[0][n], yxlocs[1][n]
        _box = img[yc - s : yc + s + 1, xc - s : xc + s + 1]
        spots.append(_box)
    return spots


def rot_gauss(pars, x, y):
    a, b, c, xc, yc, A, bg = pars
    arg = a * (x - xc) ** 2 + 2 * b * (x - xc) * (y - yc) + c * (y - yc) ** 2
    return A * np.exp(-arg) + bg


def parse_params(pars):
    a, b, c, xc, yc, A, bg = pars
    theta = 0.5 * np.arctan(2 * b / (a - c))
    sx = 1 / (
        2
        * (
            a * np.cos(theta) ** 2
            + 2 * b * np.cos(theta) * np.sin(theta)
            + c * np.sin(theta) ** 2
        )
    )
    sy = 1 / (
        2
        * (
            a * np.sin(theta) ** 2
            - 2 * b * np.cos(theta) * np.sin(theta)
            + c * np.cos(theta) ** 2
        )
    )
    return {
        "A": A,
        "bg": bg,
        "xc": xc,
        "yc": yc,
        "sx": sx,
        "sy": sy,
        "theta": np.rad2deg(theta),
    }


def objJ(pars, data, x, y):
    model = rot_gauss(pars, x, y)
    return (model - data).flatten()


def jac_objJ(pars, data, x, y):
    """6 x N matrix of partial derivatives"""
    a, b, c, xc, yc, A, bg = pars
    arg = a * (x - xc) ** 2 + 2 * b * (x - xc) * (y - yc) + c * (y - yc) ** 2
    jac = np.zeros((7, data.size))
    # partial derivative w.r.t a
    dA = np.exp(-arg)
    da = -A * (x - xc) ** 2 * np.exp(-arg)
    db = -A * (x - xc) * (y - yc) * np.exp(-arg)
    dc = -A * (y - yc) ** 2 * np.exp(-arg)
    dxc = 2 * A * a * (x - xc) * np.exp(-arg) + A * b * (y - yc) * np.exp(-arg)
    dyc = A * b * (x - xc) * np.exp(-arg) + 2 * A * c * (y - yc) * np.exp(-arg)

    jac[0] = da.flatten()
    jac[1] = db.flatten()
    jac[2] = dc.flatten()
    jac[3] = dxc.flatten()
    jac[4] = dyc.flatten()
    jac[5] = dA.flatten()
    jac[6] = 1.0

    return jac.T
