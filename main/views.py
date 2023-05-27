from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .view_utils import *
from .models import User
from .ride_manager import *
from .update_manager import *
from .ride_workload_calc import *
from django.core import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


# login
@api_view(['POST'])
@http_post_required_params(['username', 'password'])
def user_login(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if not user: return Response(data={"error": "wrong credentials or serverside error"}, status=400)
    return Response(status=200)

# logout
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    user = request.user
    logout(user)
    return Response(status=200)


# signup
@api_view(['POST'])
def user_signup(request):
    ...


# request ride
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@http_post_required_params(['source_hub_id', 'destination_hub_id'])
def create_ride(request):
    source_hub_id = request.POST['source_hub_id']
    source_hub = Hub.objects.get(id=source_hub_id)
    destination_hub_id = request.POST['destination_hub_id']
    destination_hub = Hub.objects.get(id=destination_hub_id)
    driver = request.user
    
    ride = Ride.objects.create(source_hub=source_hub, destination_hub=destination_hub, driver=driver)

    ride.points = calc_points(ride)
    ride.save()

    low_points, company_low_points = calc_points_warning(ride)
    return Response({"ride": serializers.serialize("json", [ride]), "low_points_warning": low_points, "company_low_points": company_low_points}, status=200)

# cancel ride
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@http_post_required_params(['ride_id'])
def cancel_ride(request):
    ride_id = request.POST['ride_id']
    ride = Ride.objects.get(id=ride_id)
    if ride.driver==request.user:
        ride.delete()
        for passenger in Ride2Passengers.objects.filter(ride=ride):
            push_event(user=passenger, event={'type': "ride_cancelled", "ride": ride})
        return Response(status=200)
    else:
        return Response(data={"error": "not owner"}, status=400)

class JoinRequest:
    active_join_requests = []
    def __init__(self, user, ride_id, passenger_hub_id=None):
        self.user = user
        self.ride_id = ride_id
        self.passenger_hub_id = passenger_hub_id
    @classmethod
    def add(cls, request):
        cls.active_join_requests.append(request)
    @classmethod
    def remove_all(cls, user):
        for i, v in  enumerate(cls.active_join_requests):
            if v.user == user:
                cls.active_join_requests.pop(i)
    @classmethod
    def remove(cls, user, ride_id):
        for i, join_request in enumerate(cls.active_join_requests):
            if join_request.user == user and join_request.ride_id == ride_id:
                cls.active_join_requests.pop(i)


# accept ride

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@http_post_required_params(['ride_id', 'passenger_hub_id'])
def request_join_ride(request):
    user = request.user
    ride_id = request.POST['ride_id']
    passenger_hub_id = request.POST['passenger_hub_id']
    JoinRequest.add(JoinRequest(user=user, ride_id=ride_id, passenger_hub_id=passenger_hub_id))
    ride = get_ride(ride_id)
    hub = Hub.objects.get(id=passenger_hub_id)
    push_event(user=ride.driver, event={'type': "join_request", "passenger": user, "extra_time": ride.get_duration(additional=hub) - ride.get_duration()})
    
    ride = get_ride(ride_id)
    low_points, company_low_points = calc_points_warning(ride)
    return Response(data={"ride": serializers.serialize("json", [ride]), "low_points_warning": low_points, "company_low_points": company_low_points}, status=200)


# cancel join request
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@http_post_required_params(['ride_id'])
def cancel_join_request(request):
    user = request.user
    ride_id = request.POST['ride_id']
    ride = get_ride(ride_id)
    
    JoinRequest.remove(user=user, ride_id=ride_id)
    
    push_event(user=ride.driver, event={'type': 'cancel_join_request', 'passenger': user})
    return Response(status=200)

# accept ride
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@http_post_required_params(['ride_id', 'passenger_id'])
def accept_join_request(request):
    id = request.POST['passenger_id']
    passenger = User.objects.get(id=id)


    ride_id = request.POST['ride_id']
    ride = Ride.objects.get(id=ride_id)

    for i in JoinRequest.active_join_requests:
        if i.user == passenger and i.ride_id == ride_id:
            hub = i.passenger_hub_id
            break

    JoinRequest.remove_all(passenger)

    join_ride(ride=ride, user=passenger, hub=Hub.objects.get(id=hub))

    ride.points = calc_points(ride)
    ride.save()

    push_event(user=passenger, event={'type': "joined_ride", "ride": ride})
    return Response(status=200)


# finish ride -> points etc
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@http_post_required_params(["ride_id"])
def finish_ride(request):
    ride_id = request.POST['ride_id']
    ride = get_ride(ride_id)
    user = request.user
    if ride.driver != user:
        return Response(status=400)
    else:
        points = calc_points(ride)
        user.points += points
        for passenger in ride.passengers.all():
            passenger.points += points
        return Response(status=200)

# find rides to join
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@http_post_required_params(["source_hub_id", "destination_hub_id"])
def find_rides(request):
    source_hub_id = request.POST['source_hub_id']
    source_hub = Hub.objects.get(id=source_hub_id)
    destination_hub_id = request.POST['destination_hub_id']
    destination_hub = Hub.objects.get(id=destination_hub_id)

    if destination_hub is None:
        return Response("No ride to this Destination available", status=400)
    
    rides = find_relevant_rides(source_hub=source_hub, destination_hub=destination_hub)
    return Response(data=serializers.serialize("json", rides), status=200)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    user = request.user
    return Response(data=request_update(user), status=200)


@api_view(['GET'])
def get_hubs(request):
    return Response(data=serializers.serialize('json', Hub.objects.all()), status=200)
