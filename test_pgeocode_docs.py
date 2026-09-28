import pgeocode
import pandas as pd

# Check what unique actually is
nomi = pgeocode.Nominatim(country='US')
print(f"unique type: {type(nomi.unique)}")
print(f"unique value: {nomi.unique}")

# Check if there's a way to get postal codes data directly
print(f"\nAttributes: {[a for a in dir(nomi) if not a.startswith('_')]}")

# Check the documentation
print(f"\nNominatim docstring:")
print(pgeocode.Nominatim.__doc__)

# Try query_location
print("\n\nTesting query_location:")
try:
    result = nomi.query_location('New York, NY')
    print(result)
except Exception as e:
    print(f"Error: {e}")
