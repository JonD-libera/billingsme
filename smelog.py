#!/usr/bin/env python3
import sqlite3
import os
from random import randint, choice
import random
import time

# Constants
DB_PATH = 'game_state.db'
CUSTOMER_COUNT = 3000
SERVER_COUNT = 100
START_HOUR = 3
END_HOUR = 23
END_MINUTE = 59

# Initialize database connection
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
def get_random_customer():
    cur.execute('SELECT name FROM customers WHERE status = "pending" LIMIT 1')
    result = cur.fetchone()
    if result:
        return result[0]
    return None

def update_customer_status(name, status):
    cur.execute('UPDATE customers SET status = ? WHERE name = ?', (status, name))
    conn.commit()

def convert_minutes_to_hms(minutes):
    hours = int(minutes // 60) + START_HOUR
    minutes = int(minutes % 60)
    seconds = int((minutes - int(minutes)) * 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def simulate_billing(game_start_time):
    while True:
        current_time = convert_minutes_to_hms((time.time()-game_start_time))
        if current_time >= f"{END_HOUR}:{END_MINUTE}":
            print("Time's up! The game has ended.")
            break

        customer_name = get_random_customer()
        if not customer_name:
            print("All customers have been billed. Congratulations!")
            break

        print(f"{current_time} - Begin billing for customer {customer_name}")
        failure_chance = randint(1, 100)

        # Simulate failures
        if failure_chance <= 3:  # 10% chance of server failure
            print(f"{current_time} - Server failure encountered for {customer_name}")
            fix_command = input("Type 'repair table cdr' to fix the server failure: ").strip().lower()
            while fix_command != "repair table cdr":
                time.sleep(3)
                print("Incorrect command. Billing for this customer delayed. Try again.")
                fix_command = input("Type 'repair table cdr' to fix the server failure: ").strip().lower()
            update_customer_status(customer_name, "completed")
        elif failure_chance <= 5:  # Additional 5% chance of negative invoice, total 15%
            print(f"{current_time} - Negative invoice encountered for {customer_name}")
            fix_command = input("Type 'update invoice' to fix the negative invoice: ").strip().lower()
            while fix_command != "update invoice":
                time.sleep(3)
                print("Incorrect command. Billing for this customer delayed. Try again.")
                fix_command = input("Type 'update invoice' to fix the negative invoice: ").strip().lower()
            update_customer_status(customer_name, "completed")
        else:
            update_customer_status(customer_name, "completed")
        sleep_time = round(random.uniform(0, .2), 2)
        time.sleep(sleep_time)
        print(f"{current_time} - Billing completed for {customer_name}.")

def start_game_clock():
    # Initialize game time to 03:00
    os.environ['TZ'] = 'UTC'
    time.tzset()
    start_time = time.mktime(time.strptime('03:00', '%H:%M'))
    time.localtime(start_time)
    game_start_time=time.time()
    simulate_billing(game_start_time)
def setup_database():
    cur.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        serverId INTEGER NOT NULL,
        status TEXT NOT NULL,
        invoiceTotal REAL
    )''')
    conn.commit()

def clear_customers():
    cur.execute('DELETE FROM customers')
    conn.commit()

def generate_customers():
    clear_customers()
    for i in range(1, CUSTOMER_COUNT + 1):
        name = f'Customer_{i}'
        server_id = randint(1, SERVER_COUNT)
        cur.execute('INSERT INTO customers (name, serverId, status, invoiceTotal) VALUES (?, ?, ?, ?)',
                    (name, server_id, 'pending', None))
    conn.commit()

def start_new_game():
    print('Starting a new game...')
    generate_customers()
    # Placeholder for further game initialization steps

def resume_game():
    print('Resuming game...')
    # Placeholder for game resumption logic

def main():
    setup_database()
    input('Welcome to Billing Sme Simulator!! The day... February 28th, 2019. The mission... to bill all the customers before midnight. Press enter to begin.')
    print()
    choice = input('Would you like to resume the current game or start a new one? (resume/new): ').strip().lower()
    if choice == 'new':
        print('\n\nAs long as absolutely nothing goes wrong, we should be fine. Good luck!\n')
        start_new_game()
    else:
        resume_game()
    input('Press enter to begin billing...')
    start_game_clock()

if __name__ == '__main__':
    main()
