import numpy as np
from biocraft.quaternion import Quaternion
from biocraft.transforms import Transform, transform_point, invert_transform

def test_identity_transform():
    tf = Transform()
    p = np.array([10.0, 20.0, 30.0])
    res = transform_point(p, tf)
    assert np.allclose(res, p)

def test_rotation_transform():
    q = Quaternion.from_euler(0, 0, 90, degrees=True)
    tf = Transform(q, t=[0,0,0])
    p = np.array([1.0, 0.0, 0.0])
    res = transform_point(p, tf)
    # rotating +X by +90deg yaw -> +Y (anterior)
    assert np.allclose(np.round(res, 6), np.array([0.0, 1.0, 0.0]))

def test_inverse():
    q = Quaternion.from_euler(0, 0, 45, degrees=True)
    tf = Transform(q, t=[10.0, 5.0, -2.0])
    R_inv, t_inv = invert_transform(tf)
    p = np.array([100.0, 0.0, 0.0])
    # T_inv * (T * p) == p
    R = q.to_rotation_matrix()
    p_world = R.dot(p) + tf.t
    p_back = R_inv.dot(p_world) + t_inv
    assert np.allclose(np.round(p_back,6), np.round(p,6))
