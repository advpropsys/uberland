from google_api_wrapper import get_google_directions, Direction, Leg, Step
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import reduce

@dataclass
class DirectionConfig:
    from_loc:tuple
    waypoints:list[tuple]
    to_loc:tuple
    departute_time:datetime
    max_walk_time:int
    # max_transfers:int
    transit_mode:list[str]
    elderly:bool
    # budget:int
    transport_fee:int
    taxi_fee:int

def get_taxi_step(
    from_loc:tuple,
    to_loc:tuple,
    departute_time:datetime,
):
    taxi_step = get_google_directions(
        from_loc,
        to_loc,
        departute_time=departute_time,
        mode="DRIVE"
    )
    return Step(
        distance=taxi_step[0].legs[0].distance,
        duration=taxi_step[0].legs[0].duration,
        start_location=from_loc,
        end_location=to_loc,
        polyline=taxi_step[0].overview_polyline,
        travel_mode="TAXI"
    )

def handle_leg(
    config:DirectionConfig,
    leg:Leg
):
    steps = []
    dep_time = leg.departure_time
    for step in leg.steps:
        next_step = step
        seconds_duration = step.duration.value
        if step.travel_mode == "WALKING":
            walk_time = walk_time if config.elderly else walk_time * 1.5
            if config.max_walk_time > step.duration.value:
                taxi_step = get_taxi_step(
                    step.start_location,
                    step.end_location,
                    dep_time,
                )
                seconds_duration = step.duration.value
                next_step = taxi_step
        elif step.travel_mode == "TRANSIT":
            if step.transit_details.line.vehicle.type == "BUS":
                taxi_step = get_taxi_step(
                    step.start_location,
                    step.end_location,
                    dep_time,
                )
                seconds_duration = step.duration.value
                next_step = taxi_step
        dep_time += timedelta(seconds=seconds_duration)
        steps.append(next_step)
    return steps

def calc_total_duration(steps:list[Step]):
    return sum(step.duration.value for step in steps)

def calc_total_distance(steps:list[Step]):
    return sum(step.distance.value for step in steps)

def calc_transport_cost(steps:list[Step], transport_price:float):
    return steps.count(lambda step: step.travel_mode == "TRANSIT") * transport_price

def calc_taxi_cost(steps:list[Step], taxi_price:float):
    return sum(step.distance.value for step in steps if step.travel_mode == "TAXI")

def calc_total_cost(steps:list[Step], transport_price, taxi_price):
    return calc_transport_cost(steps, transport_price) * calc_taxi_cost(steps, taxi_price)

class FinalDirection:
    steps:list[Step]
    total_duration:float
    total_distance:float
    total_cost:float
    total_transport_cost:float
    total_taxi_cost:float
    co2:float

def handle_direction(
    config:DirectionConfig,
    direction:Direction,
):
    leg_steps = []
    total_duration, total_distance, total_cost, total_transport_cost, total_taxi_cost = 0, 0, 0, 0, 0
    for leg in direction.legs:
        steps = handle_leg(config, leg)
        total_duration += calc_total_duration(steps)
        total_distance += calc_total_distance(steps)
        total_cost += calc_total_cost(steps, config.transport_fee, config.taxi_fee)
        total_transport_cost += calc_transport_cost(steps, config.transport_fee)
        total_taxi_cost += calc_taxi_cost(steps, config.taxi_fee)
        leg_steps.extend(steps)

    return FinalDirection(
        leg_steps,
        total_duration,
        total_distance,
        total_cost,
        total_transport_cost,
        total_taxi_cost,
        ,
    )

def get_direction(
    config:DirectionConfig,
):
    proposed_directions = get_google_directions(
        config.from_loc,
        config.to_loc,
        waypoints=config.waypoints,
        departute_time=config.departute_time,
        transit_mode=config.transit_mode,
    )
    return [handle_direction(config, direction) for direction in proposed_directions]
