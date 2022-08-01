def findTheClosestElevator(available_elevators, number_of_elevators, requested_floor):
    if requested_floor <= available_elevators[0].current_floor:
        return available_elevators[0]
    if requested_floor >= available_elevators[number_of_elevators - 1].current_floor:
        return available_elevators[number_of_elevators - 1]
    i = 0
    j = number_of_elevators
    mid = 0
    while i < j:
        mid = (i + j) // 2

        if available_elevators[mid].current_floor == requested_floor:
            return available_elevators[mid]
        if requested_floor < available_elevators[mid].current_floor:
            if mid > 0 and requested_floor > available_elevators[mid - 1].current_floor:
                return getClosest(
                    available_elevators[mid - 1],
                    available_elevators[mid],
                    requested_floor,
                )

            j = mid

        else:
            if (
                mid < number_of_elevators - 1
                and requested_floor < available_elevators[mid + 1].current_floor
            ):
                return getClosest(
                    available_elevators[mid],
                    available_elevators[mid + 1],
                    requested_floor,
                )

            i = mid + 1
    return available_elevators[mid]


def getClosest(val1, val2, target):
    if target - val1 >= val2 - target:
        return val2
    else:
        return val1
