# data/core/CacheManager.py

'''
- Cache Manager is the first thing that executes when the application starts,
- loads all the required data in the data/storage folder
'''

import json
import os
from typing import Any

class CacheManager:

    def __init__(self):
        self.CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "storage", "symbols.json")

    def update_cache(self, data: dict[str, Any])->bool:
        if (data is None) or (data.__class__.__name__ != "dict"):
            return False
        try:
            with open(self.CACHE_FILE, "w") as f:
                json.dump(data, f, indent=4)
                print("Cache updated successfully!")
            return True
        except IOError as e:
            print("Error updating cache: " + e)
        return False
