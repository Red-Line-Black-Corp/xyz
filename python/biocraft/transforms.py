import numpy as np
from .quaternion import Quaternion

class Transform:
    """Homogeneous transform: rotation (quaternion) and translation (3-vector). Units in mm by default."""
    def __init__(self, q: Quaternion = None, t=None):
        self.q = q if q is not None else Quaternion.identity()
        self.t = np.array(t if t is not None else [0.0, 0.0, 0.0], dtype=float)

    def as_matrix(self):
        R = self.q.to_rotation_matrix()
        T = np.eye(4, dtype=float)
        T[:3, :3] = R
        T[:3, 3] = self.t
        return T

    def inverse(self):
        R = self.q.to_rotation_matrix()
        R_inv = R.T
        t_inv = -R_inv.dot(self.t)
        # Convert R_inv back to quaternion is omitted — keep using rotation matrix when needed
        # For simplicity use identity quaternion for inverse's storage but keep t_inv and matrix for transforms
        inv = Transform(Quaternion.identity(), t_inv)
        inv._inv_R = R_inv
        return inv

def transform_point(p_local, transform: Transform):
    """p_local as iterable of length 3, return world coordinates"""
    p = np.array(p_local, dtype=float)
    R = transform.q.to_rotation_matrix()
    return R.dot(p) + transform.t

def invert_transform(transform: Transform):
    """Return (R_inv, t_inv) for the transform — R_inv is 3x3, t_inv is 3-vector"""
    R = transform.q.to_rotation_matrix()
    R_inv = R.T
    t_inv = -R_inv.dot(transform.t)
    return R_inv, t_inv
