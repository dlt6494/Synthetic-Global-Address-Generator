import pandas as pd
import pycountry
import pgeocode
import random
import time
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

class SyntheticAddressGenerator:
    """Generate synthetic but geographically valid addresses using pgeocode and pycountry."""

    SUPPORTED_COUNTRIES = ('CA', 'MX')
    
    POSTAL_CODE_RANGES = {
        # US - All 50 states + DC with comprehensive postal codes
        'US': ['35004', '35005', '35006', '35007', '35008', '99501', '99502', '99503', '99504', '99505',
               '85001', '85002', '85003', '85004', '85005', '71601', '71602', '71603', '71604', '71605',
               '90001', '90002', '90003', '90004', '90005', '80001', '80002', '80003', '80004', '80005',
               '06001', '06002', '06003', '06004', '06005', '19701', '19702', '19703', '19704', '19705',
               '20001', '20002', '20003', '20004', '20005', '32003', '32004', '32005', '32006', '32007',
               '30002', '30003', '30004', '30005', '30006', '96701', '96702', '96703', '96704', '96705',
               '83201', '83202', '83203', '83204', '83205', '60001', '60002', '60003', '60004', '60005',
               '46001', '46002', '46003', '46004', '46005', '50001', '50002', '50003', '50004', '50005',
               '66002', '66003', '66004', '66005', '66006', '40003', '40004', '40005', '40006', '40007',
               '70001', '70002', '70003', '70004', '70005', '03901', '03902', '03903', '03904', '03905',
               '20601', '20602', '20603', '20604', '20605', '01001', '01002', '01003', '01004', '01005',
               '48001', '48002', '48003', '48004', '48005', '55001', '55002', '55003', '55004', '55005',
               '38601', '38602', '38603', '38604', '38605', '63001', '63002', '63003', '63004', '63005',
               '59001', '59002', '59003', '59004', '59005', '68001', '68002', '68003', '68004', '68005',
               '88901', '88902', '88903', '88904', '88905', '03031', '03032', '03033', '03034', '03035',
               '07001', '07002', '07003', '07004', '07005', '87001', '87002', '87003', '87004', '87005',
               '00501', '00502', '00503', '00504', '00505', '27006', '27007', '27008', '27009', '27010',
               '58001', '58002', '58003', '58004', '58005', '43001', '43002', '43003', '43004', '43005',
               '73001', '73002', '73003', '73004', '73005', '97001', '97002', '97003', '97004', '97005',
               '15001', '15002', '15003', '15004', '15005', '02801', '02802', '02803', '02804', '02805',
               '29001', '29002', '29003', '29004', '29005', '57001', '57002', '57003', '57004', '57005',
               '37010', '37011', '37012', '37013', '37014', '73301', '73302', '73303', '73304', '73305',
               '84001', '84002', '84003', '84004', '84005', '05001', '05002', '05003', '05004', '05005',
               '20101', '20102', '20103', '20104', '20105', '98001', '98002', '98003', '98004', '98005',
               '24701', '24702', '24703', '24704', '24705', '53001', '53002', '53003', '53004', '53005',
               '82001', '82002', '82003', '82004', '82005'],
        
        # English-speaking and European countries (no Korean, Russian, Japanese, Chinese)
        'AT': ['1010', '2500', '5020', '6020', '8010'],
        'BE': ['1000', '2000', '3000', '8000', '9000'],
        'BR': ['01310', '20040', '30140', '50040', '70040'],
        'CH': ['1200', '2500', '3011', '4051', '5000', '6900', '8000', '9000'],
        'DE': ['10115', '20354', '30159', '40213', '50667', '60311', '70173', '80331', '90402'],
        'DK': ['1000', '2100', '2800', '4000', '5000', '6000', '7000', '8000', '9000'],
        'ES': ['28001', '08002', '41001', '46001', '37001', '48001', '80001', '46100'],
        'FI': ['00100', '33100', '90100', '70100', '40100'],
        'FR': ['75001', '69001', '13001', '59000', '14000', '35000', '33000', '13010'],
        'GB': ['SW1A', 'M1', 'B1', 'LS1', 'EH1', 'G1', 'NI1', 'CF1'],
        'HU': ['1011', '2000', '6720', '8000', '9000'],
        'IE': ['D01', 'V94', 'T12', 'D06', 'F12'],
        'IT': ['00100', '20100', '80100', '90100', '50100', '16100', '35100', '70100'],
        'NL': ['1000', '2500', '3500', '5600', '6000', '7500', '9000'],
        'NO': ['0150', '0300', '3000', '4000', '5000', '6000', '7000', '8000', '9000'],
        'PL': ['00001', '31000', '50000', '80000', '90000'],
        'PT': ['1000', '2700', '3000', '4000', '5000', '6000', '7000', '8000', '9000'],
        'RO': ['010001', '300001', '400001', '700001', '900001'],
        'SE': ['10001', '20100', '30100', '40100', '50100', '60100', '70100', '80100', '90100'],
        'SI': ['1000', '2000', '3000', '4000', '5000', '6000', '8000', '9000'],
        'SK': ['8001', '8100', '8200', '9000', '9100'],
        'CA': ['M5H', 'V6B', 'T2P', 'H2X', 'K1P', 'L4B', 'R3B', 'J4H', 'B3J', 'V1V'],
        'AU': ['2000', '3000', '4000', '5000', '6000', '7000', '2600', '2800', '3100'],
        'NZ': ['1000', '1010', '2012', '3015', '4410', '5000', '6001', '7000', '8000'],
        'MX': ['06500', '06600', '11540', '28000', '50000'],
        'IN': ['110001', '110002', '110003', '400001', '500001'],
        'CZ': ['11000', '13000', '30000', '40000', '50000'],
        'TR': ['34330', '35000', '06100', '16000', '35000'],
        'ZA': ['1000', '2000', '3000', '4000', '5000', '8000', '9000'],
    }
    
    def __init__(self):
        """Initialize the generator."""
        self.countries_with_coverage = []
        self.records = []
        self.postal_code_cache = {}
        self.postal_data_by_country = {}
        self.street_names = {
            'CA': [
                'Main Street', 'Oak Street', 'Maple Street', 'King Street', 'Queen Street',
                'First Avenue', 'Park Avenue', 'Lake Street', 'River Road', 'Cedar Road'
            ],
            'MX': [
                'Avenida Reforma', 'Avenida Juarez', 'Calle Hidalgo', 'Calle Morelos',
                'Avenida Universidad', 'Calle Independencia', 'Avenida Central',
                'Calle Allende', 'Avenida Insurgentes', 'Calle Zaragoza'
            ]
        }
        
    def get_countries_with_postal_coverage(self) -> List[str]:
        """Get list of countries with postal code coverage."""
        valid_countries = []
        for code in self.SUPPORTED_COUNTRIES:
            try:
                nomi = pgeocode.Nominatim(country=code)
                data = nomi._data.copy()
                required_columns = ['postal_code', 'place_name', 'state_name']
                data = data.dropna(subset=required_columns)
                data = data[
                    data['postal_code'].astype(str).str.strip().ne('')
                    & data['place_name'].astype(str).str.strip().ne('')
                    & data['state_name'].astype(str).str.strip().ne('')
                ]
                self.postal_data_by_country[code] = data.to_dict('records')
                if self.postal_data_by_country[code]:
                    valid_countries.append(code)
            except (AttributeError, OSError, ValueError):
                continue
        
        self.countries_with_coverage = valid_countries
        print(f"Found {len(valid_countries)} countries with postal code coverage")
        return valid_countries
    
    def get_country_name_from_code(self, code: str) -> str:
        """Convert ISO country code to country name."""
        try:
            country = pycountry.countries.get(alpha_2=code)
            return country.name if country else code
        except:
            return code
    
    def generate_random_postal_code(self, country_code: str) -> str:
        """Generate a random postal code from the list for a country."""
        if country_code not in self.POSTAL_CODE_RANGES:
            return None
        
        postal_codes = self.POSTAL_CODE_RANGES[country_code]
        return random.choice(postal_codes)
    
    def get_postal_code_data(self, country_code: str, postal_code: str) -> Optional[Dict]:
        """Get geographic data for a postal code using pgeocode only (no API calls)."""
        cache_key = f"{country_code}_{postal_code}"
        
        if cache_key in self.postal_code_cache:
            return self.postal_code_cache[cache_key]
        
        try:
            nomi = pgeocode.Nominatim(country=country_code)
            result = nomi.query_postal_code(postal_code)
            
            if result is None or result.empty:
                self.postal_code_cache[cache_key] = None
                return None
            
            # Extract data from result
            place_name = result.get('place_name', '')
            state_name = result.get('state_name', '')
            latitude = result.get('latitude')
            longitude = result.get('longitude')
            
            # Validate we have meaningful data
            if pd.isna(place_name) or place_name == '' or pd.isna(state_name) or state_name == '':
                self.postal_code_cache[cache_key] = None
                return None
            
            # Extract city from place_name
            city_parts = str(place_name).split(',')
            city = city_parts[0].strip()
            
            if not city or city.lower() == 'unknown':
                self.postal_code_cache[cache_key] = None
                return None
            
            # Reject if state is unknown
            if state_name.lower() == 'unknown':
                self.postal_code_cache[cache_key] = None
                return None
            
            data = {
                'postal_code': result.get('postal_code', postal_code),
                'place_name': place_name,
                'state_name': state_name,
                'city': city,
                'latitude': latitude,
                'longitude': longitude
            }
            
            self.postal_code_cache[cache_key] = data
            return data
            
        except Exception as e:
            self.postal_code_cache[cache_key] = None
            return None
    
    def generate_random_street_address(self, country_code: str) -> str:
        """Generate a random street address (no API calls)."""
        street_name = random.choice(self.street_names[country_code])
        house_number = random.randint(1, 999)
        return f"{house_number} {street_name}"
    
    def generate_random_address(self, country_code: Optional[str] = None) -> Optional[Dict]:
        """Generate a single random address with validation (no API calls)."""
        if not self.countries_with_coverage:
            self.get_countries_with_postal_coverage()
        
        country_code = country_code or random.choice(self.countries_with_coverage)
        country_name = self.get_country_name_from_code(country_code)
        postal_data = random.choice(self.postal_data_by_country[country_code])
        place_name = str(postal_data['place_name']).split(',')[0].strip()
        county_name = postal_data.get('county_name')
        city = str(county_name).strip() if country_code == 'MX' and pd.notna(county_name) else place_name

        return {
            'Country Name': country_name,
            'State': str(postal_data['state_name']).strip(),
            'City': city,
            'Zipcode': str(postal_data['postal_code']).strip(),
            'Street Address': self.generate_random_street_address(country_code)
        }
    
    def generate_dataset(self, num_records: int = 5000) -> pd.DataFrame:
        """Generate dataset with specified number of records (optimized, no API calls)."""
        self.get_countries_with_postal_coverage()
        
        print(f"\nGenerating {num_records} synthetic address records (optimized, pgeocode only)...")
        self.records = [
            self.generate_random_address(self.countries_with_coverage[index % len(self.countries_with_coverage)])
            for index in range(num_records)
        ]
        random.shuffle(self.records)
        
        print(f"Successfully generated {len(self.records)} records")
        
        if self.records:
            df = pd.DataFrame(self.records)
            return df
        else:
            return pd.DataFrame()
    
    def save_to_csv(self, dataframe: pd.DataFrame, filename: str = 'synthetic_addresses.csv') -> str:
        """Save the generated data to a CSV file."""
        try:
            dataframe.to_csv(filename, index=False)
            print(f"\nData saved to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return None


def main():
    """Main execution function."""
    generator = SyntheticAddressGenerator()
    
    # Generate Canada and Mexico addresses only.
    df = generator.generate_dataset(num_records=5000)
    
    # Save to CSV
    if df is not None and len(df) > 0:
        generator.save_to_csv(df, 'synthetic_addresses_canada_mexico.csv')
        
        # Print summary
        print(f"\n=== Dataset Summary ===")
        print(f"Total records: {len(df)}")
        print(f"Columns: {', '.join(df.columns.tolist())}")
        
        # Check for NULL/Unknown values
        print(f"\n=== Data Quality Check ===")
        print(f"NULL values in State: {df['State'].isnull().sum()}")
        print(f"NULL values in City: {df['City'].isnull().sum()}")
        print(f"'Unknown' values in State: {(df['State'] == 'Unknown').sum()}")
        print(f"'Unknown' values in City: {(df['City'] == 'Unknown').sum()}")
        
        print(f"\nFirst 15 records:")
        print(df.head(15).to_string())
        print(f"\nCountries represented:")
        print(df['Country Name'].value_counts())
    else:
        print("Failed to generate dataset")


if __name__ == '__main__':
    main()
