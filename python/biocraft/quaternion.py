import numpy as np

class Quaternion:
    """Simple quaternion representation (w, x, y, z)."""

    def __init__(self, w, x, y, z):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @staticmethod
    def identity():
        return Quaternion(1.0, 0.0, 0.0, 0.0)

    def as_np(self):
        return np.array([self.w, self.x, self.y, self.z], dtype=float)

    def to_rotation_matrix(self):
        w, x, y, z = self.as_np()
        # normalize to reduce drift
        n = np.linalg.norm([w, x, y, z])
        if n == 0:
            raise ValueError("Zero-length quaternion")
        w, x, y, z = (w / n, x / n, y / n, z / n)
        R = np.array([
            [1 - 2*(y*y + z*z),     2*(x*y - w*z),     2*(x*z + w*y)],
            [    2*(x*y + w*z), 1 - 2*(x*x + z*z),     2*(y*z - w*x)],
            [    2*(x*z - w*y),     2*(y*z + w*x), 1 - 2*(x*x + y*y)]
        ], dtype=float)
        return R

    @staticmethod
    def from_euler(roll, pitch, yaw, degrees=False):
        """Create quaternion from Euler angles (intrinsic XYZ)."""
        if degrees:
            roll = np.deg2rad(roll)
            pitch = np.deg2rad(pitch)
            yaw = np.deg2rad(yaw)
        cr = np.cos(roll / 2)
        sr = np.sin(roll / 2)
        cp = np.cos(pitch / 2)
        sp = np.sin(pitch / 2)
        cy = np.cos(yaw / 2)
        sy = np.sin(yaw / 2)
        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy
        return Quaternion(w, x, y, z)

    def __repr__(self):
        return f"Quaternion({self.w:.6f}, {self.x:.6f}, {self.y:.6f}, {self.z:.6f})"
