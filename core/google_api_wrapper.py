import googlemaps as gm
import os
from dotenv import load_dotenv
from datetime import datetime
import json
load_dotenv()

client = gm.Client(key= os.getenv('GOOGLE_MAPS_API_KEY'))

class Location(object):
    def __init__(self, lat:float, lng:float):
        self.lat = lat
        self.lng = lng

class Polyline(object):
    def __init__(
        self,
        points:str,
    ):
        self.points = points

class Bounds(object):
    def __init__(
        self,
        northeast:dict,
        southwest:dict,
    ):
        self.northeast = Location(**northeast)
        self.southwest = Location(**southwest)

class Time(object):
    def __init__(
        self,
        text:str,
        time_zone:str,
        value:int,
    ):
        self.text = text
        self.time_zone = time_zone
        self.value = value

class Distance(object):
    def __init__(
        self,
        text:str,
        value:int,
    ):
        self.text = text
        self.value = value
    
class Duration(object):
    def __init__(
        self,
        text:str,
        value:int,
    ):
        self.text = text
        self.value = value

class Stop(object):
    def __init__(
        self,
        location:dict,
        name:str,
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
    ):
        self.icon = icon
        self.local_icon = local_icon
        self.name = name
        self.type = type

class Line(object):
    def __init__(
        self,
        agencies:list,
        color:str,
        name:str,
        short_name:str,
        text_color:str,
        vehicle:str,
    ):
        self.agencies = agencies
        self.color = color
        self.name = name
        self.short_name = short_name
        self.text_color = text_color
        self.vehicle = Vehicle(**vehicle)

class TransitDetails(object):
    def __init__(
        self,
        arrival_stop:dict,
        arrival_time:dict,
        departure_stop:dict,
        departure_time:dict,
        headsign:str,
        line:dict,
        num_stops:int,
    ):
        self.arrival_stop = Stop(**arrival_stop)
        self.arrival_time = Time(**arrival_time)
        self.departure_stop = Stop(**departure_stop)
        self.departure_time = Time(**departure_time)
        self.headsign = headsign
        self.line = Line(**line)
        self.num_stops = num_stops

class Step(object):
    def __init__(
        self,
        distance,
        duration,
        start_location,
        end_location,
        polyline,
        travel_mode:str,
        html_instructions:str = "",
        maneuver:str = None,
        transit_details:dict = None,
        building_level:int = None,
        steps:list = [],
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
        distance:dict,
        duration:dict,
        start_address:str,
        end_address:str,
        start_location:dict,
        end_location:dict,
        traffic_speed_entry:str,
        via_waypoint:str,
        arrival_time:dict = None,
        departure_time:dict = None,
        duration_in_traffic:int = None,
        steps:list = [],
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
        bounds:dict,
        copyrights:str,
        legs:list,
        overview_polyline:str,
        summary:str,
        warnings:list,
        waypoint_order:list,
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
    transit_mode = ["bus", "subway", "train", "tram", "rail"],
):                 
    directions_result = client.directions(str(from_loc[0])+', '+str(from_loc[1]),
                                     str(to_loc[0])+', '+str(to_loc[1]),
                                    #  waypoints=waypoints,
                                     mode=mode,
                                     departure_time=departute_time, 
                                     transit_mode=transit_mode,
                                     alternatives=True)
    return [Direction(**direction) for direction in directions_result]