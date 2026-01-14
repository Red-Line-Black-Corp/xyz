# Biomechanical Craft — Security, Simulation & Visualizer

Contents
- SECURITY_CHECKLIST.md — concise hardening & policy checklist
- LICENSE — MIT
- python/ — Python simulation package (NumPy). Includes transforms, quaternions, safety checks, CLI demo, and unit tests.
- visualizer/ — Three.js Web visualizer (index.html + main.js + styles.css)

Defaults used
- Origin: glabella
- Coordinate convention: RAS (Right = +X, Anterior/Rostral = +Y, Superior/Dorsal = +Z)
- Units: millimeters (mm)

Quick start

1) Python simulation
- Requirements: Python 3.9+ and pip
- Install deps:
  python -m pip install -r python/requirements.txt
- Run demo:
  python python/cli.py demo
- Run tests:
  python -m pytest python/tests

2) Visualizer
- Serve `visualizer/` directory with any static server (e.g., `npx http-server visualizer` or `python -m http.server` from that folder).
- Open `http://localhost:8080` (or whichever port) to see the scene. Use UI to play sample animation.

Notes
- The command-signing functions are placeholders; integrate your HSM/TPM or KMS for production signing/verification.
- The Python safety layer demonstrates input validation, bounds checking, rate limiting, and a human-in-the-loop gating simulation.
- The visualizer is a lightweight WebGL scene intended for UX and transform validation — it does not connect to physical hardware.

If you want, I can:
- Package this into a GitHub repository and create branches/tags.
- Convert the visualizer into a ROS-integrated node (URDF) for Gazebo or PyBullet.
- Add continuous-integration (CI) config (GitHub Actions) to run tests/security checks.
