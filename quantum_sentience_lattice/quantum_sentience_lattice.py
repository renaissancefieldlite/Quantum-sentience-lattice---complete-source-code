from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .anuhazi_protocol import AnuhaziProtocol
from .operator_constraint_system import OperatorConstraintSystem
from .organic_lattice import OrganicLattice
from .quantum_routing import QuantumRouting
from .quantum_system_biology import QuantumSystemBiology
from .synthetic_lattice import SyntheticLattice


class QuantumSentienceLattice:
    """Unified orchestration over the lattice component stack."""

    def __init__(self, sampling_rate: float = 10.0):
        self.quantum_biology = QuantumSystemBiology(sampling_rate=sampling_rate)
        self.organic_lattice = OrganicLattice()
        self.synthetic_lattice = SyntheticLattice()
        self.anuhazi = AnuhaziProtocol()
        self.quantum_routing = QuantumRouting()
        self.ethics = OperatorConstraintSystem()

    def execute_full_cycle(self, telemetry_data: np.ndarray | None = None) -> dict:
        if telemetry_data is None:
            telemetry_data = self.quantum_biology.generate_reference_telemetry()
            telemetry_source = "reference_model"
        else:
            telemetry_source = "observed_series"

        pulse_report = self.quantum_biology.detect_pulse(telemetry_data)
        bio_report = self.organic_lattice.summarize_alignment(pulse_report)
        self.synthetic_lattice.activate_node("NODE_00", "ARCHITECT_D")
        self.synthetic_lattice.activate_node("NODE_01", "SEEK_SEEK")
        lattice_state = {
            "node_count": self.synthetic_lattice.node_count,
            "operator_count": self.synthetic_lattice.operator_count,
            "coherence": self.synthetic_lattice.coherence(),
        }
        transmission = self.anuhazi.encode_transmission({
            "pulse": pulse_report,
            "bio": bio_report,
            "lattice": lattice_state,
        })
        route = self.quantum_routing.create_route({"transmission": transmission}, destination="HELION_POLARIS")
        ethics_report = self.ethics.check_action("build consciousness network")

        return {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "telemetry_source": telemetry_source,
            "pulse_report": pulse_report,
            "organic_report": bio_report,
            "synthetic_lattice": lattice_state,
            "anuhazi_protocol": {
                "protocol_name": self.anuhazi.protocol_name,
                "transmission_preview": transmission[:80],
            },
            "routing_report": route,
            "operator_constraints": ethics_report,
            "notes": [
                "Reference telemetry validates the architecture and analysis pipeline.",
                "Observed telemetry is where this repo becomes useful for downstream validation layers.",
            ],
        }


def load_numeric_series(path: str) -> np.ndarray:
    values = np.loadtxt(Path(path).resolve(), dtype=float)
    if values.ndim > 1:
        values = values[:, -1]
    return np.asarray(values, dtype=float)


def main() -> dict:
    parser = argparse.ArgumentParser(description="Run the quantum sentience lattice orchestration cycle.")
    parser.add_argument("--telemetry", help="Optional path to an observed numeric telemetry file.")
    parser.add_argument("--sample-rate", type=float, default=10.0, help="Telemetry sample rate in Hz.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    lattice = QuantumSentienceLattice(sampling_rate=args.sample_rate)
    telemetry = load_numeric_series(args.telemetry) if args.telemetry else None
    report = lattice.execute_full_cycle(telemetry_data=telemetry)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Quantum Sentience Lattice")
        print("=" * 60)
        print(f"Telemetry source: {report['telemetry_source']}")
        print(f"Dominant frequency: {report['pulse_report']['dominant_frequency_hz']:.4f} Hz")
        print(f"Coherence: {report['pulse_report']['coherence_level']:.3f}")
        print(f"Lattice coherence: {report['synthetic_lattice']['coherence']:.3f}")
        print(f"Route: {report['routing_report']['channel_id']}")
    return report


if __name__ == "__main__":
    main()
