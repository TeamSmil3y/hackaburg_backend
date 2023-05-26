# api.HubHopper.app
Hackaburg-Project backend

## SQL Database
Located in: `main/models.py`

### Tables
**User**
+ id _(uuid)_
+ email _(string)_
+ gender _(string["M"/"F"/"D"])_
+ adress _(string)_
+ points _(integer)_
+ latitude _(float)_
+ longitude _(float)_
+ company _(foreignKey->**Company**)_

**Company**
+ id _(uuid)_
+ name _(string)_
+ adress _(string)_
+ hub _(foreignKey->**Hub**)_
+ workload _(string[comma-seperated integers])_

**Hub**
+ id _(uuid)_
+ latitude _(float)_
+ longitude _(float)_

**Ride**
+ id _(uuid)_
+ driver _(foreignKey->**User**)_
+ source_hub _(foreignKey->**Hub**))_
+ destination_time _(datetime)_
+ destination_hub _(foreignKey->Hub)_
+ passengers _(m2n through **Ride2Passengers**)_
+ is_full _(bool)_

**Ride2Passengers**
+ ride _(foreignKey->**Ride**)_
+ passenger _(foreignKey->**User**)_
+ source_hub _(foreignKey->**Hub**)_


## Dataset // Pseudodata
Located in: `main/dataset/...`
### Data imports
We imported `people-with-companies.csv` and `ratisbona-companies.csv` of the [given Dataset](https://github.com/MoJo2600/Hackaburg2023).
The script `main/dataset/import_data.py` imports these two csv-sheets into the Database.

### Pseudodata
Because we needed data about the usual workload of offices/hubs, we created pseudodata for every weekday and every hour for all companies.
The data is based on the function
<img src="https://imgur.com/YRstch0.png" width="50%"/>
with some additional randomized parameters.
<img src="https://imgur.com/Ig5DG2T.png" width="50%"/>

### Hub Optimization


## Utils

### Ride Manager
Located in: `main/ride_manager.py`

`get_ride(id)`, `get_all_rides()`, `join_ride(ride, user)` and `get_hub(id)` are simple shortcut functions.

**find_relevant_rides(source_hub, destination_hub)**
Where `source_hub` and `destination_hub` are objects with the attributes `latitude` and `longitude` (float values) (e.g. 2 Hub objects).
Relevant rides for a searching user are
+ every ride with the same destination
+ which comes from the same direction
    + The directions are measured in the angle the vectors of the driver to the destination and the passenger to the destination, and it only sees rides as eligible, if the angle i below a certain threshold. The threshold is dependent from the distance between the passenger and the destination, so when its nearer to the destination the angle may be greater, and if the distance is greater, the angle will approach roundabout 45°. The equation is `threshold = (180° - 45°)*e^(-dist(passenger; destination)) + 45°`

<img src="https://imgur.com/kmT03FQ.png" width="50%">



### Ride Workload Calc
Located in: `main/ride_workload_calc.py`

`get_hub_workload(hub: Hub, day: int, hour: int)`
returns Integer [in %], which is the average percentage workload for the given time and weekday.
The points have the following constraints:
```
points ~ 1/workload
points ~ number_passengers
```

`calc_points_warning(ride: Ride)`
returns two booleans, the first one is if the hub workload is exceptionally high, the second one is if the office workload is exceptionally high.

`get_hub_workload(hub: Hub, day: int, hour: int)`
adds all office workloads of the offices assigned to the hubs and returns the sum as a hub workload.

`calc_points(ride: Ride)`
Returns points as integer, 

### View Utils
Located in: `main/view_utils.py`

**@http_get_only decorator** (UNUSED)
Only allow `GET`-requests

**@http_post_only decorator** (UNUSED)
Only allow `POST`-requests

**@http_post_required_params(params: list) decorator**
Require all in `params` listed `POST` parameters

### Routes
Located in: `main/routed.py`

Using the google Maps Routed API (route matrix computation).
The function `get_route_duration(origins, destination)` returns the duration of the route in seconds, where `origins` is a list of objects with the attributes `latitude`and `longitude` (e.g. a list of Hubs), and `destination` is an object with the attributes `latitude`and `longitude` (e.g. a Hub).

### Update Manager
Located in: `main/update_manager.py`

Global `events` Dictionary



## Views // Endpoints
Located in: `main/views.py`

The Views are django-rest-api Endpoints (function based views).

Endpoint _/login/_
`user_login(request)`
Authenticate the user.

Endpoint _/logout/_
`user_logout(request)`
Authenticate the user.

Endpoint _/create_ride/_
`create_ride(request)`
POST `source_hub_id` and `destination_hub_id` to add new ride.
RESPONSE: ride_obj[ Obj ], low_points_warning[ Bool ], company_low_points[ Bool ]

Endpoint _/cancel_ride/_
`cancel_ride(request)`
POST `ride_id` of the ride to get cancelled.

Endpoint _/request_join_ride/_
`request_join_ride(request)`
POST `ride_id` to join the ride.
RESPONSE: ride_obj[ Obj ], low_points_warning[ Bool ], company_low_points[ Bool ]

Endpoint _/accept_join_ride/_
`accept_join_request(request)`
POST `ride_id` of the joined ride and `passenger_id` of the joining passenger.
RESPONSE: void

Endpoint _/finish_ride/_
`finish_ride(request)`
POST `ride_id`; will calculate and book the points
RESPONSE: void

Endpoint _/find_rides/_
`find_rides(request)`
POST `source_id_hub` and `destination_hub_id` to find relevant rides using the `find_relevant_rides(source_hub, destination_hub) Util to find relevant rides.
RESPONSE: rides

Endpoint _/update/_
`update(request)`
GET
RESPONSE: update (see **Update Manager**)

Endpoint _/get_hubs/_
`get_hubs()`
GET
RESPONSE hubs (list of objects)
