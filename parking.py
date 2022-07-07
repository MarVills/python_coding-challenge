# Kyle Joseph Timajo

import datetime
import math

flat_rate = 40
additional_rate = [20, 60, 100]
entry_count = 3
parking_slots = [0, 2, 1, 0, 1, 0, 2, 1, 2]
slot_distance = [(1, 4, 5), (3, 2, 3), (1, 2, 1), (2, 1, 5), (6, 4, 2), (3, 1, 5), (4, 3, 2), (3, 2, 4), (1, 4, 3)]
occupied_slots = []
parking_info = []

#Tester for existing parking
# occupied_slots = [2]
# parking_info = [(1, "KEV 1234", datetime.datetime(2022, 7, 4, 9, 25, 17))]

def chooseMenu():
    while True:
        try:
            menu = int(input("\nPark = 0 Unpark = 1 Parked Vehicles = 2\nChoose Menu: "))
            if(menu == 0):
                return park(getVehicleInfo())
            elif(menu == 1):
                return unpark(getUnparkInfo())
            elif(menu == 2):
                return getOccupiedSlots()
            else:
                print("Invalid menu type.")
        except ValueError:
            print("Please enter an integer value.")
            continue

def getVehicleInfo():
    while True:
        try:
            entrance = int(input("\nEntrance 1 = 0\nEntrance 2 = 1\nEntrance 3 = 2\nEnter Entrance Gate: "))
            if(entrance >= 0 and entrance <=2):
                break
            else:
                print("Invalid entrance number.")
        except ValueError:
            print("Please enter an integer value.")
            continue

    while True:
        plate_number = str(input("\nEnter Vehicle Plate Number: ")).strip()
        if(plate_number != ""):
            break
        continue

    while True:
        try:
            vehicle_type = int(input("\nSmall Vehicles = 0\nMedium Vehicles = 1\nLarge Vehicles = 2\nEnter Vehicle Type: "))
            if(vehicle_type >= 0 and vehicle_type <=2):
                break
            else:
                print("Invalid vehicle type.")
        except ValueError:
            print("Please enter an integer value.")
            continue

    return {"entrance" : entrance, "vehicle_type": vehicle_type, "plate_number": plate_number.upper()}

def getVacantSlotsByType(vehicle_type):
    vacant_slots = []
    for idx in range(len(parking_slots)):
        if parking_slots[idx] == vehicle_type and idx not in occupied_slots:
            vacant_slots.append(idx)

    return vacant_slots

def getNearestSlot(entrance, vehicle_type):
    vacant_slots = getVacantSlotsByType(vehicle_type)
    if len(vacant_slots) != 0:
        nearest_slot = vacant_slots[0]
        nearest_distance = slot_distance[nearest_slot][entrance]
        for slot in vacant_slots:
            distance = slot_distance[slot][entrance]
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_slot = slot

        return nearest_slot
    return None

def getParkingSlot(entrance, original_vehicle_type, vehicle_type,):
    nearest_slot = getNearestSlot(entrance, vehicle_type)

    if(original_vehicle_type == 0):
        if nearest_slot == None and vehicle_type < 2:
            vehicle_type = vehicle_type + 1
            return getParkingSlot(entrance, original_vehicle_type, vehicle_type)
        else:
            return nearest_slot
    elif(original_vehicle_type == 1):
        if nearest_slot == None and vehicle_type < 2:
            vehicle_type = vehicle_type + 1
            return getParkingSlot(entrance, original_vehicle_type, vehicle_type)
        else:
            return nearest_slot
    elif(original_vehicle_type == 2):
        return nearest_slot

def getOccupiedSlots():
    for idx in range(len(occupied_slots)):
        print("Vehicle Type: %s, Parking Slot: %s, Plate Number: %s, Date & Time of Entry: %s" % (parking_info[idx][0], occupied_slots[idx], parking_info[idx][1], parking_info[idx][2]))
    
    return chooseMenu()

def getUnparkInfo():
    while True:
        try:
            parking_slot = int(input("\nEnter Parking Slot Number: "))
            if(parking_slot >= 0 and parking_slot in occupied_slots):
                break
            else:
                print("Parking slot not found.")
                return chooseMenu()
        except ValueError:
            print("Please enter an integer value.")
            continue

    return parking_slot

def removeOccupiedSlot(slot_index):
    occupied_slots.pop(slot_index)
    parking_info.pop(slot_index)



def getParkingHours(slot_index):
    datetime_now = datetime.datetime.now()
    park_datetime = parking_info[slot_index][2]
    time_difference = datetime_now - park_datetime
    parking_hours = math.ceil(math.ceil(time_difference.total_seconds()) / 3600)
    
    return parking_hours

def calculateParkingFee(slot_index):
    parking_fee = 0
    vehicle_type = parking_info[slot_index][0]
    parking_hours = getParkingHours(slot_index)

    if(parking_hours > 24):
        exceeding_rate = (parking_hours // 24) * 5000
        remaining_rate = (parking_hours % 24) * additional_rate[vehicle_type]
        parking_fee = exceeding_rate + remaining_rate

    elif(parking_hours <= 24 and parking_hours > 3):
        parking_fee = ((parking_hours - 3) * additional_rate[vehicle_type]) + flat_rate

    elif(parking_hours > 0 and parking_hours <= 3):
        parking_fee = flat_rate

    return parking_fee

def park(vehicle_info):
    parking_slot = getParkingSlot(vehicle_info["entrance"], vehicle_info["vehicle_type"], vehicle_info["vehicle_type"])
    if(parking_slot != None):
        occupied_slots.append(parking_slot)
        park_datetime = datetime.datetime.now()
        parking_info.append((vehicle_info["vehicle_type"], vehicle_info["plate_number"], park_datetime))
        print("\nVechicle Type: %s\nPlate Number: %s\nParking Slot: %s" % (vehicle_info["vehicle_type"], vehicle_info["plate_number"], parking_slot))
    else:
        print("There are no available parking slot.")
        
    return chooseMenu()

def unpark(parking_slot):
    if(len(occupied_slots) > 0):
        slot_index = occupied_slots.index(parking_slot)
        total_hours = getParkingHours(slot_index)
        parking_fee = calculateParkingFee(slot_index)
        removeOccupiedSlot(slot_index)

        print("\nTotal Parking Hours: %d\nTotal Parking Fee: %d" % (total_hours, parking_fee))
    else:
        print("Parking slot not found.")
    
    return chooseMenu()

def main():
    chooseMenu()
    


main()
