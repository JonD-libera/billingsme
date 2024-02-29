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

character_classes = {
    "Network Engineer": {"server_failure_rate_modifier": 0.8, "description": "Expert in preventing and fixing network issues."},
    "Database Administrator": {"database_fix_time_modifier": 0.75, "description": "Skilled in managing and optimizing databases."},
    "Software Developer": {"application_issue_resolution_time_modifier": 0.75, "description": "Efficient in solving application-related problems."}
}

# Initialize database connection
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
def get_random_customer():
    cur.execute('SELECT name, serverId FROM customers WHERE status = "pending" LIMIT 1')
    result = cur.fetchone()
    if result:
        return result
    return None

def update_customer_status(name, status):
    cur.execute('UPDATE customers SET status = ? WHERE name = ?', (status, name))
    conn.commit()

def convert_minutes_to_hms(minutes, start_hour):
    hours = int(minutes // 60) + start_hour
    minutes = int(minutes % 60)
    seconds = int((minutes - int(minutes)) * 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def simulate_billing(game_start_time, character_class):
    while True:
        if character_class == "Software Developer":
            start_time = START_HOUR - 1
        else:
            start_time = START_HOUR
        current_time = convert_minutes_to_hms((time.time()-game_start_time), start_time)
        if current_time >= f"{END_HOUR}:{END_MINUTE}":
            print("Time's up! The game has ended.")
            break

        customer_name, serverId = get_random_customer()

        if not customer_name:
            print("All customers have been billed. Congratulations!")
            break
        serverId = str(serverId)
        print(f"{current_time} - Begin billing for customer {customer_name}")
        failure_chance = randint(1, 100)

        # Simulate failures
        fail_count = 0
        if failure_chance <= 2: 
            print(f"{current_time} - Server failure encountered for {customer_name}")
            fix_command = input("Type 'repair table cdr "+serverId+"' to fix the server failure: ").strip().lower()
            if character_class == "Database Administrator":
                skip_chance = randint(1, 100)
            else:
                skip_chance = 0
            if skip_chance > 75:
                print(f"{current_time} - {character_class} has quickly resolved {customer_name} due to their mad skills in database issue resolution.")
                update_customer_status(customer_name, "completed")
            while fix_command != ("repair table cdr "+serverId).strip().lower():
                time.sleep(3)
                print("Incorrect command. Billing for this customer delayed. Try again.")
                fix_command = input("Type 'repair table cdr "+serverId+"' to fix the server failure: ").strip().lower()
            update_customer_status(customer_name, "completed")
        elif failure_chance <= 4: 
            print(f"{current_time} - Negative invoice encountered for {customer_name}")
            fix_command = input("Type 'update invoice where customer_name = "+customer_name+"' to fix the negative invoice: ").strip().lower()
            while fix_command != ("update invoice where customer_name = "+customer_name).strip().lower():
                fail_count += 1
                time.sleep(3)
                if fail_count > 1:
                    print(f"You have updated the wrong record. Now you must restore from backup.")
                    fix_command = input("Type 'mysql < backup.sql' to restore the table: ").strip().lower()
                    while fix_command != ("mysql < backup.sql").strip().lower():
                        time.sleep(30)
                        print("Incorrect command. Try again.")
                        fix_command = input("Type 'mysql < backup.sql' to restore the table: ").strip().lower()
                    print(f"{current_time} - Backup restored.")
                    fix_command = input("Type 'update invoice where customer_name = "+customer_name+"' to fix the negative invoice: ").strip().lower()
                print("Incorrect command. Billing for this customer delayed. Try again.")
                fix_command = input("Type 'update invoice where customer_name = "+customer_name+"' to fix the negative invoice: ").strip().lower()
            update_customer_status(customer_name, "completed")
        elif failure_chance <= 5:
            print(f"{current_time} - Customer {customer_name} has an incorrect mtu set on their fax machine.")
            if character_class == "Network Engineer":
                skip_chance = randint(1, 100)
            else:
                skip_chance = 0
            if skip_chance > 75:
                print(f"{current_time} - {character_class} has quickly resolved {customer_name} due to their mad skills in network issue resolution.")
                update_customer_status(customer_name, "completed")
            else:
                fix_command = input("Type 'set mtu 1500' to fix the customer's fax machine: ").strip().lower()
                while fix_command != ("set mtu 1500").strip().lower():
                    time.sleep(3)
                    print("Incorrect command. Billing for this customer delayed. Try again.")
                    fix_command = input("Type 'set mtu 1500' to fix the customer's fax machine: ").strip().lower()
        elif failure_chance <= 6:
            print(f"{current_time} - Customer {customer_name} has an error calculating taxes.")
            if character_class == "Software Developer":
                skip_chance = randint(1, 100)
            else:
                skip_chance = 0
            if skip_chance > 75:
                print(f"{current_time} - {character_class} has skipped the tax calculation for {customer_name} due to their mad skills in application issue resolution.")
                update_customer_status(customer_name, "completed")
            else:
                fix_command = input("Type 'recalculate taxes' to fix the tax calculation: ").strip().lower()
                while fix_command != ("recalculate taxes").strip().lower():
                    time.sleep(3)
                    print("Incorrect command. Billing for this customer delayed. Try again.")
                    fix_command = input("Type 'recalculate taxes' to fix the tax calculation: ").strip().lower()
        elif failure_chance <= 8:
            print(f"{current_time} - Customer {customer_name} is reflecting packets back to our network from random internet baddies.")
            if character_class == "Network Engineer":
                skip_chance = randint(1, 100)
            else:
                skip_chance = 0
            if skip_chance > 75:
                print(f"{current_time} - {character_class} has quickly resolved {customer_name} due to their mad skills in network issue resolution.")
                update_customer_status(customer_name, "completed")
            else:
                fix_command = input("Type 'iptables block "+customer_name+"' to stop the evil traffic: ").strip().lower()
                while fix_command != ("iptables block "+customer_name).strip().lower():
                    time.sleep(3)
                    print("Incorrect command. Billing for this customer delayed. Try again.")
                    fix_command = input("Type 'iptables block "+customer_name+"' to stop the evil traffic: ").strip().lower()
        else:
            update_customer_status(customer_name, "completed")
        sleep_time = round(random.uniform(0, .2), 2)
        time.sleep(sleep_time)
        print(f"{current_time} - Billing completed for {customer_name}.")

def start_game_clock(character_class):
    # Initialize game time to 03:00
    os.environ['TZ'] = 'UTC'
    time.tzset()
    start_time = time.mktime(time.strptime('03:00', '%H:%M'))
    time.localtime(start_time)
    game_start_time=time.time()
    simulate_billing(game_start_time, character_class)
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
    character_class = select_character_class()
    generate_customers()
    print('Starting a new game...')
    # Placeholder for further game initialization steps
    return character_class

def resume_game():
    print('Resuming game...')
    # Placeholder for game resumption logic

def select_character_class():
    print("Please select your character class:")
    for i, (class_name, class_info) in enumerate(character_classes.items(), start=1):
        print(f"{i}. {class_name} - {class_info['description']}")
    selection = input("Enter the number of your chosen class: ")
    try:
        selected_class = list(character_classes.keys())[int(selection) - 1]
        print(f"You have selected {selected_class}.")
        return selected_class
    except (ValueError, IndexError):
        print("Invalid selection. Please select a valid class number.")
        return select_character_class()  # Recursively prompt until a valid selection is made

def print_with_delay(text, delay=1/100):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def main():
    setup_database()
    print_with_delay('Welcome to Billing Sme Simulator!!\n The day... February 28th, 2019.\n The mission... to bill all the customers before midnight.')
    print()
    
    character_class=start_new_game()
    input('Press enter to begin billing...')
    print_with_delay('\n\nAs long as absolutely nothing goes wrong, we should be fine. Good luck!\n')
    start_game_clock(character_class)

if __name__ == '__main__':
    main()
