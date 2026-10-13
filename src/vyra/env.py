"""Diagnóstico do ambiente. Não importa torch/cv2/ultralytics (usa find_spec e metadata).

Uso: python -m vyra.env [--gpu]
"""

from __future__ import annotations

import importlib.metadata as md
import importlib.util
import platform
import shutil
import sys
from dataclasses import dataclass

# nome de import -> nomes de distribuição possíveis
_PACKAGES = {
    "numpy": ("numpy",),
    "cv2": ("opencv-python-headless", "opencv-python"),
    "torch": ("torch",),
    "ultralytics": ("ultralytics",),
    "pytest": ("pytest",),
    "ruff": ("ruff",),
}


@dataclass(frozen=True, slots=True)
class EnvReport:
    python: str
    platform: str
    packages: tuple[tuple[str, str | None], ...]  # (nome, versão ou None se ausente)
    ffmpeg: str | None
    gpu: str


def _version(import_name: str, dists: tuple[str, ...]) -> str | None:
    if importlib.util.find_spec(import_name) is None:
        return None
    for dist in dists:
        try:
            return md.version(dist)
        except md.PackageNotFoundError:
            continue
    return "instalado (versão desconhecida)"


def _probe_gpu() -> str:
    try:
        import torch  # import deliberado e opcional, somente com --gpu
    except ImportError:
        return "indisponível (torch não instalado)"
    if torch.cuda.is_available():
        return f"cuda: {torch.cuda.get_device_name(0)}"
    return "indisponível (CUDA não detectada; execução em CPU)"


def diagnose(probe_gpu: bool = False) -> EnvReport:
    packages = tuple((name, _version(name, dists)) for name, dists in _PACKAGES.items())
    return EnvReport(
        python=platform.python_version(),
        platform=platform.platform(),
        packages=packages,
        ffmpeg=shutil.which("ffmpeg"),
        gpu=_probe_gpu() if probe_gpu else "não verificada (use --gpu)",
    )


def format_report(report: EnvReport) -> str:
    lines = [f"python   {report.python}", f"platform {report.platform}"]
    for name, version in report.packages:
        lines.append(f"{name:<12} {version or 'ausente'}")
    lines.append(f"ffmpeg   {report.ffmpeg or 'ausente'}")
    lines.append(f"gpu      {report.gpu}")
    return "\n".join(lines)


def main() -> int:
    report = diagnose(probe_gpu="--gpu" in sys.argv)
    print(format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
