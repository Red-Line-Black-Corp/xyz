#!/usr/bin/env python3
"""
Demo CLI for basic transforms and safety checks.
Run: python cli.py demo
"""
import argparse
import numpy as np
from biocraft.quaternion import Quaternion
from biocraft.transforms import Transform, transform_point
from biocraft.safety import SafetyLayer

def demo():
    print("Biomechanical craft transform & safety demo (units: mm, RAS coords)")
    # origin at glabella:
    origin = Transform(Quaternion.identity(), t=[0.0, 0.0, 0.0])
    # craft local point: 200 mm caudal, 50 mm ventral (caudal=-Y, ventral=-Z)
    p_local = np.array([0.0, -200.0, -50.0])
    p_world = transform_point(p_local, origin)
    print("Local point (glabella reference):", p_local)
    print("World point:", p_world)

    # apply rotation
    q = Quaternion.from_euler(0, 0, 45, degrees=True)  # yaw 45 deg
    tf = Transform(q, t=[10.0, -5.0, 2.0])
    p_transformed = transform_point(p_local, tf)
    print("Transformed point with yaw=45deg and translation [10,-5,2]:", p_transformed)

    # safety checks
    safety = SafetyLayer(translational_limits_mm=[[-500,500],[-500,500],[-500,500]],
                         rotational_limits_deg=[[-90,90],[-90,90],[-180,180]],
                         rate_interval=0.01)
    try:
        safety.validate_translation([10, -200, -50])
        safety.validate_rotation_euler_deg([0, 0, 45])
        safety.allow_command()
        print("Safety checks passed for sample command.")
    except Exception as e:
        print("Safety check failed:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs="?", default="demo", choices=["demo"])
    args = parser.parse_args()
    if args.action == "demo":
        demo()
