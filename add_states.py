import pandas as pd

# Hardcoded mapping of the 277 cities to their Indian States
city_to_state = {
    'Agartala': 'Tripura', 'Agra': 'Uttar Pradesh', 'Ahmedabad': 'Gujarat', 'Aizawl': 'Mizoram', 'Ajmer': 'Rajasthan',
    'Akola': 'Maharashtra', 'Alwar': 'Rajasthan', 'Amaravati': 'Andhra Pradesh', 'Ambala': 'Haryana', 'Amravati': 'Maharashtra',
    'Amritsar': 'Punjab', 'Anantapur': 'Andhra Pradesh', 'Angul': 'Odisha', 'Ankleshwar': 'Gujarat', 'Araria': 'Bihar',
    'Ariyalur': 'Tamil Nadu', 'Arrah': 'Bihar', 'Asansol': 'West Bengal', 'Aurangabad (Bihar)': 'Bihar', 'Aurangabad': 'Maharashtra',
    'Baddi': 'Himachal Pradesh', 'Badlapur': 'Maharashtra', 'Bagalkot': 'Karnataka', 'Baghpat': 'Uttar Pradesh', 'Bahadurgarh': 'Haryana',
    'Balasore': 'Odisha', 'Ballabgarh': 'Haryana', 'Banswara': 'Rajasthan', 'Baran': 'Rajasthan', 'Barbil': 'Odisha',
    'Bareilly': 'Uttar Pradesh', 'Baripada': 'Odisha', 'Barmer': 'Rajasthan', 'Barrackpore': 'West Bengal', 'Bathinda': 'Punjab',
    'Begusarai': 'Bihar', 'Belapur': 'Maharashtra', 'Belgaum': 'Karnataka', 'Bengaluru': 'Karnataka', 'Bettiah': 'Bihar',
    'Bhagalpur': 'Bihar', 'Bharatpur': 'Rajasthan', 'Bhilai': 'Chhattisgarh', 'Bhilwara': 'Rajasthan', 'Bhiwadi': 'Rajasthan',
    'Bhiwandi': 'Maharashtra', 'Bhiwani': 'Haryana', 'Bhopal': 'Madhya Pradesh', 'Bhubaneswar': 'Odisha', 'Bidar': 'Karnataka',
    'Bihar Sharif': 'Bihar', 'Bikaner': 'Rajasthan', 'Bilaspur': 'Chhattisgarh', 'Bileipada': 'Odisha', 'Brajrajnagar': 'Odisha',
    'Bulandshahr': 'Uttar Pradesh', 'Bundi': 'Rajasthan', 'Buxar': 'Bihar', 'Byasanagar': 'Odisha', 'Byrnihat': 'Meghalaya',
    'Chamarajanagar': 'Karnataka', 'Chandigarh': 'Chandigarh', 'Chandrapur': 'Maharashtra', 'Charkhi Dadri': 'Haryana', 'Chengalpattu': 'Tamil Nadu',
    'Chennai': 'Tamil Nadu', 'Chhal': 'Chhattisgarh', 'Chhapra': 'Bihar', 'Chikkaballapur': 'Karnataka', 'Chikkamagaluru': 'Karnataka',
    'Chittoor': 'Andhra Pradesh', 'Chittorgarh': 'Rajasthan', 'Churu': 'Rajasthan', 'Coimbatore': 'Tamil Nadu', 'Cuddalore': 'Tamil Nadu',
    'Cuttack': 'Odisha', 'Damoh': 'Madhya Pradesh', 'Darbhanga': 'Bihar', 'Dausa': 'Rajasthan', 'Davanagere': 'Karnataka',
    'Dehradun': 'Uttarakhand', 'Delhi': 'Delhi', 'Dewas': 'Madhya Pradesh', 'Dhanbad': 'Jharkhand', 'Dharuhera': 'Haryana',
    'Dharwad': 'Karnataka', 'Dholpur': 'Rajasthan', 'Dhule': 'Maharashtra', 'Dindigul': 'Tamil Nadu', 'Durgapur': 'West Bengal',
    'Eloor': 'Kerala', 'Ernakulam': 'Kerala', 'Faridabad': 'Haryana', 'Fatehabad': 'Haryana', 'Firozabad': 'Uttar Pradesh',
    'Gadag': 'Karnataka', 'GandhiNagar': 'Gujarat', 'Gangtok': 'Sikkim', 'Gaya': 'Bihar', 'Ghaziabad': 'Uttar Pradesh',
    'Gorakhpur': 'Uttar Pradesh', 'Greater Noida': 'Uttar Pradesh', 'Gummidipoondi': 'Tamil Nadu', 'Gurugram': 'Haryana', 'Guwahati': 'Assam',
    'Gwalior': 'Madhya Pradesh', 'Hajipur': 'Bihar', 'Haldia': 'West Bengal', 'Hanumangarh': 'Rajasthan', 'Hapur': 'Uttar Pradesh',
    'Hassan': 'Karnataka', 'Haveri': 'Karnataka', 'Hisar': 'Haryana', 'Hosur': 'Tamil Nadu', 'Howrah': 'West Bengal',
    'Hubballi': 'Karnataka', 'Hyderabad': 'Telangana', 'Imphal': 'Manipur', 'Indore': 'Madhya Pradesh', 'Jabalpur': 'Madhya Pradesh',
    'Jaipur': 'Rajasthan', 'Jaisalmer': 'Rajasthan', 'Jalandhar': 'Punjab', 'Jalgaon': 'Maharashtra', 'Jalna': 'Maharashtra',
    'Jalore': 'Rajasthan', 'Jhalawar': 'Rajasthan', 'Jhansi': 'Uttar Pradesh', 'Jharsuguda': 'Odisha', 'Jhunjhunu': 'Rajasthan',
    'Jind': 'Haryana', 'Jodhpur': 'Rajasthan', 'Jorapokhar': 'Jharkhand', 'Kadapa': 'Andhra Pradesh', 'Kaithal': 'Haryana',
    'Kalaburagi': 'Karnataka', 'Kalyan': 'Maharashtra', 'Kanchipuram': 'Tamil Nadu', 'Kannur': 'Kerala', 'Kanpur': 'Uttar Pradesh',
    'Karauli': 'Rajasthan', 'Karnal': 'Haryana', 'Karwar': 'Karnataka', 'Kashipur': 'Uttarakhand', 'Katihar': 'Bihar',
    'Katni': 'Madhya Pradesh', 'Keonjhar': 'Odisha', 'Khanna': 'Punjab', 'Khurja': 'Uttar Pradesh', 'Kishanganj': 'Bihar',
    'Kochi': 'Kerala', 'Kohima': 'Nagaland', 'Kolar': 'Karnataka', 'Kolhapur': 'Maharashtra', 'Kolkata': 'West Bengal',
    'Kollam': 'Kerala', 'Koppal': 'Karnataka', 'Korba': 'Chhattisgarh', 'Kota': 'Rajasthan', 'Kozhikode': 'Kerala',
    'Kunjemura': 'Chhattisgarh', 'Kurukshetra': 'Haryana', 'Latur': 'Maharashtra', 'Loni_Dehat': 'Uttar Pradesh', 'Loni_Ghaziabad': 'Uttar Pradesh',
    'Lucknow': 'Uttar Pradesh', 'Ludhiana': 'Punjab', 'Madikeri': 'Karnataka', 'Mahad': 'Maharashtra', 'Maihar': 'Madhya Pradesh',
    'Mandi Gobindgarh': 'Punjab', 'Mandideep': 'Madhya Pradesh', 'Mandikhera': 'Haryana', 'Manesar': 'Haryana', 'Mangalore': 'Karnataka',
    'Manguraha': 'Bihar', 'Medikeri': 'Karnataka', 'Meerut': 'Uttar Pradesh', 'Milupara': 'Chhattisgarh', 'Moradabad': 'Uttar Pradesh',
    'Motihari': 'Bihar', 'Mumbai': 'Maharashtra', 'Munger': 'Bihar', 'Muzaffarnagar': 'Uttar Pradesh', 'Muzaffarpur': 'Bihar',
    'Mysuru': 'Karnataka', 'Nagaon': 'Assam', 'Nagaur': 'Rajasthan', 'Nagpur': 'Maharashtra', 'Naharlagun': 'Arunachal Pradesh',
    'Nalbari': 'Assam', 'Nanded': 'Maharashtra', 'Nandesari': 'Gujarat', 'Narnaul': 'Haryana', 'Nashik': 'Maharashtra',
    'Navi Mumbai': 'Maharashtra', 'Nayagarh': 'Odisha', 'Noida': 'Uttar Pradesh', 'Ooty': 'Tamil Nadu', 'Pali': 'Rajasthan',
    'Palkalaiperur': 'Tamil Nadu', 'Palwal': 'Haryana', 'Panchkula': 'Haryana', 'Panipat': 'Haryana', 'Parbhani': 'Maharashtra',
    'Patiala': 'Punjab', 'Patna': 'Bihar', 'Pimpri Chinchwad': 'Maharashtra', 'Pithampur': 'Madhya Pradesh', 'Pratapgarh': 'Rajasthan',
    'Prayagraj': 'Uttar Pradesh', 'Puducherry': 'Puducherry', 'Pune': 'Maharashtra', 'Purnia': 'Bihar', 'Raichur': 'Karnataka',
    'Raipur': 'Chhattisgarh', 'Rairangpur': 'Odisha', 'Rajamahendravaram': 'Andhra Pradesh', 'Rajgir': 'Bihar', 'Rajsamand': 'Rajasthan',
    'Ramanagara': 'Karnataka', 'Ramanathapuram': 'Tamil Nadu', 'Ratlam': 'Madhya Pradesh', 'Rishikesh': 'Uttarakhand', 'Rohtak': 'Haryana',
    'Rourkela': 'Odisha', 'Rupnagar': 'Punjab', 'Sagar': 'Madhya Pradesh', 'Saharsa': 'Bihar', 'Salem': 'Tamil Nadu',
    'Samastipur': 'Bihar', 'Sangli': 'Maharashtra', 'Sasaram': 'Bihar', 'Satna': 'Madhya Pradesh', 'Sawai Madhopur': 'Rajasthan',
    'Shillong': 'Meghalaya', 'Shivamogga': 'Karnataka', 'Sikar': 'Rajasthan', 'Silchar': 'Assam', 'Siliguri': 'West Bengal',
    'Singrauli': 'Madhya Pradesh', 'Sirohi': 'Rajasthan', 'Sirsa': 'Haryana', 'Sivasagar': 'Assam', 'Siwan': 'Bihar',
    'Solapur': 'Maharashtra', 'Sonipat': 'Haryana', 'Sri Ganganagar': 'Rajasthan', 'Srinagar': 'Jammu & Kashmir', 'Suakati': 'Odisha',
    'Surat': 'Gujarat', 'Talcher': 'Odisha', 'Tensa': 'Odisha', 'Thane': 'Maharashtra', 'Thiruvananthapuram': 'Kerala',
    'Thoothukudi': 'Tamil Nadu', 'Thrissur': 'Kerala', 'Tiruchirappalli': 'Tamil Nadu', 'Tirupati': 'Andhra Pradesh', 'Tirupur': 'Tamil Nadu',
    'Tonk': 'Rajasthan', 'Tumakuru': 'Karnataka', 'Tumidih': 'Chhattisgarh', 'Udaipur': 'Rajasthan', 'Udupi': 'Karnataka',
    'Ujjain': 'Madhya Pradesh', 'Ulhasnagar': 'Maharashtra', 'Vapi': 'Gujarat', 'Varanasi': 'Uttar Pradesh', 'Vatva': 'Gujarat',
    'Vellore': 'Tamil Nadu', 'Vijayapura': 'Karnataka', 'Vijayawada': 'Andhra Pradesh', 'Visakhapatnam': 'Andhra Pradesh', 'Vrindavan': 'Uttar Pradesh',
    'Yadgir': 'Karnataka', 'Yamunanagar': 'Haryana'
}

print("Loading original dataset...")
df = pd.read_csv('india_aqi_2015_2023_all_cities.csv')

def get_state(city_raw):
    # Remove _AQIBulletins
    clean_city = str(city_raw).replace('_AQIBulletins', '').replace('%28','(').replace('%29',')')
    # Exact match
    if clean_city in city_to_state:
        return city_to_state[clean_city]
    
    # Try fuzzy matching (start)
    for k, v in city_to_state.items():
        if clean_city.startswith(k):
            return v
            
    return "Unknown State"

print("Mapping states...")
df['State'] = df['City'].apply(get_state)

print(f"Mapped {len(df[df['State'] != 'Unknown State'])} records successfully.")
unknowns = df[df['State'] == 'Unknown State']['City'].unique()
if len(unknowns) > 0:
    print(f"Unknown cities: {unknowns}")

# Reorder columns slightly to put State near City
cols = df.columns.tolist()
cols.insert(2, cols.pop(cols.index('State')))
df = df[cols]

output_file = 'india_aqi_with_states.csv'
df.to_csv(output_file, index=False)
print(f"Successfully saved to {output_file}!")
