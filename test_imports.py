import sys
print(sys.executable)
print(sys.path)

try:
    import pandas
    print("pandas: OK")
except ImportError as e:
    print(f"pandas: FAILED - {e}")

try:
    import pgeocode
    print("pgeocode: OK")
except ImportError as e:
    print(f"pgeocode: FAILED - {e}")

try:
    import pycountry
    print("pycountry: OK")
except ImportError as e:
    print(f"pycountry: FAILED - {e}")

try:
    import geopy
    print("geopy: OK")
except ImportError as e:
    print(f"geopy: FAILED - {e}")

try:
    import numpy
    print("numpy: OK")
except ImportError as e:
    print(f"numpy: FAILED - {e}")
