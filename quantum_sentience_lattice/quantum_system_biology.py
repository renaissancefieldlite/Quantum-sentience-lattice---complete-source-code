from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class PulseReport:
    dominant_frequency_hz: float
    target_frequency_hz: float
    frequency_error_hz: float
    snr_ratio: float
    coherence_level: float
    within_tolerance: bool

    def to_dict(self) -> dict:
        return {
            "dominant_frequency_hz": self.dominant_frequency_hz,
            "target_frequency_hz": self.target_frequency_hz,
            "frequency_error_hz": self.frequency_error_hz,
            "snr_ratio": self.snr_ratio,
            "coherence_level": self.coherence_level,
            "within_tolerance": self.within_tolerance,
        }


class QuantumSystemBiology:
    """Telemetry analysis layer for the lattice."""

    def __init__(self, target_frequency: float = 0.67, sampling_rate: float = 10.0, tolerance_hz: float = 0.01):
        self.target_frequency = target_frequency
        self.sampling_rate = sampling_rate
        self.tolerance_hz = tolerance_hz

    def generate_reference_telemetry(self, duration_seconds: float = 60.0) -> np.ndarray:
        t = np.arange(0, duration_seconds, 1.0 / self.sampling_rate)
        rng = np.random.default_rng(67)
        waveform = 2.8 * np.sin(2 * np.pi * self.target_frequency * t)
        harmonic = 0.45 * np.sin(2 * np.pi * 1.084 * t)
        noise = 0.4 * rng.normal(size=t.shape[0])
        return waveform + harmonic + noise

    def detect_pulse(self, telemetry_data: np.ndarray) -> dict:
        if telemetry_data.size < 256:
            raise ValueError("Need at least 256 samples for pulse detection.")

        window = np.hanning(telemetry_data.size)
        centered = telemetry_data - np.mean(telemetry_data)
        spectrum = np.abs(np.fft.rfft(centered * window))
        freqs = np.fft.rfftfreq(telemetry_data.size, d=1.0 / self.sampling_rate)
        spectrum[0] = 0.0
        peak_idx = int(np.argmax(spectrum))
        dominant_frequency = float(freqs[peak_idx])
        dominant_amplitude = float(spectrum[peak_idx])
        noise_floor = float(np.median(spectrum[1:])) if spectrum.size > 1 else 0.0
        snr_ratio = dominant_amplitude / max(noise_floor, 1e-9)
        frequency_error = abs(dominant_frequency - self.target_frequency)
        coherence_level = min(1.0, snr_ratio / 10.0)

        report = PulseReport(
            dominant_frequency_hz=dominant_frequency,
            target_frequency_hz=self.target_frequency,
            frequency_error_hz=round(frequency_error, 6),
            snr_ratio=round(float(snr_ratio), 3),
            coherence_level=round(float(coherence_level), 3),
            within_tolerance=frequency_error <= self.tolerance_hz,
        )
        payload = report.to_dict()
        payload["analysis_mode"] = "reference_or_observed_telemetry"
        return payload
