import unidecode
import pandas as pd
from datetime import datetime

d = [{'cont': 'North America', 'cc': 'US', 'river': 'Missisipi', 'len': 6275},
     {'cont': 'North America', 'cc': 'US', 'river': 'Rio Grande', 'len': 3034},
     {'cont': 'North America', 'cc': 'US', 'river': 'Yukon', 'len': 3184},
     {'cont': 'Asia', 'cc': 'CN', 'river': 'Yangcy', 'len': 6300},
     {'cont': 'Asia', 'cc': 'CN', 'river': 'Mekong', 'len': 4500},
     {'cont': 'Asia', 'cc': 'CN', 'river': 'HuangHe', 'len': 5464},
     {'cont': 'Asia', 'cc': 'IN', 'river': 'Indus', 'len': 3180},
     {'cont': 'Asia', 'cc': 'IN', 'river': 'Ganges', 'len': 2510},
     {'cont': 'South America', 'cc': 'BR', 'river': 'Amazon', 'len': 6400},
     {'cont': 'Africa', 'cc': 'EG', 'river': 'Nile', 'len': 6695}]

d2 = {'USA': {'capital': 'Washington', 'curr': 'USD'},
      'GER': {'capital': 'Berlin', 'curr': 'EUR'},
      'ESP': {'capital': 'Madrid', 'curr': 'EUR'},
      'POL': {'capital': 'Warsaw', 'curr': 'PLN'},
      'JAP': {'capital': 'Tokio', 'curr': 'JPY'}}

# print(list(d2.keys()))
# a = list(d2.values())

times_list = ["00:00:41.38", "00:01:29.11", "00:02:20.91", "00:03:09.54"]


print(get_split_times(times_list))