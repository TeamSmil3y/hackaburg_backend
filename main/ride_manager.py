from .models import Ride, Hub, Ride2Passengers
from django.db.models import Q
import numpy as np
import uuid

from math import acos, pi, exp

# get ride by id
def get_ride(id):
    return Ride.objects.get(id=id)


# get all rides
def get_all_rides():
    return Ride.objects.all()


# user join ride
def join_ride(ride, user, hub):
    Ride2Passengers.objects.create(ride=ride, passenger=user, source_hub=hub)


# get hub from id
def get_hub(id):
    Hub.objects.get(id=id)


# function will return a list of ride requests that are relevant to the input ride request
def find_relevant_rides(source_hub, destination_hub):
    def threshold(x, a=(pi / 2)):
        return ((2*pi - a) * exp(-.5*x)) + a

    # get all rides with same destination
    relevant_rides = Ride.objects.filter(destination_hub=destination_hub)
    relevant_rides_ids = []
    for ride in relevant_rides:
        vector_a = source_hub.get_vector(destination_hub)
        vector_b = ride.get_vector()
        
        angle = acos(np.dot(vector_a, vector_b)/(sqrt(vector_a[0]**2 + vector_a[1]**2)*sqrt(vector_b[0]**2 + vector_b[1]**2)))

        print("angle", angle)
        
        if angle <= threshold(source_hub-destination_hub):
            relevant_rides_ids.append(ride.id)
            
    relevant_rides = Ride.objects.filter(id__in=relevant_rides_ids)
    
    return relevant_rides