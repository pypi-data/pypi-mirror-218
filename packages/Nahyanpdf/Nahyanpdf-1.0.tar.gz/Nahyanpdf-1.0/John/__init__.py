import json
from pathlib import Path

x = Path("movies.json").read_text()
y = json.loads(x)
print(y[0]["title"])
