import os
import shutil
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule
import locale

def get_all_files_in_directory(directory, extensions):
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in extensions):
                yield os.path.join(dirpath, filename)

def move_files(src, dest, start_date, end_date, extensions, language):
    try:
        locale.setlocale(locale.LC_TIME, language)
    except locale.Error:
        print(f"Locale '{language}' not supported. Defaulting to system's locale.")
        locale.setlocale(locale.LC_TIME, '')

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        files_to_move = []

        for file_path in get_all_files_in_directory(src, extensions):
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mod_time.year == dt.year and file_mod_time.month == dt.month:
                files_to_move.append(file_path)

        if files_to_move:
            month_folder_name = dt.strftime("%m-%B")  # Format: "MM-MonthName" in the specified language
            year_month_folder = os.path.join(dest, dt.strftime("%Y"), month_folder_name)

            if not os.path.exists(year_month_folder):
                os.makedirs(year_month_folder)

            for file_path in files_to_move:
                new_file_path = os.path.join(year_month_folder, os.path.basename(file_path))
                if not os.path.exists(new_file_path):  # Check if the file already exists in the destination
                    shutil.move(file_path, new_file_path)
                    print(f"Moved: {os.path.basename(file_path)} -> {new_file_path}")
                else:
                    print(f"Skipped (already exists): {new_file_path}")

def confirm_destination_path(dest, language):
    try:
        locale.setlocale(locale.LC_TIME, language)
    except locale.Error:
        print(f"Locale '{language}' not supported. Defaulting to system's locale.")
        locale.setlocale(locale.LC_TIME, '')

    random_year = random.randint(2000, 2030)
    random_month = random.randint(1, 12)
    random_date = datetime(random_year, random_month, 1)
    month_name = random_date.strftime("%B")
    example_path = os.path.join(dest, f"{random_year}\\{str(random_month).zfill(2)}-{month_name}")
    print(f"Example destination path: {example_path}")
    return input("Is this path correct? (yes/no): ").strip().lower() == 'yes'

def confirm_source_path(src):
    folders = next(os.walk(src))[1]
    files = next(os.walk(src))[2]
    if folders:
        print("First few folders under the source path:")
        print("\n".join(folders[:4]))
    elif files:
        print("First few files under the source path:")
        print("\n".join(files[:5]))
    else:
        print("No folders or files found under the source path.")
    return input("Is this path correct? (yes/no): ").strip().lower() == 'yes'

def main():
    src = input("Enter the source folder path: ")
    if not confirm_source_path(src):
        print("Exiting script. Please rerun with the correct source path.")
        return

    dest = input("Enter the destination folder path: ")

    # Set language for date formatting
    language = input("Enter the locale for month names (e.g., 'en_US', 'fr_FR'): ")
    if not confirm_destination_path(dest, language):
        print("Exiting script. Please rerun with the correct destination path.")
        return
    start = datetime.strptime(input("Enter the start month-year (MM/YYYY): "), "%m/%Y")
    end = datetime.strptime(input("Enter the end month-year (MM/YYYY): "), "%m/%Y")
    extensions = ['png', 'jpeg', 'jpg', 'mp4', 'mov', 'mp5','tif']

    move_files(src, dest, start, end, extensions, language)
    print("Files have been organized.")

if __name__ == "__main__":
    main()
