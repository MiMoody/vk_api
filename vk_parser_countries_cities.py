# https://vk.com/dev/database.getCities
import json
import time
from typing import NamedTuple, List
import vk_api as vk

VK_LOGIN:str = "login or phone"
VK_PASS:str = "password"

class Country(NamedTuple):
    id: int = None
    name: str = None

    def __str__(self) -> str:
        return self.name

class City(NamedTuple):
    name:str = None
    
    def __str__(self) -> str:
        return self.name

class CountryCities(NamedTuple):
    country_name: str = None
    cities: List[City] = None
    
    def __str__(self) -> str:
        return f"{self.country_name}: {self.cities}"


def get_cities(api:vk.vk_api.VkApiMethod, country:Country) -> CountryCities:
    """ Получает все города в стране """
    
    cities = api.database.getCities(country_id=country.id, need_all=1, count=1000)
    cities_name: List[City] = format_list_cities(cities['items'])
    for i in range(1000, cities['count'], 1000):
        cities = api.database.getCities(country_id=country.id, need_all=1, offset=i, count=1000)['items']
        cities_name += format_list_cities(cities)
    return CountryCities(country_name=country.name, cities=cities_name)

def get_countries(api)-> List[Country]:
    """ Получает все страны """
    
    countries = api.database.getCountries(need_all=1, count=1000)['items']
    return [Country(id = country['id'], name = country['title']) for country in countries]

def format_list_cities(cities:dict) -> List[City]:
    """ Формирует список городов """
    
    return [City(name=city["title"]) for city in cities if city.get("title")]



if __name__ == '__main__':
    start = time.time()
    vk_session = vk.VkApi(f'{VK_LOGIN}', f'{VK_PASS}')
    vk_session.auth()
    api:vk.vk_api.VkApiMethod = vk_session.get_api()
    
    countries: List[Country] = get_countries(api)
    countries_cities: List[CountryCities] = [get_cities(api, country) for country in countries]
    data = {}
    for country_cities in countries_cities:
        data[country_cities.country_name] = [city.name for city in  country_cities.cities]
    
    with open("countries_cities.json", "w") as file:
        json.dump(data, file)
    
    with open("countries_cities.json", "r") as file:
        data = json.load(file)
        
    print('{} sec'.format(time.time() - start))
    