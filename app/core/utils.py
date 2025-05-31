import json
from pathlib import Path

class Util:
    @staticmethod
    def search_cod_municipalities(city: str, uf: str, path: str = "public/jsons/municipalities.json"):
        file = Path(path)
        if not file.exists():
            raise FileNotFoundError(f"File not foud: {path}")

        with file.open("r", encoding="utf-8") as f:
            municipalities = json.load(f)

        for municipality in municipalities:
            if municipality["Nome"].lower() == city.lower() and municipality["Uf"].upper() == uf.upper():
                return municipality["Codigo"]

        return None