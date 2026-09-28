"""
Rebuild the whole CryptoDiversify pipeline from scratch, in order:

  1. fetch_data    - download daily prices from Binance -> data/raw/
  2. load_to_db    - load prices + log returns into SQLite -> data/project.db
  3. analysis      - RQ1-RQ3 point estimates -> data/processed/
  4. significance  - block-bootstrap CIs and tests -> data/processed/significance_tests.csv

Run from the project folder:   python main.py
Use --skip-fetch to reuse the CSVs already in data/raw/ (no internet needed).
Note: fetching again pulls prices up to today, so the numbers can shift slightly.
"""
import sys

sys.path.insert(0, "src")

import fetch_data
import load_to_db
import analysis
import significance


def main():
    if "--skip-fetch" not in sys.argv:
        print("\n[1/4] Fetching prices from Binance")
        fetch_data.main()
    else:
        print("\n[1/4] Skipping download, using data/raw/")
    print("\n[2/4] Loading into SQLite")
    load_to_db.main()
    print("\n[3/4] Running analysis")
    analysis.main()
    print("\n[4/4] Bootstrap confidence intervals")
    significance.main()
    print("\nDone. Open dashboard/cryptodiversify.pbix and click Refresh to update the dashboard.")


if __name__ == "__main__":
    main()
