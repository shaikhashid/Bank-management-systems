import mysql.connector
from datetime import datetime
from getpass import getpass

# Connect to MySQL




db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="narendra@2369",
    database="bank"
)
cursor = db.cursor()

# ---------- USER MODULES ----------

def register_user():
    name = input("Enter your Name: ")
    acc_type = input("Enter Account Type (Savings/Current): ")
    pin = getpass("Set your 4-digit PIN: ")
    cursor.execute("INSERT INTO users (name, account_type, amount, pin) VALUES (%s, %s, %s, %s)", 
                   (name, acc_type, 0.0, pin))
    db.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    acc_no = cursor.fetchone()[0]
    print(f"Registration successful! Your Account Number is: {acc_no}")

def login_user():
    acc_no = input("Enter Account Number: ")
    pin = getpass("Enter PIN: ")
    cursor.execute("SELECT * FROM users WHERE account_no=%s AND pin=%s", (acc_no, pin))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        user_menu(acc_no)
    else:
        print("Invalid credentials.")

def user_menu(acc_no):
    while True:
        print("\n1. View Account Details\n2. Debit Amount\n3. Credit Amount\n4. Change PIN\n5. View Statement\n6. Logout")
        ch = input("Enter choice: ")
        if ch == '1':
            cursor.execute("SELECT account_no, name, account_type, amount FROM users WHERE account_no=%s", (acc_no,))
            acc = cursor.fetchone()
            print(f"Name: {acc[1]}, Account No: {acc[0]}, Type: {acc[2]}, Balance: ₹{acc[3]}")
            log_action(acc_no, "view_account", 0)
        elif ch == '2':
            amt = float(input("Enter amount to debit: "))
            cursor.execute("SELECT amount FROM users WHERE account_no=%s", (acc_no,))
            bal = cursor.fetchone()[0]
            if bal >= amt:
                cursor.execute("UPDATE users SET amount = amount - %s WHERE account_no=%s", (amt, acc_no))
                log_action(acc_no, "debit", amt)
                db.commit()
                print("Amount debited.")
            else:
                print("Insufficient balance.")
        elif ch == '3':
            amt = float(input("Enter amount to credit: "))
            cursor.execute("UPDATE users SET amount = amount + %s WHERE account_no=%s", (amt, acc_no))
            log_action(acc_no, "credit", amt)
            db.commit()
            print("Amount credited.")
        elif ch == '4':
            new_pin = getpass("Enter new PIN: ")
            cursor.execute("UPDATE users SET pin = %s WHERE account_no=%s", (new_pin, acc_no))
            log_action(acc_no, "pin_change", 0)
            db.commit()
            print("PIN changed successfully.")
        elif ch == '5':
            cursor.execute("SELECT * FROM transactions WHERE account_no=%s", (acc_no,))
            print("\n--- Transaction History ---")
            for row in cursor.fetchall():
                print(row)
        elif ch == '6':
            break

def log_action(acc_no, action_type, amt):
    cursor.execute("INSERT INTO transactions (account_no, action_type, amount) VALUES (%s, %s, %s)",
                   (acc_no, action_type, amt))
    db.commit()

# ---------- ADMIN MODULES ----------

def admin_login():
    aid = input("Enter Admin ID: ")
    pwd = getpass("Enter Password: ")
    cursor.execute("SELECT * FROM admin WHERE admin_id=%s AND password=%s", (aid, pwd))
    admin = cursor.fetchone()
    if admin:
        print("Admin login successful!")
        admin_menu()
    else:
        print("Invalid Admin credentials.")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View All Users\n2. View User Account Details\n3. View User Transactions\n4. View Transactions by Date\n5. Logout")
        ch = input("Choose option: ")
        if ch == '1':
            cursor.execute("SELECT account_no, name, account_type, amount, pin FROM users")
            for user in cursor.fetchall():
                masked_pin = '*' * len(user[4])
                print(f"Account No: {user[0]}, Name: {user[1]}, Type: {user[2]}, Balance: ₹{user[3]}, PIN: {masked_pin}")
        elif ch == '2':
            acc = input("Enter Account Number: ")
            cursor.execute("SELECT account_no, name, account_type, amount, pin FROM users WHERE account_no=%s", (acc,))
            user = cursor.fetchone()
            if user:
                masked_pin = '*' * len(user[4])
                print(f"Account No: {user[0]}, Name: {user[1]}, Type: {user[2]}, Balance: ₹{user[3]}, PIN: {masked_pin}")
            else:
                print("Account not found.")
        elif ch == '3':
            acc = input("Enter Account Number: ")
            cursor.execute("SELECT * FROM transactions WHERE account_no=%s", (acc,))
            print(f"\n--- Transactions for Account {acc} ---")
            for row in cursor.fetchall():
                print(row)
        elif ch == '4':
            date = input("Enter Date (YYYY-MM-DD): ")
            cursor.execute("SELECT * FROM transactions WHERE DATE(date_time)=%s", (date,))
            print(f"\n--- Transactions on {date} ---")
            for row in cursor.fetchall():
                print(row)
        elif ch == '5':
            break

# ---------- MAIN ----------

def main():
    while True:
        print("\n--- Bank Management System ---")
        print("1. User Register\n2. User Login\n3. Admin Login\n4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            admin_login()
        elif choice == '4':
            print("Thank you for using the system!")
            break

main()
