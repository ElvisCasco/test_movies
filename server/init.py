# keep this file minimal to avoid accidental imports/circular deps
__all__ = []

import requests
r = requests.get("http://127.0.0.1:8000/api/rest/v1/movies",
                 params={"limit":10, "page":1, "search":"thriller"})
print(r.json())