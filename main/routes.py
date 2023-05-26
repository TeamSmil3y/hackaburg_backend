import requests, json
from .models import *

def get_route_duration(origins, destination):
    payload = {
          "origins": [
            {
              "waypoint": {
                "location": {
                  "latLng": {
                    "latitude": origin.latitude,
                    "longitude": origin.longitude
                  }
                }
              },
              "routeModifiers": {"avoid_ferries": True}
            } for origin in origins
          ],
          "destinations": [
            {
              "waypoint": {
                "location": {
                  "latLng": {
                    "latitude": destination.latitude,
                    "longitude": destination.longitude
                  }
                }
              }
            }
          ],
          "travelMode": "DRIVE",
          "routingPreference": "TRAFFIC_AWARE"
    }
    
    
    r = requests.post(
        "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix",
        json=payload,
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": "AIzaSyCvzPeqLCekycOt-UB6EeaD6XuqcymzPNw",
            "X-Goog-FieldMask": "duration"
        }
        
    )
    
    j = r.json()
    d = 0
    for i in j:
        d += float(i["duration"].replace("s", ""))
        
    return d
    