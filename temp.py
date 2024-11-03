from datetime import datetime

today = datetime.today()
delete_time = today.timestamp() + 3600
delete_time = datetime.fromtimestamp(delete_time)
print(today.strftime("%d.%m.%Y %H:%M"))
print(delete_time)

