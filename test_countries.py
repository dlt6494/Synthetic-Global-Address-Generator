import pgeocode
import pycountry

# Test which countries actually work with pgeocode
test_countries = [
    'AT', 'BE', 'BR', 'CH', 'DE', 'DK', 'ES', 'FI', 'FR', 'GB', 
    'GR', 'HU', 'IE', 'IT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 
    'SI', 'SK', 'US', 'CA', 'AU', 'NZ', 'JP', 'KR', 'MX', 'IN',
    'RU', 'CZ', 'TR', 'IL', 'ZA', 'BR'
]

working_countries = []
for country_code in test_countries:
    try:
        nomi = pgeocode.Nominatim(country=country_code)
        # Try a simple query
        result = nomi.query_postal_code('12345')
        working_countries.append(country_code)
        print(f"✓ {country_code} works")
    except Exception as e:
        print(f"✗ {country_code}: {str(e)[:50]}")

print(f"\nWorking countries: {working_countries}")
print(f"Total: {len(working_countries)}")
