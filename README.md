# Parking-Lot-System
This Parking Lot Management System is a robust, Python-based application designed to automate the daily operations of a commercial parking facility. Built using Object-Oriented Programming (OOP) principles, the system focuses on scalability, modularity, and data integrity, making it an ideal solution for managing multi-floor parking structures.
# Parking Lot Management System

A robust, Python-based application designed to automate the daily operations of a commercial parking facility. This system manages multi-floor structures, automates slot assignment, and handles complex billing logic.

## 🚀 Features

*   **Automated Slot Assignment:** Intelligent searching for available slots based on vehicle type (Car, Bike, Truck).
*   **Dynamic Billing Engine:** Strategy-based pricing that calculates fees based on duration and vehicle category.
*   **Membership Integration:** Supports Monthly and Yearly parking passes with automated discount application.
*   **Real-time Analytics:** Provides live occupancy rates and detailed transaction logs for administrators.
*   **Audit Trail:** Maintains a complete history of vehicle records, including entry/exit timestamps and total revenue.

## 🛠️ Technical Architecture

Built using **Object-Oriented Programming (OOP)** principles, the system is divided into modular components:
- **Vehicle & ParkingSlot:** Handles physical entity attributes and status tracking.
- **ParkingLot:** Manages the 2D grid of slots across multiple floors.
- **BillingEngine:** Processes financial logic and rounding (using `math.ceil`).
- **Ticket System:** Bridges the gap between entry data and final invoicing.

## 💻 Usage

1. **Initialize:** Run the script and set up your lot name, number of floors, and total capacity.
2. **Park:** Enter vehicle details; the system assigns a unique Ticket ID and coordinates.
3. **Retrieve:** Enter the Ticket ID and duration of stay. The system generates a bill and vacates the slot instantly.
4. **Monitor:** Use the menu to check live occupancy or view the history of all user records.

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com

# Navigate to the folder
cd Parking-Lot-System

# Run the application
python parking_lot.py
```

## 📝 License
This project is for educational purposes as part of a college submission.
