from datetime import datetime
date_str = '2023-04-01'
date_object = datetime.strptime(date_str, '%Y-%m-%d')

print(date_object)