from datetime import datetime, date, time, timedelta


utc_time = datetime.now()
print(utc_time.isoformat())

# print(utc_time.year)
# print(utc_time.month)
# print(utc_time.day)
# print(utc_time.hour)
# print(utc_time.minute)

# some_datetime = datetime.datetime(year=1999, month=10, day=13, hour=14, minute=9)

# print(some_datetime)

# current_date = current_datetime.date()
# print(current_date)

# day_ago = current_datetime - datetime.timedelta(days=1)

# print(day_ago)

# print(current_datetime.strftime('%A, %d %B %Y'))


d = date(2023,3,4)
print(d.strftime("%Y-%m-%d %H:%M:%S"))

text = "2025-12-11 15:30"

print(datetime.strptime(text,"%Y-%m-%d %H:%M"))

d1 = datetime(2024, 9, 2)
d2 = datetime(2025, 9, 2)

dff = d2 - d1

print(dff.days)
print(dff.seconds)

now = datetime.now()

future = now + timedelta(days=3)

print(future)

start = datetime.now()

end = datetime.now()

print(end - start)

print(datetime.strptime("2025-01-01", "%Y-%m-%d"))

print(datetime.fromtimestamp(end))

async def add(username: str, date_born: str, file: UploadFile = File(...) , db: Session = Depends(get_db)):
    file_path = f'upload/{file.filename}'
    with open(file_path, 'wb') as f:
        f.write(await file.read())
    date_reg = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_borns = datetime.strptime(date_born, '%Y-%m-%d').date()
    today = date.today()
    age = today.year - date_borns.year - ( (today.month, today.day) < (date_borns.month, date_borns.day))
    user_db = User(username=username, file=file.filename, date_reg=date_reg, date_born=date_borns, age=age)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db