import mysql.connector

# Connect to MySQL Server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD"  # Replace with your local MySQL password
)

cur = conn.cursor()

# Auto-create database and table
cur.execute("CREATE DATABASE IF NOT EXISTS railway_new")
cur.execute("USE railway_new")

cur.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    train_no VARCHAR(10),
    source VARCHAR(30),
    destination VARCHAR(30)
)
""")
print("Database & table initialized successfully.")

def book_ticket():
    try:
        name = input("Passenger Name: ")
        age = int(input("Age: "))
        train_no = input("Train No: ")
        source = input("From: ")
        destination = input("To: ")
        
        query = "INSERT INTO tickets (name, age, train_no, source, destination) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (name, age, train_no, source, destination))
        conn.commit()
        print("✔ Ticket booked successfully!")
    except ValueError:
        print("❌ Invalid input! Age must be a number.")

def show_tickets():
    cur.execute("SELECT * FROM tickets")
    data = cur.fetchall()
    if data:
        print("\n--- ALL BOOKED TICKETS ---")
        for row in data:
            print(f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Train: {row[3]} | From: {row[4]} -> To: {row[5]}")
    else:
        print("No records found.")

def search_ticket():
    name = input("Enter passenger name to search: ")
    cur.execute("SELECT * FROM tickets WHERE name LIKE %s", (f"%{name}%",))
    data = cur.fetchall()
    if data:
        for row in data:
            print(f"ID: {row[0]} | Name: {row[1]} | Train: {row[3]} | {row[4]} -> {row[5]}")
    else:
        print("No passenger found with that name.")

def delete_ticket():
    try:
        tid = int(input("Enter Ticket ID to delete: "))
        cur.execute("DELETE FROM tickets WHERE ticket_id = %s", (tid,))
        conn.commit()
        print("✔ Ticket deleted successfully!")
    except ValueError:
        print("❌ Invalid Ticket ID.")

def update_destination():
    try:
        tid = int(input("Enter Ticket ID: "))
        new_dest = input("Enter New Destination: ")
        cur.execute("UPDATE tickets SET destination = %s WHERE ticket_id = %s", (new_dest, tid))
        conn.commit()
        print("✔ Destination updated!")
    except ValueError:
        print("❌ Invalid Ticket ID.")

def count_tickets():
    cur.execute("SELECT COUNT(*) FROM tickets")
    result = cur.fetchone()
    print(f"Total Tickets Booked: {result[0]}")

# Menu Loop
while True:
    print("\n--- Railway Ticket Management System ---")
    print("1. Book Ticket")
    print("2. Show All Tickets")
    print("3. Search Ticket by Name")
    print("4. Delete Ticket by ID")
    print("5. Update Destination")
    print("6. Count Total Tickets")
    print("7. Exit")
    
    choice = input("Enter choice (1-7): ")
    
    if choice == '1':
        book_ticket()
    elif choice == '2':
        show_tickets()
    elif choice == '3':
        search_ticket()
    elif choice == '4':
        delete_ticket()
    elif choice == '5':
        update_destination()
    elif choice == '6':
        count_tickets()
    elif choice == '7':
        print("Thank you for using the system!")
        break
    else:
        print("Invalid choice. Please choose 1-7.")

conn.close()
