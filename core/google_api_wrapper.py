import googlemaps as gm
import os
from dotenv import load_dotenv
from datetime import datetime
import json
load_dotenv()

client = gm.Client(key= os.getenv('GOOGLE_MAPS_API_KEY'))

class Location(object):
    def __init__(
        self,
        lat:float = None,
        lng:float = None,
        **kwargs
    ):
        self.lat = lat
        self.lng = lng

class Polyline(object):
    def __init__(
        self,
        points:str = None,
        **kwargs
    ):
        self.points = points

class Bounds(object):
    def __init__(
        self,
        northeast:dict = None,
        southwest:dict = None,
        **kwargs
    ):
        self.northeast = Location(**northeast)
        self.southwest = Location(**southwest)

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

class Distance(object):
    def __init__(
        self,
        text:str = None,
        value:int = None,
        **kwargs
    ):
        self.text = text
        self.value = value
    
class Duration(object):
    def __init__(
        self,
        text:str = None,
        value:int = None,
        **kwargs
    ):
        self.text = text
        self.value = value

class Stop(object):
    def __init__(
        self,
        location:dict = None,
        name:str = None,
        **kwargs
    ):
        self.location = Location(**location)
        self.name = name

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