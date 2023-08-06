# footballer_generator.py

import datetime
import random

class SameClubFootballerGenerator:
    def __init__(self, first_names, last_names, cities, club, position):
        self.first_names = first_names
        self.last_names = last_names
        self.cities = cities
        self.club = club
        self.position = position

    @staticmethod
    def generate_random_date_of_birth(start_year, end_year):
        start_date = datetime.date(start_year, 1, 1)
        end_date = datetime.date(end_year, 12, 31)
        random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        return random_date
    
    def generate_fake_club(self, club):
        club = random.choice(self.cities) + ' ' + random.choice(self.club)
        return club

    def generate_fake_footballer(self, nationality, position):
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        date_of_birth = self.generate_random_date_of_birth(1986, 2005)

        return {
            'first_name': first_name,
            'last_name': last_name,
            'position': position,
            'nationality': nationality,
            'club': club,
            'dob': date_of_birth
        }


# main.py
import datetime
import pandas as pd
import random
from footballer_generator import SameClubFootballerGenerator
from data import GER, SPA, ENG, ITA, position

# Prompt the user to choose the country
print("Available countries:")
print("1. England (ENG)")
print("2. Italy (ITA)")
print("3. Spain (SPA)")
print("4. Germany (GER)")

country_choice = input("Enter the number corresponding to the desired country: ")

# Map the user's choice to the country code
country_mapping = {
    '1': 'ENG',
    '2': 'ITA',
    '3': 'SPA',
    '4': 'GER'
}

# Validate the user's choice
if country_choice not in country_mapping:
    print("Invalid country choice. Exiting...")
    exit()

country = country_mapping[country_choice]

# Set up the SameClubFootballerGenerator based on the chosen country
if country == 'ENG':
    footballer_generator = SameClubFootballerGenerator(ENG[0], ENG[1], ENG[2], ENG[3], position)
elif country == 'ITA':
    footballer_generator = SameClubFootballerGenerator(ITA[0], ITA[1], ITA[2], ITA[3], position)
elif country == 'SPA':
    footballer_generator = SameClubFootballerGenerator(SPA[0], SPA[1], SPA[2], SPA[3], position)
elif country == 'GER':
    footballer_generator = SameClubFootballerGenerator(GER[0], GER[1], GER[2], GER[3], position)

# Each team has 24 players
num_footballers = 24

# Set the fixed number of players for each position
num_players_per_position = {
    'GK': 3,
    'LB': 2,
    'RB': 2,
    'CB': 4,
    'DM': 2,
    'CM': 2,
    'AM': 1,
    'LM': 2,
    'RM': 2,
    'ST': 4
}

# Generate the fake club
club = random.choice(footballer_generator.cities) + ' ' + random.choice(footballer_generator.club)

# Generate fake footballers with the same club and fixed number of players for each position
fake_footballers = []
for position, num_players in num_players_per_position.items():
    for _ in range(num_players):
        fake_footballer = footballer_generator.generate_fake_footballer(country, position)
        fake_footballers.append(fake_footballer)

# Create DataFrame from the list of footballers
df = pd.DataFrame(fake_footballers)

# Save DataFrame to Excel file
filename = f'fake_{country}_footballers.xlsx'
df.to_excel(filename, index=False)
print(f"Fake footballers data saved to {filename}:\n")
print(df)
