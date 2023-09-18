# Table of Contents

- [Table of Contents](#table-of-contents)
- [app](#app)
      - [pdk\_graph](#pdk_graph)
- [google\_api\_wrapper](#google_api_wrapper)
  - [Step Objects](#step-objects)
      - [\_\_init\_\_](#__init__)
      - [get\_google\_directions](#get_google_directions)
- [router](#router)
      - [get\_taxi\_step](#get_taxi_step)
      - [handle\_leg](#handle_leg)
      - [calc\_total\_duration](#calc_total_duration)
      - [calc\_total\_distance](#calc_total_distance)
      - [calc\_transport\_cost](#calc_transport_cost)
      - [calc\_taxi\_cost](#calc_taxi_cost)
      - [calc\_total\_cost](#calc_total_cost)
      - [merge\_steps](#merge_steps)
      - [merge\_taxi\_steps](#merge_taxi_steps)
      - [handle\_direction](#handle_direction)
      - [get\_direction](#get_direction)

<a id="app"></a>

# app

<a id="app.pdk_graph"></a>

#### pdk\_graph

```python
def pdk_graph(df1)
```

The function `pdk_graph` takes a DataFrame `df1` as input and creates a PyDeck graph visualization

based on the data in the DataFrame.

**Arguments**:

- `df1`: The parameter `df1` is a DataFrame that contains the data for creating the path layer in
the PyDeck graph. It should have the following columns: path, color, name

**Returns**:

a PyDeck chart object.

<a id="google_api_wrapper"></a>

# google\_api\_wrapper

<a id="google_api_wrapper.Step"></a>

## Step Objects

```python
class Step(object)
```

<a id="google_api_wrapper.Step.__init__"></a>

#### \_\_init\_\_

```python
def __init__(distance=None,
             duration=None,
             start_location=None,
             end_location=None,
             polyline=None,
             travel_mode: str = None,
             html_instructions: str = "",
             maneuver: str = None,
             transit_details: dict = None,
             building_level: int = None,
             steps: list = [],
             **kwargs)
```

The function is a constructor for a class that initializes its attributes with optional

arguments.

**Arguments**:

- `distance`: The distance between the start and end locations of the route
- `duration`: The duration parameter represents the duration of the route or step. It can be
specified as a dictionary with the following keys:
- `start_location`: The starting location of the route. It can be specified as a dictionary
with latitude and longitude values or as an instance of the Location class
- `end_location`: The end_location parameter represents the location where the route ends. It
can be specified as a dictionary with the following keys:
- `polyline`: The `polyline` parameter is used to represent the encoded polyline string that
represents the path of the route. It is used to draw the route on a map or to calculate the
distance and duration of the route
- `travel_mode` (`str`): The travel mode parameter specifies the mode of transportation for the
route. It can be one of the following values: "driving", "walking", "bicycling", "transit"
- `html_instructions` (`str`): The `html_instructions` parameter is a string that contains the
formatted instructions for a particular step in a route. These instructions are typically
displayed to the user in a user-friendly format
- `maneuver` (`str`): The `maneuver` parameter is used to specify a maneuver or action that needs to
be taken at a certain point during the navigation. It can be used to provide instructions such
as "turn left", "turn right", "continue straight", etc
- `transit_details` (`dict`): The `transit_details` parameter is a dictionary that contains additional
information about a transit step in a directions result. It includes details such as the arrival
stop, departure stop, line name, and transit mode
- `building_level` (`int`): The `building_level` parameter is an optional integer that represents the
level or floor of a building. It is used to specify the level at which a particular step or
instruction occurs during a navigation or transit route
- `steps` (`list`): The `steps` parameter is a list of `Step` objects. Each `Step` object represents a
single step in a set of directions

<a id="google_api_wrapper.get_google_directions"></a>

#### get\_google\_directions

```python
def get_google_directions(
        from_loc,
        to_loc,
        waypoints=[],
        departute_time=None,
        mode="transit",
        avoid=[],
        transit_mode=["bus", "subway", "train", "tram", "rail"])
```

The function `get_google_directions` takes in various parameters such as the starting location,

destination, waypoints, departure time, mode of transportation, and avoidance preferences, and
returns a list of directions from the Google Maps API.

**Arguments**:

- `from_loc`: The starting location for the directions. It should be a tuple of latitude and
longitude coordinates
- `to_loc`: The destination location. It is a tuple containing the latitude and longitude of the
destination
- `waypoints`: The waypoints parameter is a list of locations that you want to include as
intermediate stops in your directions. Each waypoint is specified as a tuple of latitude and
longitude coordinates
- `departute_time`: The `departure_time` parameter is used to specify the desired departure time
for the directions. It can be specified as a datetime object or as an integer representing the
number of seconds since the Unix epoch. If not specified, the current time will be used as the
departure time
- `mode`: The "mode" parameter specifies the mode of transportation to use for the directions.
The default value is "transit", which means public transportation will be used. Other possible
values include "driving" for driving directions, "walking" for walking directions, and "bicycling"
for bicycling, defaults to transit (optional)
- `avoid`: The `avoid` parameter is used to specify certain features to avoid when calculating
directions. It can be a list of strings containing the following options:
- `transit_mode`: The `transit_mode` parameter is a list of transportation modes that you want to
include in your directions. The available options are "bus", "subway", "train", "tram", and "rail".
By default, all of these modes are included in the directions

**Returns**:

a list of Direction objects.

<a id="router"></a>

# router

<a id="router.get_taxi_step"></a>

#### get\_taxi\_step

```python
def get_taxi_step(from_loc: tuple, to_loc: tuple, departute_time: datetime)
```

The function `get_taxi_step` calculates the distance, duration, start and end locations, polyline,

and travel mode for a taxi step in a given route.

**Arguments**:

- `from_loc` (`tuple`): The `from_loc` parameter is a tuple that represents the latitude and longitude of
the starting location for the taxi ride
- `to_loc` (`tuple`): The `to_loc` parameter is a tuple that represents the latitude and longitude
coordinates of the destination location
- `departute_time` (`datetime`): The `departute_time` parameter is the time at which the taxi is scheduled to
depart from the starting location. It should be a `datetime` object that represents the desired
departure time

**Returns**:

a Step object that represents a taxi step in a journey.

<a id="router.handle_leg"></a>

#### handle\_leg

```python
def handle_leg(config: DirectionConfig, leg: Leg)
```

The function `handle_leg` takes a configuration and a leg of a journey, and returns a list of steps

for that leg, considering factors such as walking time, maximum walk time, and transit details.

**Arguments**:

- `config` (`DirectionConfig`): The `config` parameter is an instance of the `DirectionConfig` class, which contains
configuration settings for handling directions. It likely includes properties such as `elderly` (a
boolean indicating if the user is elderly), `max_walk_time` (the maximum allowed walking time in
seconds), and `
- `leg` (`Leg`): The `leg` parameter represents a single leg of a journey. It contains information about
the steps involved in that leg, such as the travel mode (e.g., walking, transit), duration, and
transit details (if applicable)

**Returns**:

a list of steps.

<a id="router.calc_total_duration"></a>

#### calc\_total\_duration

```python
def calc_total_duration(steps: list[Step])
```

The function `calc_total_duration` calculates the total duration by summing the duration values of

each step in a list.

**Arguments**:

- `steps` (`list[Step]`): The `steps` parameter is a list of `Step` objects

**Returns**:

the sum of the duration values of each step in the given list.

<a id="router.calc_total_distance"></a>

#### calc\_total\_distance

```python
def calc_total_distance(steps: list[Step])
```

The function calculates the total distance by summing the distance values of each step in a list.

**Arguments**:

- `steps` (`list[Step]`): The `steps` parameter is a list of `Step` objects

**Returns**:

the total distance calculated from the list of steps.

<a id="router.calc_transport_cost"></a>

#### calc\_transport\_cost

```python
def calc_transport_cost(steps: list[Step], transport_price: float)
```

The function calculates the total cost of transportation based on the number of transit steps and

the price per transit.

**Arguments**:

- `steps` (`list[Step]`): The `steps` parameter is a list of `Step` objects. Each `Step` object represents a
step in a journey and contains information such as the travel mode (e.g., "TRANSIT", "WALKING",
"DRIVING"), distance, duration, etc
- `transport_price` (`float`): The transport_price parameter is the cost of using a particular mode of
transportation, such as a bus or train, for each step in the list of steps

**Returns**:

the total cost of transportation for all the steps in the given list, where the travel mode
is "TRANSIT". The cost is calculated by multiplying the number of transit steps by the given
transport price.

<a id="router.calc_taxi_cost"></a>

#### calc\_taxi\_cost

```python
def calc_taxi_cost(steps: list[Step], taxi_price: float)
```

The function `calc_taxi_cost` calculates the cost of taking a taxi based on the distance traveled

and the price per kilometer.

**Arguments**:

- `steps` (`list[Step]`): The `steps` parameter is a list of `Step` objects. Each `Step` object represents a
step in a route, such as walking, driving, or taking public transportation. The `Step` object has a
`distance` attribute that represents the distance of the step in meters, and a
- `taxi_price` (`float`): The taxi_price parameter represents the cost per kilometer for taking a taxi

**Returns**:

the total cost of taking a taxi for the given steps, based on the distance traveled and the
price per kilometer of the taxi.

<a id="router.calc_total_cost"></a>

#### calc\_total\_cost

```python
def calc_total_cost(steps: list[Step], transport_price, taxi_price)
```

The function calculates the total cost of transportation for a given list of steps, using the

provided transport and taxi prices.

**Arguments**:

- `steps` (`list[Step]`): A list of Step objects representing the different steps of a journey
- `transport_price`: The transport_price parameter represents the cost of using public
transportation for each step in the list of steps
- `taxi_price`: The taxi_price parameter represents the cost of taking a taxi for each step in
the list of steps

**Returns**:

the total cost, which is the sum of the transport cost and the taxi cost.

<a id="router.merge_steps"></a>

#### merge\_steps

```python
def merge_steps(prev_step: Step, next_step: Step)
```

The function `merge_steps` takes two `Step` objects and merges them into a new `Step` object with

combined distance, duration, start location, end location, polylines, and travel mode.

**Arguments**:

- `prev_step` (`Step`): The `prev_step` parameter is an instance of the `Step` class, which represents a
single step in a route. It contains information about the distance, duration, start location, end
location, polyline, and travel mode of the step
- `next_step` (`Step`): The `next_step` parameter is an instance of the `Step` class. It represents the
next step in a series of directions

**Returns**:

a new Step object with merged information from the previous step and the next step.

<a id="router.merge_taxi_steps"></a>

#### merge\_taxi\_steps

```python
def merge_taxi_steps(steps)
```

The function `merge_taxi_steps` merges consecutive taxi steps in a list of steps into a single step.

**Arguments**:

- `steps`: The `steps` parameter is a list of objects representing different steps of a journey.
Each step object has a `travel_mode` attribute that indicates the mode of transportation for that
step

**Returns**:

a list of merged steps.

<a id="router.handle_direction"></a>

#### handle\_direction

```python
def handle_direction(config: DirectionConfig, direction: Direction)
```

The function `handle_direction` calculates various metrics for a given direction and returns a

`FinalDirection` object.

**Arguments**:

- `config` (`DirectionConfig`): The `config` parameter is an instance of the `DirectionConfig` class. It contains
configuration settings for handling directions, such as transport fees and taxi fees
- `direction` (`Direction`): The `direction` parameter is an object of type `Direction`. It represents a set of
directions for a specific route. It contains information about the legs of the route, which are the
individual segments of the route between waypoints

**Returns**:

an instance of the `FinalDirection` class.

<a id="router.get_direction"></a>

#### get\_direction

```python
def get_direction(config: DirectionConfig)
```

The function `get_direction` takes a `DirectionConfig` object as input and returns a list of

directions obtained from Google Maps API.

**Arguments**:

- `config` (`DirectionConfig`): The `config` parameter is an instance of the `DirectionConfig` class. It contains
various properties that define the configuration for getting directions. These properties include:

**Returns**:

The function `get_direction` returns a list of directions. Each direction is processed by
the `handle_direction` function before being added to the list.

