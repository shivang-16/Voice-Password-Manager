import json
import os

# File paths
SECURITY_KEY_FILE = 'security_key.json'
PASSWORDS_FILE = 'passwords.json'

def set_security_key():
    key = input("Set your Security Key: ")
    with open(SECURITY_KEY_FILE, 'w') as file:
        json.dump({'key': key}, file)
    print("Security Key has been set.")

def check_permission():
    if not os.path.exists(SECURITY_KEY_FILE):
        print("Security Key not set. Please set it first.")
        set_security_key()
        return False

    key = input("Enter Security Key: ")
    with open(SECURITY_KEY_FILE, 'r') as file:
        saved_key = json.load(file).get('key', None)

    if saved_key and saved_key == key:
        return True
    else:
        return False

def viewpassword():
    if check_permission():
        if not os.path.exists(PASSWORDS_FILE):
            print("No passwords stored yet.")
            open(PASSWORDS_FILE, 'w').close()
            return

        with open(PASSWORDS_FILE, 'r') as file:
            try:
                passwords = json.load(file)
            except json.JSONDecodeError:
                passwords = {}

        if not passwords:
            print("No passwords stored yet.")
        else:
            for account, password in passwords.items():
                print(f"Account: {account}, Password: {password}")
    else:
        print("Wrong Security Key")

def addpassword():
    account = input("Account name: ")
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, 'r') as file:
            try:
                passwords = json.load(file)
            except json.JSONDecodeError:
                passwords = {}
    else:
        passwords = {}

    if account in passwords:
        confirm = input(f"Account '{account}' already exists. Are you sure you want to overwrite the password? (yes/no): ").lower()
        if confirm != 'yes':
            print("Password not updated.")
            return

    password = input("Enter Password: ")
    passwords[account] = password

    with open(PASSWORDS_FILE, 'w') as file:
        json.dump(passwords, file)

    print(f"Password for account: {account} has been added/updated.")

if __name__ == "__main__":
    if not os.path.exists(SECURITY_KEY_FILE):
        set_security_key()

    while True:
        command = input('Type what you want to do: View/Add/Exit ').lower()

        if command == "view":
            viewpassword()
        elif command == "add":
            addpassword()
        elif command == "exit":
            print("Exiting the password manager.")
            break
        else:
            print("Invalid command")
