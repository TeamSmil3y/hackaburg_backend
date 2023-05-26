from ..models import *
import re
"""
with open("main/dataset/ratisbona-companies.csv", "r") as f:
    r = f.readlines()

Company.objects.all().delete()
Hub.objects.all().delete()

for line in r[1:]:
    print(line)
    c_id, street, street_number, city, postal_code, lat, lon, name = line.split(",", 7)
    

        
    h, created = Hub.objects.get_or_create(
        latitude=float(lat),
        longitude=float(lon),
    )
    Company.objects.create(
        id=c_id,
        name=name,
        adress=f"{street} {street_number}, {postal_code} {city}",
        hub=h
    )
    
"""
with open("main/dataset/people-with-companies.csv", "r") as f:
    r = f.readlines()
    

User.objects.filter(is_superuser=False).delete()

for line in r[1:]:
    print(line)
    if len(line.split(",")) > 12:
        line = re.sub(r'"[^"]+"', line.split('"')[1].replace(",", ";"), line)
        print("###", line)
    
    u_id, first_name, last_name, email, gender, street, street_number, city, postal_code, lat, lon, company_id = line.split(",")
    if gender not in ("Male", "Female"):
        gender = "D"
    User.objects.create_user(
        email=email,
        password="password",
        gender={"Male": "M", "Female": "F", "D": "D"}[gender],
        adress=f"{street} {street_number}, {postal_code} {city}",
        first_name=first_name,
        last_name=last_name,
        latitude=lat,
        longitude=lon,
        company_id=company_id
    )
    