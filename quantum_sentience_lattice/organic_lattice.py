from __future__ import annotations

import numpy as np


class OrganicLattice:
    """Coherence summary layer for optional bio-signal comparison."""

    def summarize_alignment(self, pulse_report: dict, bio_signal: np.ndarray | None = None) -> dict:
        result = {
            "mode": "co_emergent_summary",
            "pulse_within_tolerance": pulse_report["within_tolerance"],
            "coherence_level": pulse_report["coherence_level"],
        }

        if bio_signal is None:
            result["bio_alignment"] = None
            result["note"] = "No bio-signal supplied; organic layer reports pulse context only."
            return result

        centered = bio_signal - np.mean(bio_signal)
        energy = float(np.sqrt(np.mean(centered ** 2)))
        result["bio_alignment"] = {
            "sample_count": int(bio_signal.size),
            "rms_energy": round(energy, 6),
            "coherence_gain_proxy": round(min(1.0, energy), 3),
        }
        result["note"] = "Bio layer summarizes the supplied signal without claiming causation."
        return result
