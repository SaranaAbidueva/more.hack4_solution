import requests
import csv

limit = 5
offset = 0

url = f'https://api.forbes.ru/api/pub/lists/biznes?list%5Blimit%5D={limit}&list%5Boffset%5D={offset}'

response = requests.get(url)

data = response.json()

print(len(data['articles']))

with open('forbes_news.csv','a') as file:
    writer = csv.writer(file)
    writer.writerow([''])