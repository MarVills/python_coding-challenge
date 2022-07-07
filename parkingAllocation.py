# Marben Villaflor

import math
import datetime
import random

error_message = "Please select from the choices only!"
entrances = ["Entance 1", "Entrance 2", "Entrance 3"]
type = ["Small", "Medium", "Large"]
vehicle_type = ["S","M","L"]
parking_type = ["SP", "MP", "LP"]
parked_vehicles = []
slot_distances = [(1, 4, 5), (3, 2, 3), (2, 4, 3), (5, 3, 4), (1, 5, 4), (4, 1, 3), (4, 5, 4), (2, 2, 1), (2, 3, 2)]
parking_slots = [0, 2, 1, 1, 0, 0, 2, 2, 1]
occupied_slots = []

# available slots for vehicle type 
# small = 9
# medium = 6
# large = 3

def message(messType, message):
  mess_bar = "**********"
  err_bar = "=========="
  if (messType == "error"): print("\n\n" + err_bar + " " + message + " " + err_bar)
  # elif(messType == "customError"): print("\n\n" + err_bar + " " + message + " " + err_bar)
  else: print("\n\n" + mess_bar + " " + message + " " + mess_bar)

def parkingDetails(): 
  entrance = 0
  vehicle_type = 0
  plate_number = ""
  while True: # Getting Entrance number 
    try:
      entrance = int(input("\nEntrance 1 = 1\nEntrance 2 = 2\nEntrance 3 = 3\n\nSelect Entrance Number: "))
      if(entrance == 1 or entrance == 2 or entrance == 3):
        break
      else:
        message("error", error_message)
    except ValueError:
      message("error", error_message)
      continue
  while True: # Getting Vehicle type 
    try:
      vehicle_type = int(input("\nSmall Vehicles = 1\nMedium Vehicles = 2\nLarge Vehicles = 3\n\nEnter Vehicle Type: "))
      if(vehicle_type == 1 or vehicle_type == 2 or vehicle_type == 3):
        break
      else:
        message("error", error_message)
    except ValueError:
      message("error", error_message)
      continue
  while True: # Getting Plate number 
      plate_number = str(input("\nEnter Plate Number: ")).strip()
      if(plate_number != "" or plate_number != " "): break
      else: continue
        
  return entrance - 1, vehicle_type - 1, plate_number

def getAssignedSlot(entrance, vehicle_type): # Assigning parking slot 
  available_slots = []
  distances = []
  near_slot = {}
  for slot in range(len(parking_slots)):
    if(vehicle_type == 0):
      if(slot not in occupied_slots):
        available_slots.append(slot)
    elif(vehicle_type == 1):
      if(parking_slots[slot] >= 1 and slot not in occupied_slots):
        available_slots.append(slot)
    else:
      if(parking_slots[slot] == 2 and slot not in occupied_slots):
        available_slots.append(slot)
  for slot in available_slots:
    distances.append(slot_distances[slot][entrance])
    near_slot[slot_distances[slot][entrance]] = slot
  return None if available_slots == [] else near_slot.get(min(distances))

def parkVehicle(detail): # Parking vehicle
  parking_details = list(detail)
  current_time = datetime.datetime.now()
  set_slot = getAssignedSlot(parking_details.pop(0), detail[1])
  if set_slot == None: 
    print("\nThere are no available slot for this vehicle!\n")
    isContinue() 
  parking_details.append(current_time)
  parking_details.append(set_slot)
  message("message", "Parking Vehicle")
  occupied_slots.append(parking_details[3])
  parked_vehicles.append(parking_details)
  print("\n", "Vehicle Type: ", type[parking_details[0]],"\n", "Plate Number: ", parking_details[1] ,"\n", "Parking Time: ", parking_details[2] ,"\n", "Parking Slot: ", parking_details[3])
# ----------------------------------------------------------
def calculatePayment(parking_time):
  parking_fee = 0
  unpark_time = datetime.datetime.now()
  total_time = unpark_time - parking_time
  print(total_time.total_seconds())
  # park_time = round(math.ceil(total_time.total_seconds()) / 3600)
  print(parking_time)
  print(unpark_time)
  print(total_time)
  return parking_fee

def unparkVehicle(slot): # Unparking vehicle
  for s in parked_vehicles:
    if(slot == s[3]):
      parking_fee = calculatePayment(s[2])
      message("message", "Unparking Vehicle")
      parked_vehicles.remove(s)
      occupied_slots.remove(slot)
  isContinue()
# ----------------------------------------------------------
def pakingStatus(): # Parking status/information
  print("")
  if(parked_vehicles == []):
    print("All parking slots are available!\n")
    isContinue()
  else:
    for parked in parked_vehicles:
      print("\n","Vehicle Type: ",type[parked[0]],"\n","Plate Number: ",parked[1],"\n", "Parking Time: ", parked[2] ,"\n", "Parking Slot: ", parked[3])

def isContinue():
  run_program = True
  while run_program:
    is_continue = input("Continue? y/n: ")
    if(is_continue == "y"): menu()
    elif(is_continue == "n"): exit()
    else: continue

def menu():
  message("message", "Menu")
  while True:
    try:
      menu = int(input("\nPark Vehicle = 1 \nUnpark Vehicle = 2 \nParking Status = 3 \nExit = 0\n\nEnter Menu Number: "))
      if(menu == 0):
        exit()
      elif(menu == 1):
        details = parkingDetails()
        parking_details = (details[0],details[1], details[2])
        parkVehicle(parking_details)
      elif(menu == 2):
        while True:
          if(occupied_slots == []):
              print("No vehicle in the parking complex!")
              break
          try:
            parking_slot = int(input("Enter occupied slot: "))
            if(parking_slot in occupied_slots):
              unparkVehicle(parking_slot)
              break
            elif(parking_slot < 9 or parking_slot >=0): 
              print("\nThis slot is not occupied!\n")
              print(occupied_slots)
            else: print("\nInvalid slot!\n")
          except ValueError as e:
            message("error", "Please enter valid occupied slot!")
            print(e)
            continue
      elif(menu == 3):
        message("message", "Parking Status")
        pakingStatus()
      else:
        message("error", error_message)
    except ValueError as e: 
      message("error", error_message)
      print(e)
      continue

menu()