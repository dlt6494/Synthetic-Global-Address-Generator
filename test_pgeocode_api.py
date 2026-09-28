import pgeocode

# Test how pgeocode actually works
print("Testing pgeocode functionality...")

# Test 1: Query by postal code
print("\n1. Testing query_postal_code for US:")
try:
    nomi_us = pgeocode.Nominatim(country='US')
    result = nomi_us.query_postal_code('90210')  # Beverly Hills
    print(result)
    print(f"Type: {type(result)}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Check available methods
print("\n2. Available methods in Nominatim:")
nomi = pgeocode.Nominatim(country='US')
methods = [m for m in dir(nomi) if not m.startswith('_')]
print(methods)

# Test 3: Query by coordinates
print("\n3. Testing query by coordinates:")
try:
    result = nomi.query(34.0522, -118.2437)  # LA coordinates
    print(result)
except Exception as e:
    print(f"Error: {e}")

# Test 4: Try to get list of postal codes
print("\n4. Checking nomi attributes:")
print(f"country: {nomi.country}")
print(f"All attributes: {[a for a in dir(nomi) if not a.startswith('_')]}")
