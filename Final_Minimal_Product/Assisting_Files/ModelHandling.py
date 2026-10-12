import json
from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parents[1] / "Model"


def modelpath(modelname):
    path = Path(str(modelname).replace("\\", "/"))
    return path if path.is_absolute() else MODEL_DIR / path.name


def readmodel(modelname):
    with modelpath(modelname).open(encoding="utf-8") as json_file:
        return json.load(json_file)
