from pathlib import Path
import csv
import io
import json
import zipfile
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SkyGuard API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUIRED_FIELDS = {"temperature", "humidity", "pressure", "wind_speed"}


def numeric(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def detect(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Baseline, transparent detector. Replace with the trained model adapter later."""
    measurements = [
        {key: numeric(row.get(key)) for key in REQUIRED_FIELDS}
        for row in rows
    ]
    valid = [row for row in measurements if all(v is not None for v in row.values())]
    if not valid:
        raise HTTPException(400, "CSV must contain numeric temperature, humidity, pressure and wind_speed columns")

    stats: dict[str, tuple[float, float]] = {}
    for key in REQUIRED_FIELDS:
        values = [row[key] for row in valid if row[key] is not None]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        stats[key] = (mean, variance**0.5)

    results = []
    for index, row in enumerate(measurements):
        scores = []
        for key, value in row.items():
            mean, std = stats[key]
            scores.append(abs(value - mean) / std if std > 0 else 0.0)
        score = max(scores)
        results.append({"row": index + 1, "anomaly": score >= 3, "score": round(score, 3), "values": row})

    anomalies = sum(item["anomaly"] for item in results)
    return {"total": len(results), "anomalies": anomalies, "normal": len(results) - anomalies, "results": results}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)) -> dict[str, Any]:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Upload a CSV file")
    try:
        text = (await file.read()).decode("utf-8-sig")
        rows = list(csv.DictReader(io.StringIO(text)))
        return detect(rows)
    except UnicodeDecodeError as exc:
        raise HTTPException(400, "CSV must be UTF-8 encoded") from exc


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "SkyGuard API is running", "docs": "/docs"}
