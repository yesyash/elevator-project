from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from api.helpers import findTheClosestElevator
from .models import Elevator, ElevatorSystem, Requests
from .serializers import ElevatorSerializer, ElevatorSystemSerializer

import datetime


@csrf_exempt
def elevator_system(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ElevatorSystemSerializer(data=data)
        if serializer.is_valid():
            for i in range(int(data["number_of_elevators"])):
                e = Elevator()
                e.save()
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse({"message": "Invalid input"}, status=400)


@csrf_exempt
def elevators(request):
    # remove out dated requests
    current_timestamp_in_unix_timestamp = (
        datetime.datetime.timestamp(datetime.datetime.now()) * 1000
    )
    delete_pending_requests(current_timestamp_in_unix_timestamp)

    # get status of all working elevators
    if request.method == "GET":
        working_elevators = []
        elevators = list(Elevator.objects.filter(is_working=True))
        for i in range(len(elevators)):
            working_elevator = {
                "elevator_id": elevators[i].id,
                "current_floor": elevators[i].current_floor,
                "next_destination": elevators[i].next_destination,
                "is_moving": elevators[i].is_moving,
                "direction": elevators[i].direction,
            }
            working_elevators.append(working_elevator)

        return JsonResponse(working_elevators, safe=False, status=200)

    # update status of an elevator to maintenance / not working or working
    if request.method == "PUT":
        if hasattr(request, "query_params"):
            elevator_id = request.query_params.get("elevator_id", None)
        elif hasattr(request, "GET"):
            elevator_id = request.GET.get("elevator_id", None)
        else:
            return JsonResponse(
                {
                    "message": "elevator_id is missing",
                },
                status=400,
            )

        data = JSONParser().parse(request)
        status = (
            False
            if data["status"] == "maintenance" or data["status"] == "not working"
            else True
        )
        ele = Elevator.objects.filter(id=elevator_id)
        if ele:
            ele.update(
                is_working=status,
                is_moving=False,
                direction=None,
                next_destination=None,
                current_floor=1,
                is_door_open=False,
            )
            return JsonResponse(
                {
                    "message": f"elevator {elevator_id} is now {'working' if status else 'under maintenance'}",
                },
                status=200,
            )
        else:
            return JsonResponse(
                {
                    "message": "elevator not found",
                },
                status=404,
            )


# helper function used in requests function
def delete_pending_requests(current_timestamp_in_unix_timestamp):
    # Remove any out dated requests
    requests = list(
        Requests.objects.filter(completes_by__lte=current_timestamp_in_unix_timestamp)
    )

    if len(requests) > 0:
        for i in range(len(requests)):
            req = requests[i]
            elevator = Elevator.objects.filter(id=req.elevator_id)
            # update the elevator status to idle / is_moving to false
            elevator.update(is_moving=False, next_destination=None)
            # delete the request record from db
            req.delete()


@csrf_exempt
def requests(request):
    current_timestamp_in_unix_timestamp = (
        datetime.datetime.timestamp(datetime.datetime.now()) * 1000
    )

    # get all the lifts which have pending requests
    if request.method == "GET":
        lifts_working_on_pending_requests = []
        requests = list(
            Requests.objects.filter(
                completes_by__gt=current_timestamp_in_unix_timestamp
            )
        )

        for i in range(len(requests)):
            elevator_id = requests[i].elevator_id
            destination = Elevator.objects.filter(id=requests[i].elevator_id)[
                0
            ].next_destination

            lifts_working_on_pending_requests.append(
                {
                    "elevator_id": elevator_id,
                    "destination": destination,
                }
            )

        return JsonResponse(
            {
                "requests": lifts_working_on_pending_requests,
            },
            status=200,
        )

    # create a new request if an elevator is available
    if request.method == "POST":
        TRAVEL_TIME = 10000  # 10 seconds

        # deletes pending request records from db
        delete_pending_requests(current_timestamp_in_unix_timestamp)

        data = JSONParser().parse(request)
        destination_floor = data["requested_floor"]
        available_elevators = Elevator.objects.filter(is_working=True, is_moving=False)
        available_elevators = list(available_elevators)

        if len(available_elevators) == 0:
            return JsonResponse(
                {"message": "No lifts are available currently"},
                status=200,
            )

        # Find the closed elevator
        closet_available_elevator = findTheClosestElevator(
            available_elevators, len(available_elevators), destination_floor
        )

        # Add a new request
        completes_by = (
            datetime.datetime.timestamp(datetime.datetime.now()) * 1000 + TRAVEL_TIME
        )
        elevator_req = Requests(
            elevator_id=closet_available_elevator.id,
            from_floor=closet_available_elevator.current_floor,
            to_floor=destination_floor,
            completes_by=completes_by,
        )

        print(f"\n\n{completes_by}\n\n")

        elevator_req.save()

        # Update the elevator status
        direction = (
            "down"
            if closet_available_elevator.current_floor > destination_floor
            else "up"
        )
        Elevator.objects.filter(id=closet_available_elevator.id).update(
            is_moving=True, next_destination=destination_floor, direction=direction
        )

        return JsonResponse(
            {
                "message": f"Elevator {closet_available_elevator.id} is moving to floor {destination_floor}"
            },
            status=200,
        )


@csrf_exempt
def destination(request):
    # remove out dated requests
    current_timestamp_in_unix_timestamp = (
        datetime.datetime.timestamp(datetime.datetime.now()) * 1000
    )
    delete_pending_requests(current_timestamp_in_unix_timestamp)

    if hasattr(request, "query_params"):
        elevator_id = request.query_params.get("elevator_id", None)
    elif hasattr(request, "GET"):
        elevator_id = request.GET.get("elevator_id", None)
    else:
        return JsonResponse(
            {
                "message": "elevator_id is missing",
            },
            status=400,
        )

    dest = Elevator.objects.filter(id=elevator_id)[0].next_destination

    if dest:
        return JsonResponse(
            {
                "destination": dest,
            },
            status=200,
        )

    return JsonResponse(
        {
            "destination": "null",
        },
        status=200,
    )


@csrf_exempt
def doors(request):
    if request.method == "PUT":
        if hasattr(request, "query_params"):
            elevator_id = request.query_params.get("elevator_id", None)
        elif hasattr(request, "GET"):
            elevator_id = request.GET.get("elevator_id", None)
        else:
            return JsonResponse(
                {
                    "message": "elevator_id is missing",
                },
                status=400,
            )

        data = JSONParser().parse(request)
        action = data["action"]

        should_open = True if action == "open" else False
        ele = Elevator.objects.filter(id=elevator_id)
        if ele:
            ele.update(
                is_door_open=should_open,
            )
            return JsonResponse(
                {
                    "message": f"elevator {elevator_id} door is now {'open' if should_open else 'close'}",
                },
                status=200,
            )
        else:
            return JsonResponse(
                {
                    "message": "elevator not found",
                },
                status=404,
            )
