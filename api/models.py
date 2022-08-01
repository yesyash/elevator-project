from operator import mod
from django.db import models

import datetime


class ElevatorSystem(models.Model):
    number_of_elevators = models.IntegerField()
    number_of_floors = models.IntegerField()


class Elevator(models.Model):
    current_floor = models.IntegerField(default=1)
    next_destination = models.IntegerField(null=True)
    direction = models.TextField(max_length=100, null=True)
    is_moving = models.BooleanField(default=False)
    is_door_open = models.BooleanField(default=False)
    is_working = models.BooleanField(default=True)


class Requests(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    from_floor = models.IntegerField()
    to_floor = models.IntegerField()
    completes_by = models.BigIntegerField(null=True)
