"""
Code witch create json file named records_json.json. File records_json.json
is used to display events in celandar depend on type and date.
"""

import sqlite3
import json
import collections

conn = sqlite3.connect('app.db')
cursor = conn.cursor()
cursor.execute('select Name, StartTime, EndTime, Color from Event '
               'inner join EventType on EventType.Id = Event.EventTypeId order by StartTime;')
rows = cursor.fetchall()

rowarray_list = []
for row in rows:
    t = (row[0], row[1], row[2], row[3])
    rowarray_list.append(t)


rowarrays_file = '../records_json.json'
f = open(rowarrays_file, 'w')

objects_list = []
for row in rows:
    d = collections.OrderedDict()
    d['title'] = row[0]
    d['start'] = row[1]
    d['end'] = row[2]
    d['color'] = row[3]

    objects_list.append(d)

j = json.dumps(objects_list)
objects_file = '../records_json.json'
with open(objects_file, 'r+') as file:
    file.write(j)

conn.close()
