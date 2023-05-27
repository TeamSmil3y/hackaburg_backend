import datetime

from .models import Hub, User, Ride, Company, Ride2Passengers


# calculates amount of points for ride
def calc_points(ride: Ride):
    workload = get_hub_workload(ride.destination_hub, day=ride.destination_time.weekday(), hour=ride.destination_time.hour)
    passenger_multiplier = len(Ride2Passengers.objects.filter(ride=ride))
    points = int((100-workload)*10*passenger_multiplier)
    return points


# returns true if general workload above threshold, company workload above threshold
def calc_points_warning(ride: Ride):
    dt = datetime.datetime.now()
    today = dt.weekday()
    hour = dt.hour
    
    hub_workload = get_hub_workload(ride.destination_hub, hour=hour, day=today)

    passengers = Ride2Passengers.objects.filter(ride=ride)
    if len(passengers) > 0:
        company_workload = sum([get_company_workload(i.user.company, hour=hour,day=today) for i in passengers]) / len(passengers)
        company_workload = (company_workload + get_company_workload(ride.driver.company, hour=hour, day=today)) / 2

    else:
        company_workload = get_company_workload(ride.driver.company, hour=hour, day=today)


    threshold = 0.5
    return hub_workload > threshold, company_workload > threshold


# returns data for all ride destinations
def calc_trueload():
    hubs = dict()
    for ride in Ride.objects.all():
        if ride.destination_hub not in hubs: hubs[ride.destination_hub] = 0
        hubs[ride.ride.destination_hub] += 1
    return hubs


# returns hub workload as specified by data
def get_hub_workload(hub: Hub, day: int, hour: int):
    companies = Company.objects.filter(hub=hub)
    workload = 0
    for company in companies:
        workload += get_company_workload(company, day, hour)
    return workload

# returns hub workload for company
def get_company_workload(company: Company, day: int, hour: int):
    return company[day, hour]
