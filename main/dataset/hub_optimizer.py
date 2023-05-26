from ..models import Hub, Company
from django.db.models import Q

threshold = 0.01 # in km

hubs = Hub.objects.all()

for hub1 in hubs:
    for hub2 in hubs:
        if hub1 - hub2 < threshold:
            print(hub1 - hub2)
            #latitude, longitude = hub1 // hub2
            #hub3 = Hub.objects.create(longitude=longitude, latitude=latitude)
            #for i in Company.objects.filter(Q(hub=hub1)|Q(hub=hub2)):
            #    i.hub = hub3
            #    i.save()
                
                
b = True

while b:
    for hub1 in hubs:
        for hub2 in hubs:
            if hub1 - hub2 < threshold:
                print(hub1 - hub2)
                latitude, longitude = hub1 // hub2
                hub3 = Hub.objects.create(longitude=longitude, latitude=latitude)
                for i in Company.objects.filter(Q(hub=hub1)|Q(hub=hub2)):
                    i.hub = hub3
                    i.save()
                break
        else:
            continue
        break
    else:
        b = False
    
                

for hub in Hub.objects.all():
    if len(Company.objects.filter(hub=hub)) == 0:
        hub.delete()
        