import os
import zipfile
from datetime import datetime
import numpy as np
from abc import ABC, abstractmethod


class AbstractFileManager(ABC):
    """Abstract class to define common file operations."""

    def __init__(self, directory):
        self.directory = directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    @abstractmethod
    def execute(self):
        pass


class UserAuthentication:
    """Class to handle user authentication (login and signup)."""

    def __init__(self):
        self.users_file = "users.txt"
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                pass

    def signup(self, username, password):
        with open(self.users_file, "r") as f:
            users = f.readlines()

        if any(username == user.split(",")[0] for user in users):
            print("Username already exists. Try logging in.")
            return False

        with open(self.users_file, "a") as f:
            f.write(f"{username},{password}\n")

        print("Signup successful! You can now log in.")
        return True

    def login(self, username, password):
        with open(self.users_file, "r") as f:
            users = f.readlines()

        for user in users:
            stored_username, stored_password = user.strip().split(",")
            if username == stored_username and password == stored_password:
                print("Login successful! Welcome.")
                return True

        print("Invalid credentials. Please try again or sign up.")
        return False


class BackupBuddy(AbstractFileManager):
    """Main BackupBuddy class extending AbstractFileManager."""

    def __init__(self, backup_dir):
        super().__init__(backup_dir)
        self.backups = []  # Store backup metadata (name, size, etc.)

    def create_backup(self, source_dir):
        if not os.path.exists(source_dir):
            print(f"Source directory '{source_dir}' does not exist.")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.zip"
            backup_path = os.path.join(self.directory, backup_name)

            with zipfile.ZipFile(backup_path, 'w') as backup_zip:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        backup_zip.write(file_path, arcname)

            backup_size = os.path.getsize(backup_path)
            self.backups.append({"name": backup_name, "size": backup_size, "timestamp": timestamp})

            print(f"Backup created successfully: {backup_path}")
        except Exception as e:
            print(f"An error occurred while creating the backup: {e}")

    def list_backups(self):
        if not self.backups:
            print("No backups found.")
            return

        print("Available backups:")
        for b in self.backups:
            print(f"- {b['name']} (Size: {b['size'] / 1024:.2f} KB, Timestamp: {b['timestamp']})")

    def restore_backup(self, backup_file, restore_dir):
        try:
            backup_path = os.path.join(self.directory, backup_file)
            if not os.path.exists(backup_path):
                print(f"Backup file '{backup_file}' does not exist.")
                return

            if not os.path.exists(restore_dir):
                os.makedirs(restore_dir)

            with zipfile.ZipFile(backup_path, 'r') as backup_zip:
                backup_zip.extractall(restore_dir)

            print(f"Backup '{backup_file}' restored successfully to '{restore_dir}'.")
        except Exception as e:
            print(f"An error occurred while restoring the backup: {e}")

    def delete_backup(self, backup_file):
        try:
            backup_path = os.path.join(self.directory, backup_file)
            if not os.path.exists(backup_path):
                print(f"Backup file '{backup_file}' does not exist.")
                return

            os.remove(backup_path)
            self.backups = [b for b in self.backups if b["name"] != backup_file]
            print(f"Backup '{backup_file}' deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting the backup: {e}")

    def analyze_backups(self):
        sizes = np.array([b["size"] for b in self.backups])
        if sizes.size == 0:
            print("No backups available for analysis.")
            return

        sorted_backups = sorted(self.backups, key=lambda b: b["size"])

        print("\n=== Backup Analysis ===")
        print(f"Total backups: {len(sizes)}")
        print(f"Total size: {sizes.sum() / 1024:.2f} KB")
        print(f"Average size: {sizes.mean() / 1024:.2f} KB")
        print(f"Largest backup: {sizes.max() / 1024:.2f} KB")
        print(f"Smallest backup: {sizes.min() / 1024:.2f} KB")

        print("\nSorted Backups (by size):")
        for b in sorted_backups:
            print(f"- {b['name']} (Size: {b['size'] / 1024:.2f} KB)")

    def execute(self):
        pass


# Main program
def main(input_func=input):
    auth = UserAuthentication()

    while True:
        print("\n=== Welcome to BackupBuddy ===")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input_func("Choose an option: ").strip()

        if choice == '1':
            username = input_func("Enter your username: ").strip()
            password = input_func("Enter your password: ").strip()
            if auth.login(username, password):
                break
        elif choice == '2':
            username = input_func("Enter a new username: ").strip()
            password = input_func("Enter a new password: ").strip()
            auth.signup(username, password)
        elif choice == '3':
            print("Exiting. Goodbye!")
            return
        else:
            print("Invalid choice. Try again.")

    bb = BackupBuddy("backups")

    while True:
        print("\n=== BackupBuddy Menu ===")
        print("1. Create Backup")
        print("2. List Backups")
        print("3. Restore Backup")
        print("4. Delete Backup")
        print("5. Analyze Backups")
        print("6. Logout")
        choice = input_func("Choose an option: ").strip()

        if choice == '1':
            source_dir = input_func("Enter the directory to back up: ").strip()
            bb.create_backup(source_dir)
        elif choice == '2':
            bb.list_backups()
        elif choice == '3':
            bb.list_backups()
            backup_file = input_func("Enter the backup file to restore: ").strip()
            restore_dir = input_func("Enter the directory to restore to: ").strip()
            bb.restore_backup(backup_file, restore_dir)
        elif choice == '4':
            bb.list_backups()
            backup_file = input_func("Enter the backup file to delete: ").strip()
            bb.delete_backup(backup_file)
        elif choice == '5':
            bb.analyze_backups()
        elif choice == '6':
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
