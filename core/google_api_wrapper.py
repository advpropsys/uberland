import googlemaps as gm
import os
from dotenv import load_dotenv
from datetime import datetime
import json
load_dotenv()

client = gm.Client(key= os.getenv('GOOGLE_MAPS_API_KEY'))

# The Location class is a basic object that represents a location.
class Location(object):
    def __init__(
        self,
        lat:float = None,
        lng:float = None,
        **kwargs
    ):
        self.lat = lat
        self.lng = lng

# The Polyline class is a representation of a series of connected line segments in a two-dimensional
# space.
class Polyline(object):
    def __init__(
        self,
        points:str = None,
        **kwargs
    ):
        self.points = points

# The Bounds class is a Python object that represents a range of values.
class Bounds(object):
    def __init__(
        self,
        northeast:dict = None,
        southwest:dict = None,
        **kwargs
    ):
        self.northeast = Location(**northeast)
        self.southwest = Location(**southwest)

# The Time class is a basic representation of time in hours, minutes, and seconds.
class Time(object):
    def __init__(
        self,
        text:str = None,
        time_zone:str = None,
        value:int = None,
        **kwargs
    ):
        self.text = text
        self.time_zone = time_zone
        self.value = value

# The Distance class is a Python object that represents a distance measurement.
class Distance(object):
    def __init__(
        self,
        text:str = None,
        value:int = None,
        **kwargs
    ):
        self.text = text
        self.value = value
    
# The Duration class is a Python object that represents a duration of time.
class Duration(object):
    def __init__(
        self,
        text:str = None,
        value:int = None,
        **kwargs
    ):
        self.text = text
        self.value = value

# The Stop class is a basic object class.
class Stop(object):
    def __init__(
        self,
        location:dict = None,
        name:str = None,
        **kwargs
    ):
        self.location = Location(**location)
        self.name = name

# The Vehicle class is a base class for all types of vehicles.
class Vehicle(object):
    def __init__(
        self,
        icon:str = None,
        local_icon:str = None,
        name:str = None,
        type:str = None,
        **kwargs
    ):
        self.icon = icon
        self.local_icon = local_icon
        self.name = name
        self.type = type

# The Line class is a blueprint for creating line objects.
class Line(object):
    def __init__(
        self,
        agencies:list = None,
        color:str = None,
        name:str = None,
        short_name:str = None,
        text_color:str = None,
        vehicle:str = None,
        url:str = None,
        icon:str = None,
        **kwargs
    ):
        self.agencies = agencies
        self.color = color
        self.name = name
        self.short_name = short_name
        self.text_color = text_color
        self.vehicle = Vehicle(**vehicle)
        self.url = url
        self.icon = icon

# The TransitDetails class is a Python object that represents details about a transit route.
class TransitDetails(object):
    def __init__(
        self,
        arrival_stop:dict = None,
        arrival_time:dict = None,
        departure_stop:dict = None,
        departure_time:dict = None,
        headsign:str = None,
        line:dict = None,
        num_stops:int = None,
        headway:int = None,
        trip_short_name:str = None,
        **kwargs
    ):
        self.arrival_stop = Stop(**arrival_stop)
        self.arrival_time = Time(**arrival_time)
        self.departure_stop = Stop(**departure_stop)
        self.departure_time = Time(**departure_time)
        self.headsign = headsign
        self.line = Line(**line)
        self.num_stops = num_stops
        self.headway = headway
        self.trip_short_name = trip_short_name

# The Step class is a basic object in Python.
class Step(object):
    def __init__(
        self,
        distance = None,
        duration = None,
        start_location = None,
        end_location = None,
        polyline = None,
        travel_mode:str = None,
        html_instructions:str = "",
        maneuver:str = None,
        transit_details:dict = None,
        building_level:int = None,
        steps:list = [],
        **kwargs
    ):
        """
        The function is a constructor for a class that initializes its attributes with optional
        arguments.
        
        :param distance: The distance between the start and end locations of the route
        :param duration: The duration parameter represents the duration of the route or step. It can be
        specified as a dictionary with the following keys:
        :param start_location: The starting location of the route. It can be specified as a dictionary
        with latitude and longitude values or as an instance of the Location class
        :param end_location: The end_location parameter represents the location where the route ends. It
        can be specified as a dictionary with the following keys:
        :param polyline: The `polyline` parameter is used to represent the encoded polyline string that
        represents the path of the route. It is used to draw the route on a map or to calculate the
        distance and duration of the route
        :param travel_mode: The travel mode parameter specifies the mode of transportation for the
        route. It can be one of the following values: "driving", "walking", "bicycling", "transit"
        :type travel_mode: str
        :param html_instructions: The `html_instructions` parameter is a string that contains the
        formatted instructions for a particular step in a route. These instructions are typically
        displayed to the user in a user-friendly format
        :type html_instructions: str
        :param maneuver: The `maneuver` parameter is used to specify a maneuver or action that needs to
        be taken at a certain point during the navigation. It can be used to provide instructions such
        as "turn left", "turn right", "continue straight", etc
        :type maneuver: str
        :param transit_details: The `transit_details` parameter is a dictionary that contains additional
        information about a transit step in a directions result. It includes details such as the arrival
        stop, departure stop, line name, and transit mode
        :type transit_details: dict
        :param building_level: The `building_level` parameter is an optional integer that represents the
        level or floor of a building. It is used to specify the level at which a particular step or
        instruction occurs during a navigation or transit route
        :type building_level: int
        :param steps: The `steps` parameter is a list of `Step` objects. Each `Step` object represents a
        single step in a set of directions
        :type steps: list
        """
        self.distance = Distance(**distance) if type(distance) is dict else distance
        self.duration = Duration(**duration) if type(duration) is dict else duration
        self.start_location = Location(**start_location) if type(start_location) is dict else start_location
        self.end_location = Location(**end_location) if type(end_location) is dict else end_location
        self.html_instructions = html_instructions
        self.polyline = Polyline(**polyline) if type(polyline) is dict else polyline
        self.travel_mode = travel_mode
        self.manuever = maneuver
        self.transit_details = None if transit_details is None else TransitDetails(**transit_details)
        self.building_level = building_level
        self.steps = [Step(**step) for step in steps]

# The Leg class is a basic representation of a leg in a humanoid body.
class Leg(object):
    def __init__(
        self,
        distance:dict = None,
        duration:dict = None,
        start_address:str = None,
        end_address:str = None,
        start_location:dict = None,
        end_location:dict = None,
        traffic_speed_entry:str = None,
        via_waypoint:str = None,
        arrival_time:dict = None,
        departure_time:dict = None,
        duration_in_traffic:int = None,
        steps:list = [],
        **kwargs
    ):
        self.arrival_time = None if arrival_time is None else Time(**arrival_time)
        self.departure_time = None if arrival_time is None else Time(**departure_time)
        self.distance = Distance(**distance)
        self.duration = Duration(**duration)
        self.start_address = start_address
        self.end_address = end_address
        self.start_location = Location(**start_location)
        self.end_location = Location(**end_location)
        self.traffic_speed_entry = traffic_speed_entry
        self.duration_in_traffic = duration_in_traffic
        self.via_waypoint = via_waypoint
        self.steps = [Step(**step) for step in steps]

# The Direction class is a basic template for representing directions.
class Direction(object):
    def __init__(
        self,
        bounds:dict = None,
        copyrights:str = None,
        legs:list = None,
        overview_polyline:str = None,
        summary:str = None,
        warnings:list = None,
        waypoint_order:list = None,
        **kwargs
    ):
        self.bounds = Bounds(**bounds)
        self.copyrights = copyrights
        self.legs = [Leg(**leg) for leg in legs]
        self.overview_polyline = Polyline(**overview_polyline)
        self.summary = summary
        self.warnings = warnings
        self.waypoint_order = waypoint_order

def get_google_directions(
    
    from_loc,
    to_loc,
    waypoints = [],
    departute_time = None,
    mode = "transit",
    avoid = [],
    transit_mode = ["bus", "subway", "train", "tram", "rail"],
):
    """
    The function `get_google_directions` takes in various parameters such as the starting location,
    destination, waypoints, departure time, mode of transportation, and avoidance preferences, and
    returns a list of directions from the Google Maps API.
    
    :param from_loc: The starting location for the directions. It should be a tuple of latitude and
    longitude coordinates
    :param to_loc: The destination location. It is a tuple containing the latitude and longitude of the
    destination
    :param waypoints: The waypoints parameter is a list of locations that you want to include as
    intermediate stops in your directions. Each waypoint is specified as a tuple of latitude and
    longitude coordinates
    :param departute_time: The `departure_time` parameter is used to specify the desired departure time
    for the directions. It can be specified as a datetime object or as an integer representing the
    number of seconds since the Unix epoch. If not specified, the current time will be used as the
    departure time
    :param mode: The "mode" parameter specifies the mode of transportation to use for the directions.
    The default value is "transit", which means public transportation will be used. Other possible
    values include "driving" for driving directions, "walking" for walking directions, and "bicycling"
    for bicycling, defaults to transit (optional)
    :param avoid: The `avoid` parameter is used to specify certain features to avoid when calculating
    directions. It can be a list of strings containing the following options:
    :param transit_mode: The `transit_mode` parameter is a list of transportation modes that you want to
    include in your directions. The available options are "bus", "subway", "train", "tram", and "rail".
    By default, all of these modes are included in the directions
    :return: a list of Direction objects.
    """
    print([str(waypoint[0]) + ', ' + str(waypoint[1]) for waypoint in waypoints])
    directions_result = client.directions(str(from_loc[0])+', '+str(from_loc[1]),
                                     str(to_loc[0])+', '+str(to_loc[1]),
                                     waypoints= [str(waypoint[0]) + ', ' + str(waypoint[1]) for waypoint in waypoints],
                                     mode=mode,
                                     departure_time=departute_time, 
                                     transit_mode=transit_mode,
                                     avoid=avoid,
                                     alternatives=True)
    return [Direction(**direction) for direction in directions_result]