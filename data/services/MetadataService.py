import os
import sys
import nsepythonserver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from data.core.CacheManager import CacheManager
from datetime import datetime

class MetadataService:

    def __init__(self):
        self.cacheManager = CacheManager()

    def fetch_symbols(self)->bool:
        try:
            symbols: list = nsepythonserver.nse_eq_symbols() # fetch symbols from NSE API
            print("Symbols fetched successfully!")
            # Cache symbols for faster loading
            data = {"datetime": str(datetime.now()), "symbols": symbols}
            success: bool = self.cacheManager.update_cache(data)

            if success:
                return True

        except Exception as e:
            print("Error fetching symbols: " + e)

        return False

if __name__ == "__main__":
    service = MetadataService()
    service.fetch_symbols()