# recommend/utils.py
import json
import os

def load_tickers():
    filepath = os.path.join(
        os.path.expanduser("~"),
        "OneDrive", "바탕 화면", "Final_Project", "front", "src", "assets", "tickers.json"
    )
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
