from .google_api_wrapper import get_google_directions, Direction, Leg, Step, Location, Distance
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import dataclasses, json

with open('./data/emissions.json') as json_file:
    emissions_info = json.load(json_file)

@dataclass
# The DirectionConfig class is used to configure directions.
class DirectionConfig:
    from_loc:tuple
    waypoints:list[tuple]
    to_loc:tuple
    departute_time:datetime
    max_walk_time:float
    transit_mode:list[str]
    avoid:list[str]
    elderly:bool
    transport_fee:float
    taxi_fee:float
    research_alpha_bus:float

def get_taxi_step(
    from_loc:tuple,
    to_loc:tuple,
    departute_time:datetime,
):  
    """
    The function `get_taxi_step` calculates the distance, duration, start and end locations, polyline,
    and travel mode for a taxi step in a given route.
    
    :param from_loc: The `from_loc` parameter is a tuple that represents the latitude and longitude of
    the starting location for the taxi ride
    :type from_loc: tuple
    :param to_loc: The `to_loc` parameter is a tuple that represents the latitude and longitude
    coordinates of the destination location
    :type to_loc: tuple
    :param departute_time: The `departute_time` parameter is the time at which the taxi is scheduled to
    depart from the starting location. It should be a `datetime` object that represents the desired
    departure time
    :type departute_time: datetime
    :return: a Step object that represents a taxi step in a journey.
    """
    taxi_step = get_google_directions(
        from_loc,
        to_loc,
        departute_time=departute_time,
        mode="driving"
    )
    return Step(
        distance=taxi_step[0].legs[0].distance,
        duration=taxi_step[0].legs[0].duration,
        start_location=Location(from_loc[0], from_loc[1]),
        end_location=Location(to_loc[0], to_loc[1]),
        polyline=taxi_step[0].overview_polyline,
        travel_mode="TAXI",
        emissions=emissions_info["TAXI"],
    )

def handle_leg(
    
    config:DirectionConfig,
    leg:Leg
    ):
    """
    The function `handle_leg` takes a configuration and a leg of a journey, and returns a list of steps
    for that leg, considering factors such as walking time, maximum walk time, and transit details.
    
    :param config: The `config` parameter is an instance of the `DirectionConfig` class, which contains
    configuration settings for handling directions. It likely includes properties such as `elderly` (a
    boolean indicating if the user is elderly), `max_walk_time` (the maximum allowed walking time in
    seconds), and `
    :type config: DirectionConfig
    :param leg: The `leg` parameter represents a single leg of a journey. It contains information about
    the steps involved in that leg, such as the travel mode (e.g., walking, transit), duration, and
    transit details (if applicable)
    :type leg: Leg
    :return: a list of steps.
    """
    steps = []
    dep_time = datetime.fromtimestamp(leg.departure_time.value)
    for step in leg.steps:
        next_step = step
        seconds_duration = step.duration.value
        if step.travel_mode == "WALKING":
            step.emissions = emissions_info["WALKING"] * step.distance.value / 1000
            walk_time = float(step.duration.value if config.elderly else step.duration.value * 1.5)
            if float(config.max_walk_time) < walk_time:
                taxi_step = get_taxi_step(
                    [step.start_location.lat, step.start_location.lng],
                    [step.end_location.lat, step.end_location.lng],
                    dep_time,
                )
                seconds_duration = walk_time
                next_step = taxi_step
        elif step.travel_mode == "TRANSIT":
            step.emissions = (emissions_info[step.transit_details.line.vehicle.type] if step.transit_details.line.vehicle.type in emissions_info else emissions_info["DEFAULT"]) * step.distance.value / 1000
            if step.transit_details.line.vehicle.type == "BUS":
                research_alpha_bus = step.distance.value / step.transit_details.num_stops
                if research_alpha_bus > config.research_alpha_bus:
                    taxi_step = get_taxi_step(
                        [step.start_location.lat, step.start_location.lng],
                        [step.end_location.lat, step.end_location.lng],
                        dep_time,
                    )
                    seconds_duration = step.duration.value
                    next_step = taxi_step
        dep_time += timedelta(seconds=seconds_duration)
        steps.append(next_step)
    return steps

def calc_total_duration(steps:list[Step]):
    """
    The function `calc_total_duration` calculates the total duration by summing the duration values of
    each step in a list.
    
    :param steps: The `steps` parameter is a list of `Step` objects
    :type steps: list[Step]
    :return: the sum of the duration values of each step in the given list.
    """
    return sum(step.duration.value for step in steps)

def calc_total_distance(steps:list[Step]):
    """
    The function calculates the total distance by summing the distance values of each step in a list.
    
    :param steps: The `steps` parameter is a list of `Step` objects
    :type steps: list[Step]
    :return: the total distance calculated from the list of steps.
    """
    return sum(step.distance.value for step in steps)

def calc_transport_cost(steps:list[Step], transport_price:float):
    """
    The function calculates the total cost of transportation based on the number of transit steps and
    the price per transit.
    
    :param steps: The `steps` parameter is a list of `Step` objects. Each `Step` object represents a
    step in a journey and contains information such as the travel mode (e.g., "TRANSIT", "WALKING",
    "DRIVING"), distance, duration, etc
    :type steps: list[Step]
    :param transport_price: The transport_price parameter is the cost of using a particular mode of
    transportation, such as a bus or train, for each step in the list of steps
    :type transport_price: float
    :return: the total cost of transportation for all the steps in the given list, where the travel mode
    is "TRANSIT". The cost is calculated by multiplying the number of transit steps by the given
    transport price.
    """
    return sum(1 for step in steps if step.travel_mode == "TRANSIT") * transport_price

def calc_taxi_cost(steps:list[Step], taxi_price:float):
    """
    The function `calc_taxi_cost` calculates the cost of taking a taxi based on the distance traveled
    and the price per kilometer.
    
    :param steps: The `steps` parameter is a list of `Step` objects. Each `Step` object represents a
    step in a route, such as walking, driving, or taking public transportation. The `Step` object has a
    `distance` attribute that represents the distance of the step in meters, and a
    :type steps: list[Step]
    :param taxi_price: The taxi_price parameter represents the cost per kilometer for taking a taxi
    :type taxi_price: float
    :return: the total cost of taking a taxi for the given steps, based on the distance traveled and the
    price per kilometer of the taxi.
    """
    return sum(step.distance.value for step in steps if step.travel_mode == "TAXI") / 1000 * taxi_price

def calc_total_cost(steps:list[Step], transport_price, taxi_price):
    """
    The function calculates the total cost of transportation for a given list of steps, using the
    provided transport and taxi prices.
    
    :param steps: A list of Step objects representing the different steps of a journey
    :type steps: list[Step]
    :param transport_price: The transport_price parameter represents the cost of using public
    transportation for each step in the list of steps
    :param taxi_price: The taxi_price parameter represents the cost of taking a taxi for each step in
    the list of steps
    :return: the total cost, which is the sum of the transport cost and the taxi cost.
    """
    return calc_transport_cost(steps, transport_price) + calc_taxi_cost(steps, taxi_price)

def calc_total_emissions(steps:list[Step]):
    """
    The function calculates the total CO2 emissions.
    
    :param steps: A list of Step objects representing the different steps of a journey
    :type steps: list[Step]
    :return: the total emissions, which is the sum of each step emissions.
    """
    return sum(step.emissions for step in steps)

@dataclass
# The FinalDirection class is a placeholder for a class that will handle the final direction of an
# object.
class FinalDirection:
    steps:list[Step]
    total_duration:float
    total_distance:float
    total_cost:float
    total_transport_cost:float
    total_taxi_cost:float
    co2:float

def merge_steps(prev_step:Step, next_step:Step):
    """
    The function `merge_steps` takes two `Step` objects and merges them into a new `Step` object with
    combined distance, duration, start location, end location, polylines, and travel mode.
    
    :param prev_step: The `prev_step` parameter is an instance of the `Step` class, which represents a
    single step in a route. It contains information about the distance, duration, start location, end
    location, polyline, and travel mode of the step
    :type prev_step: Step
    :param next_step: The `next_step` parameter is an instance of the `Step` class. It represents the
    next step in a series of directions
    :type next_step: Step
    :return: a new Step object with merged information from the previous step and the next step.
    """
    new_distance = Distance(
        prev_step.distance.text + " + " + next_step.distance.text,
        prev_step.distance.value + next_step.distance.value,
    )
    new_duration = Distance(
        prev_step.duration.text + " + " + next_step.duration.text,
        prev_step.duration.value + next_step.duration.value,
    )

    return Step(
        new_distance,
        new_duration,
        prev_step.start_location,
        next_step.end_location,
        [prev_step.polyline,next_step.polyline],
        travel_mode="TAXI",
        emissions=emissions_info["TAXI"],
    )

def merge_taxi_steps(steps):
    """
    The function `merge_taxi_steps` merges consecutive taxi steps in a list of steps into a single step.
    
    :param steps: The `steps` parameter is a list of objects representing different steps of a journey.
    Each step object has a `travel_mode` attribute that indicates the mode of transportation for that
    step
    :return: a list of merged steps.
    """
    merged_steps = []
    prev_step = None
    for step in steps:
        if step.travel_mode == "TAXI":
            if prev_step is None:
                prev_step = step
            else:
                prev_step = merge_steps(prev_step, step)
        else:
            if prev_step is not None:
                merged_steps.append(prev_step)
                prev_step = None
            merged_steps.append(step)
    if prev_step is not None:
        merged_steps.append(prev_step)
    return merged_steps

def handle_direction(

    config:DirectionConfig,
    direction:Direction,
):
    """
    The function `handle_direction` calculates various metrics for a given direction and returns a
    `FinalDirection` object.
    
    :param config: The `config` parameter is an instance of the `DirectionConfig` class. It contains
    configuration settings for handling directions, such as transport fees and taxi fees
    :type config: DirectionConfig
    :param direction: The `direction` parameter is an object of type `Direction`. It represents a set of
    directions for a specific route. It contains information about the legs of the route, which are the
    individual segments of the route between waypoints
    :type direction: Direction
    :return: an instance of the `FinalDirection` class.
    """
    leg_steps = []
    total_duration, total_distance, total_cost, total_transport_cost, total_taxi_cost, total_emissions = 0, 0, 0, 0, 0, 0
    for leg in direction.legs:
        steps = handle_leg(config, leg)
        total_duration += calc_total_duration(steps)
        total_distance += calc_total_distance(steps)
        total_cost += calc_total_cost(steps, config.transport_fee, config.taxi_fee)
        total_transport_cost += calc_transport_cost(steps, config.transport_fee)
        total_taxi_cost += calc_taxi_cost(steps, config.taxi_fee)
        total_emissions += calc_total_emissions(steps)
        leg_steps.extend(steps)
    
    return FinalDirection(
        merge_taxi_steps(leg_steps),
        total_duration,
        total_distance,
        total_cost,
        total_transport_cost,
        total_taxi_cost,
        total_emissions,
    )

def get_direction(
   
    config:DirectionConfig,
):
    """
    The function `get_direction` takes a `DirectionConfig` object as input and returns a list of
    directions obtained from Google Maps API.
    
    :param config: The `config` parameter is an instance of the `DirectionConfig` class. It contains
    various properties that define the configuration for getting directions. These properties include:
    :type config: DirectionConfig
    :return: The function `get_direction` returns a list of directions. Each direction is processed by
    the `handle_direction` function before being added to the list.
    """
    proposed_directions = get_google_directions(
        config.from_loc,
        config.to_loc,
        # waypoints=config.waypoints,
        departute_time=config.departute_time,
        avoid=config.avoid,
        transit_mode=config.transit_mode,
    )
    return [handle_direction(config, direction) for direction in proposed_directions]
