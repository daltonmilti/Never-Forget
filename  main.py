import os
import csv
import pandas as pd
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials from .env
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("YOUR_PHONE_NUMBER")

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def load_birthdays(filename="birthdays.csv"):
    return pd.read_csv(filename)

def check_birthdays():
    today_str = datetime.today().strftime("%m-%d")
    df = load_birthdays()
    
    # Find today's birthdays
    today_birthdays = df[df["birthday"] == today_str]
    
    return today_birthdays

def send_sms(to, message):
    """Send an SMS message using Twilio"""
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to
    )

def add_birthday(filename="birthdays.csv"):
    """Function to add a new birthday entry."""
    name = input("Enter the person's name: ")
    birthday = input("Enter their birthday (MM-DD): ")
    phone = input("Enter their phone number: ")

    # Append to the CSV file
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, birthday, phone])

    print(f"🎉 Birthday for {name} added successfully!")

def main():
    while True:
        print("\n🎉 Birthday Reminder System 🎉")
        print("1. Check Today's Birthdays & Send SMS")
        print("2. Add a New Birthday")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            birthdays_today = check_birthdays()
            if not birthdays_today.empty:
                for _, row in birthdays_today.iterrows():
                    name = row["name"]
                    phone = row["phone"]
                    message = f"Reminder: Today is {name}'s birthday! 🎉"
                    
                    send_sms(MY_PHONE_NUMBER, message)  # Send a reminder to yourself
                    send_sms(phone, f"Happy Birthday, {name}! 🎂")  # Send to the birthday person

                print("Messages sent!")
            else:
                print("No birthdays today.")
        
        elif choice == "2":
            add_birthday()
        
        elif choice == "3":
            print("Exiting program. Goodbye! 👋")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
