import json
import re
import geocoder
import random
from textblob import TextBlob

table = []
output = []

with open('stream__hurricanemaria1.json', 'r') as data_file:
    for line in data_file:
        table.append(json.loads(line))
i = 1
cities = dict()
for row in table:
    tim = row['created_at']
    index = tim.find('+')
    tim = tim[:index-1:]

    location = row['user']['location']
    if location is None:
        continue
    else:
        location = location.lower()

    if str(location) == 'None' or '➡' in str(location):
        lat_lng = (0.0, 0.0)
    else:
        if location in cities:
            lat_lng = cities[location]
        else:
            lat_lng = geocoder.google(location).latlng
            if not lat_lng:
                lat_lng = (0.0, 0.0)
            else:
                lat_lng[0] = lat_lng[0] + random.randrange(-1, 1) * 0.1
                lat_lng[1] = lat_lng[1] + random.randrange(-1, 1) * 0.1
            cities[location] = lat_lng

    text = row['text']
    if text[0] == 'R' and text[1] == 'T':
        index = text.find(': ')
        text = text[index+2:]
    text = re.sub(r'http\S+', '', text)

    sentiment = (TextBlob(text).sentiment.polarity + 1.0) / 2.0
    output.append({'sentiment': sentiment, 'latitude': lat_lng[0], 'longitude': lat_lng[1], 'time_stamp': tim})

with open('OutputData.json', 'w') as f:
    f.write(json.dumps(output))
    print('Done')
