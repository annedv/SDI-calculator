## Author: Anne De Vreyer
## Date created: 15 September 2021
## Date last changed: 20 November 2021
## This program uses observation records of birds (species name and number of individuals) to:
## A - calculate Simpson's Diversity Index (SDI) and store records based on the user's input
## B - of two different locations, recommend the one with the highest SDI to go for a walk
## C - calculate SDIs for a set of five different locations
## The program generates a GUI with one root window and three other windows.
## It goes from one window to the other as needed to execute the user's chosen option.
## Input file: observation_records.txt
## Output file: diversity_index.txt


## LOADING THE LIBRARY FOR GUI
from tkinter import *


## DEFINING CONSTANT - to display index more accurately in a readable way
MULTIPLICATION_FACTOR = 1000

## DEFINING DATA STRUCTURES
menu_list = ["Enter records and calculate an index", "Compare two locations and get a recommendation for a walk",
             "Show all existing records and indices"]
locations_list = ["Black Mountain Nature Reserve", "Lake Ginninderra (John Knight Memorial Park)",
                  "University of Canberra", "Australian National University", "Australian National Botanic Gardens"]
index_dict = {}  # Stores location name and index as key : value pair.
all_records_list = []  # Stores unsorted records from observation_record.txt
records_species_list = []  # Stores species name (str)
records_count_list = []  # Stores bird count (int)

## DEFINING VARIABLES
location_name_str = ""
location1_str = ""
location2_str = ""
index_float = 0.0


## DEFINING FUNCTIONS AND PROCEDURES
# Reads observation records from text file and stores them in a list for use in options B & C.
def read_records():
    try:
        input_file = open("observation_records.txt", "r")
    except FileNotFoundError:  # If program could not find input file.
        outcome.set("Error: The file observation_records.txt doesn't exist or cannot be accessed by the program.")
    else:
        for line in input_file:
            all_records_list.append(line.strip("\n"))
        input_file.close()


# Creates records lists for one location, from all_records_list.
# Generates two lists stored in tuple: one with bird count (int), one with species name (str).
# Matching species and count are at same index in each list.
# Parameter is a string that is the location's name.
def split_records(a_string):
    records_list = []
    records_species_list = []
    records_count_list = []
    # Step 1: Create a list that starts at the location's name and stops at the last entered value for it.
    # In all_records_list, each location records start with location name and ends with an empty str.
    start_index = all_records_list.index(a_string)
    for item in all_records_list[start_index:]:
        if item != "":  # Empty str separate records for different locations.
            records_list.append(item)
        else:
            break
    # Step 2: Iterate over step 1's list to create a list of species names and a list of bird counts.
    for item in records_list:
        if item.isdigit():  # Digits are birds counts.
            item = int(item)
            records_count_list.append(item)
        elif item == a_string:  # Location's name is not appended.
            continue
        else:  # Other strings are species names.
            records_species_list.append(item)
    return records_count_list, records_species_list


# Calculates SDI from list of bird counts.
# Parameter is a list of integers.
def calculate_index(records_list):
    sum_records_int = 0
    total_birds_int = 0
    for bird_count_int in records_list:
        sum_records_int += (bird_count_int - 1) * bird_count_int
        total_birds_int += bird_count_int
    try:
        index_float = (1 - (sum_records_int / (total_birds_int * (total_birds_int - 1)))) * MULTIPLICATION_FACTOR
        return index_float
    except ZeroDivisionError:  # Erroneous records could lead to zero division.
        outcome.set("Error: The SDI could not be calculated. Check observation records include at least two species and no 0 count.")
        msg.set("Error: The SDI could not be calculated. Check observation records include at least two species and no 0 count.")
        message.set("Error: The SDI could not be calculated. Check observation records include at least two species and no 0 count.")


# Writes observations records and diversity index to a text file.
# Observations are displayed in a table style.
# Parameters: list of int (bird count), list of str (species), float (SDI), str (location name).
def write_observations(count_list, species_list, a_float, a_str):
    try:
        records_file = open("../diversity_index.txt", "a")
        records_file.write("\n\n" + "*" * 70)
        records_file.write(f"\nObservation records for {a_str}.")  # Title of table.
        records_file.write("\n" + "*" * 70)
        for i in range(0, len(species_list)):  # Table style. Matching species and count are at same index in each list.
            records_file.write(f"\n{species_list[i]}".ljust(40))
            records_file.write(f"{count_list[i]}".ljust(20))
        records_file.write(f"\n\nIn {a_str}, SDI = {a_float:.2f}.")  # SDI below the table.
        records_file.close()
    except PermissionError:  # If the program cannot write to output text file.
        outcome.set("Error: The program couldn't access and modify diversity_index.txt.")
        msg.set("Error: The program couldn't access and modify diversity_index.txt.")
        message.set("Error: The program couldn't access and modify diversity_index.txt.")
    except TypeError:  # If program has empty fields passed to it.
        outcome.set("Error: The SDI could not be calculated. Check observation records include at least two species and no 0 count.")
        msg.set("Error: The SDI could not be calculated. Check observation records include at least two species and no 0 count.")
        message.set("Error: The SDI could not be calculated. Check observation records include at least two species and no 0 count.")


# Calls all functions/procedures involved in calculating index and writing result to output file for a single location.
# For options B & C.
# Parameter is a string that is the location's name.
# Returns dict with {location name : SDI}. (Used to update index_dict in option B.)
def create_dict_index(a_string):
    a_tuple = split_records(a_string)  # Gets location's data from all_records_list (bird count and species name).
    index_float = calculate_index(a_tuple[0])  # Calculates SDI for location. a_tuple[0] is list of bird counts (int).
    write_observations(a_tuple[0], a_tuple[1], index_float, a_string)  # Writes location's records and SDI to diversity_index.txt.
    index_dict[a_string] = index_float  # Stores data (location name and SDI) in a dict for use in option B.


# Finds highest SDI (value) and corresponding location name (key) in dictionary, then writes and prints the recommendation.
# Called for option B.
def location_recommendation():
    try:
        recommended_place = max(index_dict, key=index_dict.get)  # Finds place with highest SDI.
        records_file = open("../diversity_index.txt", "a")  # Writes recommendation to output text file.
        records_file.write("\n" + "*" * 70)
        records_file.write(f"\nGo to {recommended_place} for your walk. SDI = {index_dict[recommended_place]:.2f}.")
        records_file.close()
        # Inform user of recommendation in GUI windows.
        message.set(f"Go to {recommended_place} for your walk. SDI = {index_dict[recommended_place]:.2f}.")
        outcome.set(f"Go to {recommended_place} for your walk.")
    except PermissionError:  # If the program cannot write to output text file.
        message.set("Error: The program couldn't access and modify diversity_index.txt.")
        outcome.set("Error: The program couldn't access and modify diversity_index.txt.")
    except ValueError:  # If records could not be read from input file.
        outcome.set(
            "Error: The SDI couldn't be calculated. Check that observations_records.txt is not empty or erroneous.")
        message.set(
            "Error: The SDI couldn't be calculated. Check that observations_records.txt is not empty or erroneous.")
    

# Gets back to root window (main menu) from other windows.
# Called when user clicks on "Back to main menu" button.
def back_to_main():
    # Withdraw all windows that could be open aside from root window.
    records_entry_window.withdraw()
    compare_window.withdraw()
    # Clear messages on outcome of previous operations (in options A or B).
    message.set("")  # In records_entry_window.
    msg.set("")  # In compare_window.
    # Bring main window back
    root_window.deiconify()


# Gets user's observation records from GUI. Called for option A.
# Called when user clicks "Save entry" button (records_entry_window).
# Validates input, stores species name in list of str and bird cound in list of int at same index.
# Assumes user will not enter negative numbers nor math equations.
def save_records():
    # Clear output field.
    msg.set("")
    try:
        # Get input from GUI.
        bird_count_num = eval(bird_count.get())
        species_str = species_name.get()
        # Validate input.
        1 / bird_count_num  # To check that user entered a number different from 0 (ZeroDivisionError).
        if species_str != "":  # Check that species field is not empty.
            if type(bird_count_num) is int:  # Check that bird count is a whole number (int).
                # Save records to lists.
                records_count_list.append(bird_count_num)  # List of int - bird count
                records_species_list.append(species_str)  # List of str - species name
                # Clear entry fields for next record entry.
                species_input.delete(0, END)
                count_input.delete(0, END)
            else:  # Tell user to type in whole number only.
                msg.set("Invalid input: You did not enter a whole number. Please enter an integer (digits only).")
        else:  # Tell user to enter a species name.
            msg.set("Invalid input: You did not enter a species name.")
    except SyntaxError:  # User did not enter anything, used leading 0s or entered letters/other characters.
        msg.set("Invalid input: Please enter an integer (digits only) for bird count.")
    except TypeError:  # User entered characters other than digits.
        msg.set("Invalid input: Please enter an integer (digits only) for bird count.")
    except NameError:  # User entered letters.
        msg.set("Invalid input: Please enter an integer (digits only) for bird count.")
    except ZeroDivisionError:  # User entered 0 (not a valid record).
        msg.set("Invalid input: You entered 0 for bird count. Number of observed birds must be 1 or greater.")


# Calls all functions/procedures involved in carrying out option A.
# Called when user clicks "Calculate SDI" button (records_entry_window).
# Calculates index and writes records & SDI to output file.
def carry_out_a():
    global records_species_list
    global records_count_list
    location_name_str = location_name.get()
    if location_name_str == "":  # Check that user entered location name.
        msg.set("Please enter the name of the location.")
    elif len(records_species_list) == 1:  # Calculating SDI for one species is useless (SDI = 0).
        msg.set("You entered records for only one species (SDI = 0). Enter at least two species.")
    else:
        try:
            # Create or clear text file.
            open("../diversity_index.txt", "w").close()
            # Calculate SDI, write SDI and records to output file.
            index_float = calculate_index(records_count_list)
            write_observations(records_count_list, records_species_list, index_float, location_name_str)
            # Inform user of outcome in GUI.
            outcome.set(f"SDI = {index_float:.2f} at {location_name_str}. Records are in diversity_index.txt.")
            msg.set(f"SDI = {index_float:.2f} at {location_name_str}. Records are in diversity_index.txt.")
            # Clear location name field.
            location_input.delete(0, END)
            # Clear data structures (in case user wants to enter new records).
            records_species_list = []
            records_count_list = []
        except PermissionError:  # If the program cannot open/create output text file.
            msg.set("Error: The program couldn't access or create diversity_index.txt.")
            outcome.set("Error: The program couldn't access or create diversity_index.txt.")
        except TypeError:  # If program has empty fields passed to it.
            outcome.set("Error: The SDI could not be calculated. Check observation records include at least two species and no 0 count.")
            msg.set("Error: The SDI could not be calculated. Check observation records include at least two species and no 0 count.")


# Calls all functions/procedures involved in carrying out option B.
# Called when user clicks "Calculate and compare SDI" button (compare_window).
# Gets user's selection from GUI, calculates and compares indices, gives a recommendation.
def carry_out_b():
    global index_dict
    # Clear dictionary.
    index_dict = {}
    try:
        # Create or clear text file.
        open("../diversity_index.txt", "w").close()
        # Calculate SDI for first location.
        first_location = location1_str.get()
        create_dict_index(first_location)
        # Calculate SDI for second location.
        second_location = location2_str.get()
        create_dict_index(second_location)
    except ValueError:  # If input file is empty or erroneous.
        outcome.set("Error: The SDI couldn't be calculated. Check that observations_records.txt is not empty or erroneous.")
        message.set("Error: The SDI couldn't be calculated. Check that observations_records.txt is not empty or erroneous.")
    except PermissionError:  # If the program cannot open/create output text file.
        message.set("Error: The program couldn't access or create diversity_index.txt.")
        outcome.set("Error: The program couldn't access or create diversity_index.txt.")
    # Compare indices and recommend one location.
    location_recommendation()

    
# Executes actions corresponding to user's choice in GUI main menu (root_window).
# Called when user clicks on one of three options in the listbox menu.
def menu_choice(event):
    read_records()
    option_picked = menu.get(menu.curselection())

    # Option A.
    if option_picked == "Enter records and calculate an index":
        # Clear output fields.
        outcome.set("")
        # Hide main menu window and bring window for records entry forward.
        root_window.withdraw()
        records_entry_window.deiconify()

    # Option B.
    if option_picked == "Compare two locations and get a recommendation for a walk":
        # Clear output fields.
        outcome.set("")
        # Hide main menu window and bring window for comparing and choosing forward.
        root_window.withdraw()
        compare_window.deiconify()

    # Option C.
    if option_picked == "Show all existing records and indices":
        try:
            # Create or clear text file and output field.
            outcome.set("")
            open("../diversity_index.txt", "w").close()
            # Calculate index and write to text file for each location.
            for location in locations_list:
                create_dict_index(location)
            # Inform user of outcome.
            outcome.set("Observation records and SDIs are now ready in diversity_index.txt.")
        except ValueError:  # If input file is empty or erroneous.
            outcome.set("Error: The SDI couldn't be calculated. Check that observations_records.txt is not empty or erroneous.")
        except PermissionError:  # If the program cannot open/create output text file.
            outcome.set("Error: The program couldn't access or create diversity_index.txt.")



## CREATE WINDOWS FOR GUI
# MAIN MENU WINDOW
root_window = Tk()
root_window.title("Index Calculator Menu")
root_window["bg"] = "light blue"

# Show menu_choice menu options.
question = Label(root_window, text="What would you like to do?", bg="light blue")
question.grid(row=0, column=0, pady=10)
choose_option = StringVar()
menu = Listbox(root_window, width=60, height=3, listvariable=choose_option)
menu.grid(row=1, column=0, padx=15, pady=10, rowspan=3)
choose_option.set(tuple(menu_list))
menu.bind("<<ListboxSelect>>", menu_choice)

# Field to display message informing user of program outcome.
outcome = StringVar()
outcome_msg = Entry(root_window, state="readonly", width=90, textvariable=outcome)
outcome_msg.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Exit button.
exit_button = Button(root_window, text="Exit program", command=exit)
exit_button.grid(row=5, column=0, columnspan=2, pady=10)



# WINDOW FOR OPTION A - USER INPUTS OBSERVATION RECORDS
records_entry_window = Toplevel(root_window)
records_entry_window.withdraw()  # Hidden until needed.
records_entry_window.title("Enter your own observation records.")
records_entry_window["bg"]="light blue"

# Label and Entry for location name.
enter_location = Label(records_entry_window, text="Location name:", bg="light blue")
enter_location.grid(row=0, column=0, pady=15)
location_name = StringVar()
location_input = Entry(records_entry_window, width=20, textvariable=location_name)
location_input.grid(row=0, column=1, pady=15)

# Entry for instructions on how to enter records.
instruction_txt = StringVar()
instruction = Entry(records_entry_window, width=90, state="readonly", textvariable=instruction_txt)
instruction.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
instruction_txt.set("To save a species count: click on \"Save entry\". You can then enter the next record for the next species.")

# Label and Entry for species name.
enter_species = Label(records_entry_window, text="Species name:", bg="light blue")
enter_species.grid(row=2, column=0, pady=5)
species_name = StringVar()
species_input = Entry(records_entry_window, width=20, textvariable=species_name)
species_input.grid(row=2, column=1, pady=5)

# Label and Entry for bird count.
enter_count = Label(records_entry_window, text="Bird count:", bg="light blue")
enter_count.grid(row=3, column=0, pady=5)
bird_count = StringVar()
count_input = Entry(records_entry_window, width=20, textvariable=bird_count)
count_input.grid(row=3, column=1, pady=5)

# Next entry button.
next_button = Button(records_entry_window, text="Save entry", command=save_records)
next_button.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

# Field to display message informing user of program outcome.
msg = StringVar()
done_msg = Entry(records_entry_window, width=90, state="readonly", textvariable=msg)
done_msg.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

# Calculate index button.
calculate_button = Button(records_entry_window, text="Calculate SDI", command=carry_out_a)
calculate_button.grid(row=5, column=0, pady=10)

# Back to main menu button.
done_button = Button(records_entry_window, text="Back to main menu", command=back_to_main)
done_button.grid(row=5, column=3, pady=10)



# WINDOW FOR OPTION B - USER SELECTS 2 LOCATIONS TO COMPARE
compare_window = Toplevel(root_window)
compare_window.withdraw()  # Hidden until needed.
compare_window.title("SDI comparison.")
compare_window["bg"]="light blue"

# Selecting locations through two dropdown submenus.
# Label for submenus.
prompt = Label(compare_window, text="Select locations to compare from the dropdown menus below:", bg="light blue")
prompt.grid(row=0, column=0, columnspan=4, pady=10)
# First submenu.
text1 = Label(compare_window, text="Compare", bg="light blue")
text1.grid(row=1, column=0)
location1_str = StringVar()
location1_str.set(locations_list[0])
submenu1 = OptionMenu(compare_window, location1_str, *locations_list)
submenu1.grid(row=1, column=1, pady=10)
# Second submenu.
text2 = Label(compare_window, text="to", bg="light blue")
text2.grid(row=1, column=2)
location2_str = StringVar()
location2_str.set(locations_list[0])
submenu2 = OptionMenu(compare_window, location2_str, *locations_list)
submenu2.grid(row=1, column=3, pady=10)

# Field to display recommendation in GUI.
message = StringVar()
outcome_msg = Entry(compare_window, state="readonly", width=90, textvariable=message)
outcome_msg.grid(row=2, column=0, columnspan=4, rowspan=2, pady=10, padx=5)

# Calculate and compare indices button.
compare_button = Button(compare_window, text="Calculate and compare SDI", command=carry_out_b)
compare_button.grid(row=4, column=0, columnspan=2, pady=10)

# Back to main menu button.
back_button = Button(compare_window, text="Back to main menu", command=back_to_main)
back_button.grid(row=4, column=2, columnspan=2, pady=10)


root_window.mainloop()
