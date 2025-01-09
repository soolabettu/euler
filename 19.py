#!/usr/bin/env python

from datetime import date, timedelta

# Get today's date
today = date.today()

# Subtract 7 days
new_date = today - timedelta(days=2)

import re
cnt = 0
while True:
    new_date = new_date - timedelta(days=7)
    date_str = str(new_date)
    parts = re.split('-', date_str)
    if int(parts[0]) < 1901:
        break

    if int(parts[0]) <=2000 and int(parts[2]) == 1:
        cnt += 1
    
print(cnt)