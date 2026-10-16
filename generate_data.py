import pandas as pd
import numpy as np
import random
import string
import json

# Set seed for reproducibility
np.random.seed(42)

# Massive banks of distinct names to ensure zero unintended repeats
male_first = ["Joseph", "Emmanuel", "Samuel", "David", "Daniel", "Brian", "Moses", "John", "Peter", "Michael", "Robert", "Paul", "Kato", "Wasswa", "Ivan", "Ronald", "Patrick", "Julius", "Martin", "Ainebyona", "Tumusiime", "Mugisha", "Kizza", "Wycliffe", "Amos", "Erias", "Frank", "Geoffrey", "Hassan", "Ibrahim", "Benard", "Gilbert", "Rogers", "Enock", "Alex", "Jackson", "Denis", "Richard", "Kenneth", "Tonny"]
female_first = ["Mary", "Sarah", "Grace", "Betty", "Florence", "Prossy", "Justine", "Christine", "Lillian", "Phionah", "Esther", "Babirye", "Nakato", "Ritah", "Joan", "Amina", "Brenda", "Caroline", "Diana", "Evelyn", "Fatumah", "Gertrude", "Hellen", "Isabella", "Jovia", "Annet", "Doreen", "Hilda", "Juliet", "Racheal"]
middle_names = ["Katumba", "Kigozi", "Kakooza", "Wamani", "Mwesigwa", "Ssebuwufu", "Kiggundu", "Mwanje", "Luggya", "Kayanja", "Nsubuga", "Walusimbi", "Ssebagala", "Kibirige", "Muwanguzi", "Magumba", "Waiswa", "Isabirye", "Kaddu", "Katogo"]
surnames = ["Mukasa", "Kizito", "Akello", "Tusiime", "Asiimwe", "Byaruhanga", "Namaganda", "Nalubega", "Nankya", "Musisi", "Ssenyonga", "Muwonge", "Kintu", "Nanteza", "Namubiru", "Nakalema", "Nambooze", "Nantege", "Namusoke", "Nalwoga", "Otim", "Okello", "Opio", "Odongo", "Kansiime", "Tumukunde", "Atuhaire", "Ninsiima", "Mbabazi", "Ampaire"]

district_coords = {
    'Central': {
        'Buikwe': (0.3333, 33.0333), 'Bukomansimbi': (-0.1667, 31.6167), 'Butambala': (0.2333, 32.0500), 
        'Buvuma': (-0.2500, 33.2667), 'Gomba': (0.1667, 31.7500), 'Kalangala': (-0.6167, 32.2500), 
        'Kalungu': (-0.0833, 31.8167), 'Kampala': (0.3476, 32.5825), 'Kassanda': (0.5500, 31.8167), 
        'Kayunga': (0.7000, 32.9000), 'Kiboga': (0.8833, 31.7667), 'Kyankwanzi': (1.1500, 31.5333), 
        'Kyotera': (-0.6333, 31.5167), 'Luweero': (0.8333, 32.5000), 'Lwengo': (-0.4000, 31.4167), 
        'Lyantonde': (-0.4000, 31.1500), 'Masaka': (-0.3333, 31.7333), 'Mityana': (0.4000, 32.0333), 
        'Mpigi': (0.2333, 32.3333), 'Mubende': (0.5667, 31.4000), 'Mukono': (0.3500, 32.7500), 
        'Nakaseke': (0.7333, 32.4167), 'Nakasongola': (1.3167, 32.4500), 'Rakai': (-0.7167, 31.4000), 
        'Sembabule': (-0.0833, 31.4667), 'Wakiso': (0.4000, 32.4833)
    },
    'Western': {
        'Buhweju': (-0.3333, 30.3000), 'Buliisa': (2.1333, 31.4000), 'Bundibugyo': (0.7000, 30.0667), 
        'Bunyangabu': (0.5667, 30.2500), 'Bushenyi': (-0.5333, 30.1833), 'Fort Portal': (0.6500, 30.2667), 
        'Hoima': (1.4333, 31.3500), 'Ibanda': (-0.1333, 30.5000), 'Isingiro': (-0.8333, 30.8000), 
        'Kabale': (-1.2500, 30.0000), 'Kagadi': (0.9333, 30.8000), 'Kakumiro': (0.7833, 31.3167), 
        'Kamwenge': (0.1833, 30.4500), 'Kanungu': (-0.8500, 29.7833), 'Kasese': (0.1833, 30.0833), 
        'Kazo': (-0.0500, 30.7667), 'Kibaale': (0.8000, 31.0833), 'Kikuube': (1.4167, 31.1167), 
        'Kiruhura': (-0.2000, 30.9833), 'Kiryandongo': (1.8667, 32.0667), 'Kisoro': (-1.2833, 29.6833), 
        'Kyegegwa': (0.4833, 31.0500), 'Kyenjojo': (0.6167, 30.6333), 'Masindi': (1.6833, 31.7167), 
        'Mbarara': (-0.6000, 30.6500), 'Mitooma': (-0.5833, 30.0000), 'Ntoroko': (1.0333, 30.3833), 
        'Ntungamo': (-0.8833, 30.2667), 'Rubanda': (-1.1833, 29.8333), 'Rubirizi': (-0.2667, 30.1000), 
        'Rukiga': (-1.1500, 30.0500), 'Rukungiri': (-0.7833, 29.9333), 'Rwampara': (-0.7667, 30.4333), 
        'Sheema': (-0.5833, 30.3667)
    },
    'Eastern': {
        'Amuria': (2.0333, 33.6333), 'Budaka': (1.0167, 33.9500), 'Bududa': (1.0500, 34.3333), 
        'Bugiri': (0.5667, 33.7500), 'Bugweri': (0.5833, 33.6000), 'Bukedea': (1.3333, 34.0500), 
        'Bukwo': (1.2833, 34.7167), 'Bulambuli': (1.1500, 34.3833), 'Busia': (0.4667, 34.0833), 
        'Butebo': (1.2167, 33.9167), 'Buyende': (1.1500, 33.1667), 'Iganga': (0.6167, 33.4833), 
        'Jinja': (0.4333, 33.2000), 'Kaberamaido': (1.7500, 33.1500), 'Kalaki': (1.8500, 33.3500), 
        'Kaliro': (0.9000, 33.5000), 'Kamuli': (0.9500, 33.1167), 'Kapchorwa': (1.4000, 34.4500), 
        'Kapelebyong': (2.3333, 33.8000), 'Katakwi': (1.9167, 34.0000), 'Kibuku': (1.0333, 33.8333), 
        'Kumi': (1.5000, 33.9333), 'Kween': (1.4167, 34.5167), 'Luuka': (0.7167, 33.3333), 
        'Manafwa': (0.9000, 34.3167), 'Mayuge': (0.4500, 33.4833), 'Mbale': (1.0833, 34.1833), 
        'Namayingo': (0.3000, 33.8833), 'Namisindwa': (0.8333, 34.3833), 'Namutumba': (0.8333, 33.6833), 
        'Ngora': (1.4500, 33.7667), 'Pallisa': (1.1667, 33.7167), 'Serere': (1.5000, 33.4500), 
        'Sironko': (1.2333, 34.2500), 'Soroti': (1.7167, 33.6167), 'Tororo': (0.7000, 34.1833)
    },
    'Northern': {
        'Abim': (2.7333, 33.6667), 'Adjumani': (3.3833, 31.7833), 'Agago': (2.8333, 33.3333), 
        'Alebtong': (2.2500, 33.3000), 'Amolatar': (1.6333, 32.8333), 'Amudat': (1.9500, 34.9500), 
        'Amuru': (2.8167, 31.9333), 'Apac': (1.9833, 32.5333), 'Arua': (3.0333, 30.9167), 
        'Dokolo': (1.9167, 33.1667), 'Gulu': (2.7667, 32.3000), 'Kaabong': (3.5167, 34.1167), 
        'Karenga': (3.5000, 33.8000), 'Kitgum': (3.2833, 32.8833), 'Koboko': (3.4167, 30.9667), 
        'Kole': (2.3667, 32.8000), 'Kotido': (3.0167, 34.1167), 'Kwania': (1.9000, 32.7500), 
        'Lamwo': (3.5333, 32.8000), 'Lira': (2.2500, 32.9000), 'Madi-Okollo': (2.8500, 31.1333), 
        'Maracha': (3.2333, 30.9333), 'Moroto': (2.5333, 34.6667), 'Moyo': (3.6500, 31.7167), 
        'Nabilatuk': (2.1333, 34.6000), 'Nakapiripirit': (1.8500, 34.7167), 'Napak': (2.1500, 34.2833), 
        'Nebbi': (2.4833, 31.0833), 'Nwoya': (2.6333, 31.9000), 'Obongi': (3.3667, 31.4167), 
        'Omoro': (2.5667, 32.3667), 'Otuke': (2.4833, 33.1500), 'Oyam': (2.3833, 32.3833), 
        'Pader': (2.9000, 33.0833), 'Pakwach': (2.4667, 31.4000), 'Terego': (3.1667, 31.0667), 
        'Yumbe': (3.4667, 31.2500), 'Zombo': (2.5000, 30.9000)
    }
}

loan_platforms_mtn = ["MTN MoMo Advance", "MoKash (MTN)", "Centenary Mobile (MTN)", "Finca Mobile (MTN)"]
loan_platforms_airtel = ["Airtel QuickLoan", "Wewole (Airtel)", "Stanbic Incubator (Airtel)", "Pride Microfinance (Airtel)"]

num_records = 15000 
data = []
generated_names = set()

for _ in range(num_records):
    gender = random.choice(['Male', 'Female'])
    
    # Enforce strict uniqueness and structural variety (some 2 names, some 3 names)
    while True:
        f_name = random.choice(male_first) if gender == 'Male' else random.choice(female_first)
        s_name = random.choice(surnames)
        
        # 50% chance to include a middle/clan name for variety
        if random.choice([True, False]):
            mid_name = random.choice(middle_names)
            borrower_name = f"{f_name} {mid_name} {s_name}"
        else:
            borrower_name = f"{f_name} {s_name}"
            
        if borrower_name not in generated_names:
            generated_names.add(borrower_name)
            break
            
    nin_prefix = 'CM' if gender == 'Male' else 'CF'
    nin_suffix = ''.join(random.choices(string.digits, k=7)) + ''.join(random.choices(string.ascii_uppercase, k=5))
    national_id = nin_prefix + nin_suffix
    
    mtn_number = f"+256 {random.choice(['77', '78', '76'])}{random.randint(1000000, 9999999)}"
    airtel_number = f"+256 {random.choice(['75', '70'])}{random.randint(1000000, 9999999)}"

    region = random.choice(list(district_coords.keys()))
    district = random.choice(list(district_coords[region].keys()))
    lat, lon = district_coords[region][district]
    lat += np.random.normal(0, 0.04)
    lon += np.random.normal(0, 0.04)
    
    age = np.random.randint(18, 60)
    
    if region == 'Central':
        income_source = random.choices(['Informal Trade', 'Salary', 'Services'], weights=[0.5, 0.3, 0.2])[0]
        monthly_income = max(100000, round(np.random.normal(600000, 200000), -3))
        active_loans = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.2, 0.3, 0.2, 0.15, 0.1, 0.05]) if age < 35 else np.random.choice([0, 1, 2, 3], p=[0.5, 0.3, 0.15, 0.05])
    else:
        income_source = random.choices(['Agriculture', 'Informal Trade', 'Salary'], weights=[0.6, 0.3, 0.1])[0]
        monthly_income = max(100000, round(np.random.normal(300000, 100000), -3))
        active_loans = np.random.choice([0, 1, 2, 3], p=[0.5, 0.3, 0.15, 0.05])
        
    total_debt = 0
    loans_list = []
    
    if active_loans > 0:
        for i in range(active_loans):
            network = random.choice(['MTN', 'Airtel'])
            platform = random.choice(loan_platforms_mtn) if network == 'MTN' else random.choice(loan_platforms_airtel)
            
            days_ago = random.randint(1, 45)
            hour = random.randint(8, 20)
            minute = random.randint(0, 59)
            disbursal_dt = pd.Timestamp("2026-10-16") - pd.Timedelta(days=days_ago) - pd.Timedelta(hours=hour, minutes=minute)
            disbursal_str = disbursal_dt.strftime("%Y-%m-%d %H:%M")
            
            due_dt = disbursal_dt + pd.Timedelta(days=30)
            due_str = due_dt.strftime("%Y-%m-%d")
            
            amount = round(np.random.uniform(30000, 150000), -3)
            total_debt += amount
            
            loans_list.append({
                "Platform": platform,
                "Network": network,
                "Disbursed": disbursal_str,
                "Due_Date": due_str,
                "Amount_UGX": amount
            })

    total_debt = round(total_debt, -3)
    dti_ratio = total_debt / monthly_income if monthly_income > 0 else 0
    default_status = np.random.choice([1, 0], p=[0.8, 0.2]) if (dti_ratio > 0.4 and active_loans > 1) else np.random.choice([1, 0], p=[0.1, 0.9])
    momo_tx_count = int(max(1, np.random.normal(15, 10) if region == 'Central' else np.random.normal(5, 3)))

    data.append([
        f"USR_{random.randint(10000, 99999)}", borrower_name, national_id, mtn_number, airtel_number, gender, 
        region, district, lat, lon, age, income_source, monthly_income, 
        active_loans, total_debt, dti_ratio, momo_tx_count, default_status, json.dumps(loans_list)
    ])

columns = [
    'Borrower_ID', 'Borrower_Name', 'National_ID_Number', 'MTN_Phone', 'Airtel_Phone', 'Gender', 'Region', 
    'District', 'Latitude', 'Longitude', 'Age', 'Income_Source', 'Monthly_Income_UGX', 
    'Active_Digital_Loans', 'Total_Debt_UGX', 'Debt_to_Income_Ratio', 
    'MoMo_Monthly_Tx_Count', 'Default_Status', 'Loans_JSON'
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("uganda_digital_debt_data.csv", index=False)
print("Success! Dataset generated with 100% unique, non-repeating names (mixed two-part and three-part names).")
