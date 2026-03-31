import pandas as pd
import json

df = pd.read_excel('population.xlsx', header=None)

# Step 1: Find the column containing 'INDIA' (usually Area Name)
name_col = None
for c in df.columns:
    if df[c].astype(str).str.contains('INDIA').any():
        name_col = c
        break

if name_col is None:
    print("Could not find Area Name column.")
    exit()

# Step 2: Find the population column. Usually it's the 4th or 5th numerical column, or the one with the highest max.
# By Indian census standard: Col 1(State), Col 2(District), Col 3(Sub), Col 4(Town/Vill), Col 5(Ward), Col 7(Name), Col 8(TRU), Col 9(No_HH), Col 10(TOT_P)
# We will just guess based on standard structure. Let's find the numeric column that has the highest max value (India's pop = 1,210,854,977)
pop_col = None
max_val = 0
for c in df.columns:
    nums = pd.to_numeric(df[c], errors='coerce').fillna(0)
    if nums.max() > max_val:
        max_val = nums.max()
        pop_col = c

print(f"Name column: {name_col}, Population column: {pop_col}")

# Step 3: Extract mapping
mapping = {}
for _, row in df.iterrows():
    name = str(row[name_col]).strip().lower()
    pop = pd.to_numeric(row[pop_col], errors='coerce')
    if pd.notna(pop) and name != 'nan':
        mapping[name] = pop

# Filter out small irrelevant things if we want, but keeping all is fine
with open("pop_mapping.json", "w") as f:
    json.dump(mapping, f, indent=2)

print("Saved pop_mapping.json! Extracted", len(mapping), "entries.")
