"""
 RALIGN - Rigid alignment of two sets of points in k-dimensional
          Euclidean space.  Given two sets of points in
          correspondence, this function computes the scaling,
          rotation, and translation that define the transform TR
          that minimizes the sum of squared errors between TR(X)
          and its corresponding points in Y.  This routine takes
          O(n k^3)-time.

 Inputs:
   X - a k x n matrix whose columns are points
   Y - a k x n matrix whose columns are points that correspond to
       the points in X
 Outputs:
   c, R, t - the scaling, rotation matrix, and translation vector
             defining the linear map TR as

                       TR(x) = c * R * x + t

             such that the average norm of TR(X(:, i) - Y(:, i))
             is minimized.
"""
import copy

"""
Copyright: Carlo Nicolini, 2013
Code adapted from the Mark Paskin Matlab version
from http://openslam.informatik.uni-freiburg.de/data/svn/tjtf/trunk/matlab/ralign.m 
"""

import numpy as np


import numpy as np

# Input: expects 3xN matrix of points
# Returns R,t
# R = 3x3 rotation matrix
# t = 3x1 column vector

def rigid_transform_3D(A, B):
    assert A.shape == B.shape

    num_rows, num_cols = A.shape
    if num_rows != 3:
        raise Exception(f"matrix A is not 3xN, it is {num_rows}x{num_cols}")

    num_rows, num_cols = B.shape
    if num_rows != 3:
        raise Exception(f"matrix B is not 3xN, it is {num_rows}x{num_cols}")

    # find mean column wise
    centroid_A = np.mean(A, axis=1)
    centroid_B = np.mean(B, axis=1)

    # ensure centroids are 3x1
    centroid_A = centroid_A.reshape(-1, 1)
    centroid_B = centroid_B.reshape(-1, 1)

    # subtract mean
    Am = A - centroid_A
    Bm = B - centroid_B

    H = Am @ np.transpose(Bm)

    # sanity check
    #if linalg.matrix_rank(H) < 3:
    #    raise ValueError("rank of H = {}, expecting 3".format(linalg.matrix_rank(H)))

    # find rotation
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # special reflection case
    if np.linalg.det(R) < 0:
        print("det(R) < R, reflection detected!, correcting for it ...")
        Vt[2,:] *= -1
        R = Vt.T @ U.T

    t = -R @ centroid_A + centroid_B

    trans = np.concatenate((R, t.reshape(-1, 1)), axis=1)
    trans = np.concatenate((trans, np.reshape([0, 0, 0, 1], (1, -1))), axis=0)
    return trans


A = np.asarray([(1.6252901554107666, 0.0, 7.969329357147217),
        (0.12602098286151886, 19.68000030517578, 7.71914529800415),
        (1.9483412504196167, 62.28000259399414, 14.915325164794922),
        (4.186198711395264, 62.28000259399414, 1.5045814514160156)])


B = np.asarray([(-7.7337517738342285, -81.62846374511719, -0.7607399821281433),
    (-9.19552993774414, -65.96459197998047, -0.5031039714813232),
    (-6.304498195648193, -23.512468338012695, 5.515425205230713),
    (-4.061666965484619, -23.66792869567871, -8.060047149658203)])


print(rigid_transform_3D(A.T, B.T))


















def ralign(X, Y):
    m, n = X.shape

    mx = X.mean(1)
    my = Y.mean(1)
    Xc = X - np.tile(mx, (n, 1)).T
    Yc = Y - np.tile(my, (n, 1)).T

    sx = np.mean(np.sum(Xc * Xc, 0))
    sy = np.mean(np.sum(Yc * Yc, 0))

    Sxy = np.dot(Yc, Xc.T) / n

    U, D, V = np.linalg.svd(Sxy, full_matrices=True, compute_uv=True)
    V = V.T.copy()

    r = np.linalg.matrix_rank(Sxy)
    d = np.linalg.det(Sxy)
    S = np.eye(m)
    if r > (m - 1):
        if (np.linalg.det(Sxy) < 0):
            S[m-1, m-1] = -1;
        elif (r == m - 1):
            if (np.linalg.det(U) * np.linalg.det(V) < 0):
                S[m-1, m-1] = -1
        else:
            R = np.eye(3)
            c = 1
            t = np.zeros(3)
    else:
        R = np.dot(np.dot(U, S), V.T)

        c = np.trace(np.dot(np.diag(D), S)) / sx
        t = my - c * np.dot(R, mx)

    trans = np.concatenate((c*R, t.reshape(-1,1)), axis=1)
    trans = np.concatenate((trans, np.reshape([0,0,0,1], (1,-1))), axis=0)
    return trans

def demo1():
    # Run an example test
    # We have 3 points in 3D. Every point is a column vector of this matrix A
    A = np.asarray([(1.6252901554107666, 0.0, 7.969329357147217),
        (0.12602098286151886, 19.68000030517578, 7.71914529800415),
        (1.9483412504196167, 62.28000259399414, 14.915325164794922),
        (4.186198711395264, 62.28000259399414, 1.5045814514160156)])


    B = np.asarray([(-7.7337517738342285, -81.62846374511719, -0.7607399821281433),
        (-9.19552993774414, -65.96459197998047, -0.5031039714813232),
        (-6.304498195648193, -23.512468338012695, 5.515425205230713),
        (-4.061666965484619, -23.66792869567871, -8.060047149658203)])


    # Reconstruct the transformation with ralign.ralign
    # R, c, t = ralign(A.T, B.T)
    # print("Rotation matrix=\n", R, "\nScaling coefficient=", c, "\nTranslation vector=", t)

    trans = ralign(A.T, B.T)
    print("变换矩阵是：\n",trans)
    Atemp = np.concatenate((A.T, np.ones((1, A.shape[0]))), axis=0)
    print(type(trans))
    print(trans.dot(Atemp), '\n', B.T)

"""https://gist.github.com/CarloNicolini/7118015"""

#----------------------------------------------------------------------------------------

#!/usr/bin/env python

import numpy as np

# From https://gist.github.com/CarloNicolini/7118015


def umeyama(X, Y):
  assert X.shape[0] == 3
  assert Y.shape[0] == 3
  assert X.shape[1] > 0
  assert Y.shape[1] > 0

  m, n = X.shape

  mx = X.mean(1)
  my = Y.mean(1)

  Xc = X - np.tile(mx, (n, 1)).T
  Yc = Y - np.tile(my, (n, 1)).T

  sx = np.mean(np.sum(Xc * Xc, 0))
  sy = np.mean(np.sum(Yc * Yc, 0))
  Sxy = np.dot(Yc, Xc.T) / n

  U, D, V = np.linalg.svd(Sxy, full_matrices=True, compute_uv=True)
  V = V.T.copy()

  r = np.linalg.matrix_rank(Sxy)
  d = np.linalg.det(Sxy)
  S = np.eye(m)
  if r > (m - 1):
    if (np.linalg.det(Sxy) < 0):
      S[m, m] = -1
    elif (r == m - 1):
      if (np.linalg.det(U) * np.linalg.det(V) < 0):
        S[m, m] = -1
    else:
      R = np.eye(2)
      c = 1
      t = np.zeros(2)
      return R, c, t

  R = np.dot(np.dot(U, S), V.T)

  c = np.trace(np.dot(np.diag(D), S)) / sx
  t = my - c * np.dot(R, mx)

  return R, t, c


def demo2():
  p_A = np.random.rand(3, 10)
  R_BA = np.array([[0.9689135, -0.0232753, 0.2463025],
                   [0.0236362, 0.9997195, 0.0014915],
                   [-0.2462682, 0.0043765, 0.9691918]])
  B_t_BA = np.array([[1], [2], [3]])
  p_B = np.dot(R_BA, p_A) + B_t_BA

  # Reconstruct the transformation with ralign.ralign
  R, t, c = umeyama(p_A, p_B)
  print("Rotation matrix=\n",R)
  print("Scaling coefficient=", c)
  print("Translation vector=", t)


# demo1()
# demo2()