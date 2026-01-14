#!/usr/bin/env python3
import argparse
import math
from dataclasses import dataclass, asdict
from typing import Tuple, Dict, Any


@dataclass
class GeoPoint:
    latitude: float
    longitude: float
    elevation: float  # in meters


@dataclass
class NodeCell:
    lat_index: int
    lon_index: int
    elev_index: int
    lat_unit_size_deg: float
    lon_unit_size_deg: float
    elev_unit_size_m: float

    @property
    def id(self) -> str:
        """
        Deterministic ID for the adaptive node cell.
        """
        return f"cell_lat{self.lat_index}_lon{self.lon_index}_elev{self.elev_index}"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["id"] = self.id
        return d


def convert_elevation_to_meters(elev: float, unit: str) -> float:
    """
    Convert elevation to meters from the given unit.
    Supported units: 'm', 'ft'.
    """
    unit = unit.lower()
    if unit == "m":
        return elev
    if unit == "ft":
        return elev * 0.3048
    raise ValueError(f"Unsupported elevation unit: {unit}")


def quantize_coordinate(value: float, unit_size: float) -> int:
    """
    Quantize a continuous coordinate into an integer index based on unit size.
    """
    return math.floor(value / unit_size)


def build_node_cell(
    point: GeoPoint,
    lat_unit_size_deg: float,
    lon_unit_size_deg: float,
    elev_unit_size_m: float,
) -> NodeCell:
    """
    Build a NodeCell representing the collocated adaptive-node region
    for the given point and unit sizes.
    """
    lat_index = quantize_coordinate(point.latitude, lat_unit_size_deg)
    lon_index = quantize_coordinate(point.longitude, lon_unit_size_deg)
    elev_index = quantize_coordinate(point.elevation, elev_unit_size_m)

    return NodeCell(
        lat_index=lat_index,
        lon_index=lon_index,
        elev_index=elev_index,
        lat_unit_size_deg=lat_unit_size_deg,
        lon_unit_size_deg=lon_unit_size_deg,
        elev_unit_size_m=elev_unit_size_m,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collocate adaptive-node at a select unit of elevation origin using lat/long."
    )
    parser.add_argument("--lat", "--latitude", dest="latitude", required=True, type=float,
                        help="Latitude in decimal degrees.")
    parser.add_argument("--lon", "--longitude", dest="longitude", required=True, type=float,
                        help="Longitude in decimal degrees.")
    parser.add_argument("--elev", "--elevation", dest="elevation", required=True, type=float,
                        help="Elevation at origin.")
    parser.add_argument("--elev-unit", dest="elev_unit", default="m", choices=["m", "ft", "M", "FT"],
                        help="Unit of elevation origin (m or ft).")
    parser.add_argument("--lat-unit-size", dest="lat_unit_size", default=0.01, type=float,
                        help="Latitudinal unit size in degrees for node cell.")
    parser.add_argument("--lon-unit-size", dest="lon_unit_size", default=0.01, type=float,
                        help="Longitudinal unit size in degrees for node cell.")
    parser.add_argument("--elev-unit-size", dest="elev_unit_size", default=10.0, type=float,
                        help="Elevation unit size in the same unit as --elev-unit.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Convert elevation to meters and unit size to meters
    elev_m = convert_elevation_to_meters(args.elevation, args.elev_unit)
    elev_unit_size_m = convert_elevation_to_meters(args.elev_unit_size, args.elev_unit)

    point = GeoPoint(
        latitude=args.latitude,
        longitude=args.longitude,
        elevation=elev_m,
    )

    node_cell = build_node_cell(
        point=point,
        lat_unit_size_deg=args.lat_unit_size,
        lon_unit_size_deg=args.lon_unit_size,
        elev_unit_size_m=elev_unit_size_m,
    )

    # Output a concise, machine- and human-readable summary
    print("=== Adaptive Node Collocation Result ===")
    print(f"Input point: lat={point.latitude}, lon={point.longitude}, elev_m={point.elevation}")
    print(f"Unit sizes: lat={args.lat_unit_size}°, lon={args.lon_unit_size}°, elev={elev_unit_size_m} m")
    print(f"Node cell ID: {node_cell.id}")
    print("Node cell indices and metadata:")
    for k, v in node_cell.to_dict().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
