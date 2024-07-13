import pandas as pd
from io import StringIO

def validate_csv(file):
    try:
        df = pd.read_csv(file)
        if df.columns.tolist() != ['Serial Number', 'Product Name', 'Input Image Urls']:
            return False
        return True
    except Exception as e:
        return False
