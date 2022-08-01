from rest_framework import serializers

from api.models import Elevator, ElevatorSystem

# Elevator system serializers
class ElevatorSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ElevatorSystem
        fields = [
            "number_of_elevators",
            "number_of_floors",
        ]


# Elevator serializers
class ElevatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Elevator
        fields = [
            "id",
            "current_floor",
            "next_destination",
            "direction",
            "is_moving",
            "is_door_open",
            "is_working",
        ]
