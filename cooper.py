from enum import Enum
from datetime import datetime, timedelta
import math

class vehicleType(Enum) :
    Car = 1
    Bike = 2
    Truck = 3

class Vehicle :
    def __init__ (self,vehiclenum,type,ownername) :
        self.vehiclenum=vehiclenum
        self.type=type
        self.ownername=ownername
    def get_Type(self) :
        return self.type
    def get_vehiclenum(self) :
        return self.vehiclenum
    def get_ownername(self) :
        return self.ownername
    def matches(self, slot) :
        if self.type == slot.type :
            return True
        else :
            return False
class ticket :
    def __init__ (self,ticketid,vehiclenum,slotid,entrytime,exittime) :
        self.ticketid=ticketid
        self.vehiclenum=vehiclenum
        self.slotid=slotid
        self.entrytime=entrytime
        self.exittime=exittime
    def generate_bill(self, billing_engine) :
        duration = self.exittime - self.entrytime
        hours = math.ceil(duration.total_seconds()/3600)
        return billing_engine.calculate_bill(hours)
    def close_ticket(self, exittime) :
        self.exittime = exittime
class ParkingSlot :
    def __init__ (self,slotid,floor,row,type,isOccupied) :
        self.slotnum=slotid
        self.floor=floor
        self.row=row
        self.type=type
        self.isOccupied=isOccupied
    def occupy(self) :
        self.isOccupied = True
    def vacate(self) :
        self.isOccupied = False
    def get_location(self) :
        return (self.floor, self.row, self.slotnum)
class Parkinglot :
    def __init__ (self,name,floors,slots,ratecard) :
        self.name=name
        self.floors=floors
        self.num_slots=slots
        self.ratecard=ratecard
        # Initialize 2D array of parking slots
        self.slots = []
        slots_per_floor = slots // floors
        for i in range(floors):
            floor_slots = []
            for j in range(slots_per_floor):
                floor_slots.append(ParkingSlot(f"{i}-{j}", i, j, vehicleType.Car, False))
            self.slots.append(floor_slots)
    def find_slot(self, vehicle) :
        for i in range(self.floors):
            for j in range(self.num_slots//self.floors):
                slot = self.slots[i][j]
                if not slot.isOccupied and vehicle.matches(slot):
                    return slot
        return None
    def addfloor(self) :
        self.floors += 1
    def getOccupancy(self) :
        total_slots = self.floors * (self.num_slots // self.floors)
        occupied_slots = sum(1 for i in range(self.floors) for j in range(self.num_slots//self.floors) if self.slots[i][j].isOccupied)
        return occupied_slots / total_slots if total_slots > 0 else 0
class BillingEngine :
    def __init__ (self,type) :
        self.type=type
        self.rate_per_hour = 10.0
    def compute_bill(self, duration,vehicleType) :
        if vehicleType == "Car" :
            self.rate_per_hour = 10.0
        elif vehicleType == "Bike" :
            self.rate_per_hour = 5.0
        elif vehicleType == "Truck" :
            self.rate_per_hour = 15.0
        return duration * self.rate_per_hour
    def applypass(self, parking_pass) :
        if parking_pass.type == "Monthly" :
            self.rate_per_hour *= 0.8
        elif parking_pass.type == "Yearly" :
            self.rate_per_hour *= 0.5
    def calculate_bill(self, hours) :
        return hours * self.rate_per_hour
class Pass :
    def __init__ (self, passid, type, valid_until) :
        self.passid=passid
        self.type=type
        self.valid_until=valid_until
    def is_valid(self) :
        return datetime.now() < self.valid_until
if __name__ == "__main__":
    print("=== Parking Lot Management System ===\n")
    
    # Initialize parking lot
    lot_name = input("Enter parking lot name (default: Central Park): ").strip() or "Central Park"
    floors = int(input("Enter number of floors (default: 3): ").strip() or "3")
    slots = int(input("Enter total number of slots (default: 30): ").strip() or "30")
    
    parking_lot = Parkinglot(lot_name, floors, slots, None)
    billing_engine = BillingEngine("Standard")
    tickets = {}
    vehicle_records = []  # Store all completed transactions
    vehicle_count = 0
    
    while True:
        print("\n--- Menu ---")
        print("1. Park a vehicle")
        print("2. Retrieve a vehicle")
        print("3. Check occupancy")
        print("4. Apply parking pass")
        print("5. View all user records")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            vehicle_count += 1
            vehicle_num = input("Enter vehicle number: ").strip()
            owner_name = input("Enter owner name: ").strip()
            
            print("\nVehicle Types:")
            for i, vtype in enumerate(vehicleType, 1):
                print(f"{i}. {vtype.name}")
            vtype_choice = int(input("Select vehicle type (1-3): ").strip())
            vehicle_type = list(vehicleType)[vtype_choice - 1]
            
            vehicle = Vehicle(vehicle_num, vehicle_type, owner_name)
            slot = parking_lot.find_slot(vehicle)
            
            if slot:
                slot.occupy()
                ticket_id = f"T{vehicle_count}"
                entry_time = datetime.now()
                t = ticket(ticket_id, vehicle_num, slot.slotnum, entry_time, None)
                tickets[ticket_id] = (vehicle, slot, t)
                print(f"\n✓ Vehicle {vehicle_num} parked at slot {slot.get_location()}")
                print(f"Ticket ID: {ticket_id}")
            else:
                print("\n✗ No available slot for this vehicle type.")
        
        elif choice == "2":
            ticket_id = input("Enter ticket ID: ").strip()
            
            if ticket_id in tickets:
                vehicle, slot, t = tickets[ticket_id]
                hours = int(input("How many hours did the vehicle stay? ").strip())
                exit_time = t.entrytime + timedelta(hours=hours)
                t.close_ticket(exit_time)
                
                bill = t.generate_bill(billing_engine)
                print(f"\n✓ Vehicle {vehicle.get_vehiclenum()} retrieved from slot {slot.get_location()}")
                print(f"Bill amount: ${bill:.2f}")
                
                # Store record
                record = {
                    "ticket_id": ticket_id,
                    "vehicle_num": vehicle.get_vehiclenum(),
                    "owner_name": vehicle.get_ownername(),
                    "vehicle_type": vehicle.get_Type().name,
                    "slot": slot.get_location(),
                    "entry_time": t.entrytime.strftime("%Y-%m-%d %H:%M:%S"),
                    "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "hours": hours,
                    "bill_amount": bill
                }
                vehicle_records.append(record)
                
                slot.vacate()
                del tickets[ticket_id]
            else:
                print("\n✗ Ticket ID not found.")
        
        elif choice == "3":
            occupancy = parking_lot.getOccupancy()
            total = parking_lot.num_slots
            occupied = int(occupancy * total)
            print(f"\nOccupancy: {occupied}/{total} slots ({occupancy*100:.1f}%)")
        
        elif choice == "4":
            ticket_id = input("Enter ticket ID: ").strip()
            if ticket_id in tickets:
                print("\nPass Types:")
                print("1. Monthly")
                print("2. Yearly")
                pass_choice = input("Select pass type (1-2): ").strip()
                pass_type = "Monthly" if pass_choice == "1" else "Yearly"
                
                pass_id = input("Enter pass ID: ").strip()
                valid_until = datetime.now() + timedelta(days=30 if pass_choice == "1" else 365)
                parking_pass = Pass(pass_id, pass_type, valid_until)
                
                if parking_pass.is_valid():
                    billing_engine.applypass(parking_pass)
                    print(f"\n✓ {pass_type} pass applied!")
                else:
                    print("\n✗ Pass is not valid.")
            else:
                print("\n✗ Ticket ID not found.")
        
        elif choice == "5":
            if not vehicle_records:
                print("\n--- No records found ---")
            else:
                print("\n" + "="*120)
                print(f"{'Ticket ID':<12} {'Vehicle #':<12} {'Owner':<15} {'Type':<8} {'Slot':<15} {'Entry Time':<20} {'Exit Time':<20} {'Hours':<7} {'Bill':<10}")
                print("="*120)
                for record in vehicle_records:
                    print(f"{record['ticket_id']:<12} {record['vehicle_num']:<12} {record['owner_name']:<15} {record['vehicle_type']:<8} {str(record['slot']):<15} {record['entry_time']:<20} {record['exit_time']:<20} {record['hours']:<7} ${record['bill_amount']:<9.2f}")
                print("="*120)
                total_revenue = sum(r['bill_amount'] for r in vehicle_records)
                print(f"\nTotal Records: {len(vehicle_records)}")
                print(f"Total Revenue: ${total_revenue:.2f}")
        
        elif choice == "6":
            print("\nThank you for using Parking Lot Management System!")
            break
        
        else:
            print("\n✗ Invalid choice. Please try again.")
