
Adaptive‑Node Assignment & QR Identity System

Repository: Red‑Line Black Corp / xyz

This repository implements the Device Adaptive‑Node Assignment System, a geospatial identity engine that assigns deterministic/L node‑cell identifiers to registered devices, generates QR codes, and produces identity bundles for downstream routing, inspection, and service‑code validation.

The system is powered by GitHub Actions, Python, and a deterministic geospatial quantization model.

🔧 Core Features

1. Adaptive‑Node Collocation

Each device is mapped into a deterministic node cell using:

Latitude

Longitude

Elevation (meters or feet)

Configurable unit sizes

This produces a stable identifier:

cell_lat{index}_lon{index}_elev{index}

2. QR Code Generation

Each workflow run generates:

A QR code image

A compact JSON payload for scanning

A full identity bundle

3. Identity Bundle Output

Each device receives:

Node‑cell metadata

Primary + side URIs

Service code

Owner mark

Witness metadata

Inspection timestamp

4. Artifact Storage

Outputs are stored under:

artifacts/
└── qr/
└── <device_id>_identity.json

🚀 How to Use the System

1. Trigger the Workflow

Navigate to:

GitHub → Actions → Device Adaptive Node & QR Assignment → Run workflow

Fill in the required fields:

device_id

latitude

longitude

elevation

elevation_unit (m or ft)

service_code

owner_mark (optional)

2. Workflow Execution

The workflow:

Computes the node‑cell index

Generates a QR code

Builds the identity bundle

Stores artifacts

3. Retrieve Artifacts

After the run completes:

Open the workflow run

Scroll to Artifacts

Download:

qr/<device_id>_qr.png

<device_id>_identity.json

📁 Repository Structure

xyz/
│
├── .github/
│   └── workflows/
│       └── device-node-collocate.yml
│
├── tools/
│   └── device_node_assignment.py
│
├── artifacts/
│   ├── qr/
│   └── *.json
│
├── docs/
│   ├── system-overview.md
│   ├── node-cell-spec.md
│   └── api-uris.md
│
├── README.md
└── .gitignore

🧠 Technical Overview

Node‑Cell Quantization

The system uses fixed unit sizes:

0.01° latitude

0.01° longitude

10 m elevation

These can be extended in future workflows.

Elevation Conversion

Supports:

meters

feet → converted to meters

QR Payload Format

Compact JSON:

{
  "device_id": "...",
  "node_cell_id": "...",
  "service_code": "...",
  "primary_uri": "...",
  "side_uri": "..."
}

Identity Bundle Format

Full JSON:

{
  "device_id": "...",
  "owner_mark": "...",
  "service_code": "...",
  "geo_point": {...},
  "node_cell": {...},
  "uris": {...},
  "inspection": {...},
  "witness": {...},
  "qr": {...}
}

🛠 Dependencies

Installed automatically by the workflow:

qrcode[pil]

Python version: 3.11

📌 Future Extensions (Supported by This Repo)

This repository is structured to support additional workflows:

Device inspection & verification

Transaction logging

Side‑domain routing updates

Monitoring map generation

Multi‑unit node‑cell scaling

Device revocation & re‑assignment


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
  python -m pip 
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
- Add continuous-integration (CI) config (GitHub 
