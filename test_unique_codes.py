import pgeocode
import pandas as pd

# Test unique() method to get all valid postal codes
print("Testing unique postal codes...")

# Test for US
print("\n1. Testing US unique postal codes:")
try:
    nomi_us = pgeocode.Nominatim(country='US')
    unique_codes = nomi_us.unique()
    print(f"Type: {type(unique_codes)}")
    print(f"Length: {len(unique_codes) if hasattr(unique_codes, '__len__') else 'unknown'}")
    if isinstance(unique_codes, pd.Index):
        print(f"First 20 postal codes: {unique_codes[:20].tolist()}")
    elif isinstance(unique_codes, pd.Series):
        print(f"First 20: {unique_codes.head(20).tolist()}")
    else:
        print(f"First 20: {unique_codes[:20]}")
except Exception as e:
    print(f"Error: {e}")

# Test for a small country
print("\n2. Testing Austria unique postal codes:")
try:
    nomi_at = pgeocode.Nominatim(country='AT')
    unique_codes = nomi_at.unique()
    print(f"Type: {type(unique_codes)}")
    print(f"Length: {len(unique_codes)}")
    if isinstance(unique_codes, pd.Index):
        print(f"Sample postal codes: {unique_codes[:10].tolist()}")
    elif isinstance(unique_codes, pd.Series):
        print(f"Sample: {unique_codes.head(10).tolist()}")
    else:
        print(f"Sample: {list(unique_codes[:10])}")
except Exception as e:
    print(f"Error: {e}")

# Test query_postal_code for one of those codes
print("\n3. Testing query_postal_code with a real code:")
try:
    result = nomi_at.query_postal_code('1010')
    print(result)
except Exception as e:
    print(f"Error: {e}")
