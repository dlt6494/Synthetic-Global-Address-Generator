import pandas as pd

# Load and analyze the new CSV
df = pd.read_csv('synthetic_addresses.csv')

print("=" * 80)
print("DATA QUALITY REPORT - IMPROVED VERSION")
print("=" * 80)

print(f"\nTotal Records: {len(df)}")
print(f"\n1. NULL VALUES ANALYSIS")
null_counts = df.isnull().sum()
null_percent = (null_counts / len(df) * 100).round(2)

print(f"   Column              | NULL Count | NULL %")
print(f"   {'-'*47}")
print(f"   Country Name        | {null_counts['Country Name']:10d} | {null_percent['Country Name']:6.2f}%")
print(f"   State               | {null_counts['State']:10d} | {null_percent['State']:6.2f}%")
print(f"   City                | {null_counts['City']:10d} | {null_percent['City']:6.2f}%")
print(f"   Zipcode             | {null_counts['Zipcode']:10d} | {null_percent['Zipcode']:6.2f}%")
print(f"   Street Address      | {null_counts['Street Address']:10d} | {null_percent['Street Address']:6.2f}%")
print(f"   {'-'*47}")
print(f"   TOTAL NULL VALUES   | {null_counts.sum():10d} | {(null_counts.sum() / (len(df) * 5) * 100):6.2f}%")

print(f"\n2. DATA COMPLETENESS")
print(f"   Records with ALL fields populated: {len(df[df.isnull().sum(axis=1) == 0])} / {len(df)} ({(len(df[df.isnull().sum(axis=1) == 0]) / len(df) * 100):.1f}%)")

print(f"\n3. SAMPLE DATA (First 10 rows)")
print(df.head(10).to_string())

print(f"\n4. COMPARISON WITH PREVIOUS VERSION")
print(f"   BEFORE (Original):  State NULL: 365, City NULL: 313, Total NULL: 678")
print(f"   AFTER (Improved):   State NULL: {null_counts['State']}, City NULL: {null_counts['City']}, Total NULL: {null_counts.sum()}")
improvement = 678 - null_counts.sum()
print(f"   IMPROVEMENT:        {improvement} fewer NULL values ({(improvement/678*100):.1f}% reduction)")

print(f"\n" + "=" * 80)
