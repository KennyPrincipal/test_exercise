import prettytable
import requests


class Country:
    def __init__(self, country_name):
        self.country_name = country_name
        self.official_name = None
        self.capital = None
        self.flag_link_png = None
        self.get_country_data()

    def get_country_data(self):
        response = requests.get(f"https://restcountries.com/v3.1/name/{self.country_name}?fullText=true").json()
        self.official_name = response[0]['name']['official']
        self.capital = response[0]['capital'][0]
        self.flag_link_png = response[0]['flags']['png']

    def display_country_data(self):
        table = prettytable.PrettyTable()
        table.field_names = ["Назва країни", "Назва столиці", "Посилання на зображення прапору"]
        table.add_row([self.official_name, self.capital, self.flag_link_png])
        print(table)


country = Country("Ukraine")
country.display_country_data()




