import time
from datetime import datetime, date, timedelta

t1 = datetime.now()
time.sleep(2)
t2 = datetime.now()
print(t1-t2)
if t2 - t1 > timedelta(seconds=1):
    print('ok')