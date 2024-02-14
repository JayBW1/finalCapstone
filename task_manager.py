# admin rights -> username: admin | password: password
#====import libraries====
import os
from datetime import datetime, date
DATETIME_STRING_FORMAT = "%Y-%m-%d"

#====login====
curr_user_list = []; log_list = []; username_password = {}
logged_in = False; log_list.append(logged_in)
def login():
    """Reads usernames and passwords from user.txt,
    allowing user to login.
    Writes default account if non exist"""
    if log_list[0] == False:
        if not os.path.exists("user.txt"):
            with open("user.txt", "w+") as default_file:
                default_file.write("admin;password")
        with open("user.txt", "r") as user_file:
            user_data = user_file.read().split("\n")
        for user in user_data:
            username, password = user.split(";")
            username_password[username] = password
        while not log_list[0]:
            print("-Login-")
            curr_user = input("Enter Username: ")
            if curr_user in username_password.keys():
                print("Valid Username")
            else:
                print("Invalid Username"); continue
            curr_pass = input("Enter Password: ")
            if username_password[curr_user] == curr_pass:
                print("Valid Password\nSuccessfully Logged In\n")
                curr_user_list.append(curr_user)
                log_list[0] = True
            else:
                print("Invalid Password"); continue
    # else: # already logged in
        """count users and returns number"""
    registered_user_list = []
    # read user.txt and append users to list
    with open("user.txt", "r")as out_file:
        read_out_file = out_file.readlines()
        user = dict(line.split(";") for line in read_out_file)
        registered_user_list.append(user.keys())
    return len(registered_user_list)

#====reports====
task_overview_value = []; user_overview_value = []
def report():
    """- if task overview and user overview exist,
    read both files, find numbers in file, append number to list and 
    assign list index to variable
    - else create new files with starting count
    - update the variables when a user adds or completes tasks"""
    replace_list = []
    # task overview
    if os.path.exists("task_overview.txt"):
        with open("task_overview.txt", "r") as task_overview:
            task_overview.seek(0, 0) # use file to update vars
            task_overview_read = task_overview.readlines()
            for line in task_overview_read:
                line_search = line.split(" ")
                for number in line_search:
                    if number.isnumeric():
                        task_overview_value.append(int(number))
            task_overview_value.append(0)
            # math vars
            task_overview_value[2] = (
                task_overview_value[0] - task_overview_value[1])
            # zero div
            try:
                task_overview_value[6] = (
                (task_overview_value[1] / task_overview_value[0]) * 100)
                task_overview_value[5] = (
                (task_overview_value[3] / task_overview_value[0]) * 100)
            except ZeroDivisionError:
                task_overview_value[6] = 0; task_overview_value[5] = 0
            if task_overview_value[0] == 0:
                task_overview_value[4] = 0
            else:
                task_overview_value[4] = 100 - task_overview_value[6]
    else: # if file does not exist, write starting count to new file
        for i in range(6):
            task_overview_value.append(0)
    # format data and write to file
    with open("task_overview.txt", "w+") as task_overview:
        task_overview.write(f"Task Overview:\n\
Number Of Tasks Generated:\t\t {task_overview_value[0]} \n\
Number Of Completed Tasks:\t\t {task_overview_value[1]} \n\
Number Of Incomplete Tasks:\t\t {task_overview_value[2]} \n\
Number Of Tasks Overdue:\t\t {task_overview_value[3]} \n\
Percentage Of Tasks Incomplete:\t\t {round(task_overview_value[4])} % \n\
Percentage Of Tasks Overdue:\t\t {round(task_overview_value[5])} %")
    # individual user overview
    if os.path.exists(f"{curr_user_list[0]}_overview.txt"):
        with open(f"{curr_user_list[0]}_overview.txt", "r") as user_overview:
            user_overview.seek(0, 0) # use file to update vars
            user_overview_read = user_overview.readlines()
            user_overview.seek(0, 0); user_read_str = user_overview.read()
            replace_list.append(user_read_str)
            for line in user_overview_read:
                line_search = str(line).split(" ")
                for number in line_search:
                    if number.isnumeric():
                        user_overview_value.append(int(number))
            try:
                user_overview_value.append(
                (user_overview_value[0] * 100) / user_overview_value[2])
            except ZeroDivisionError:
                user_overview_value.append(0)
            # math vars
            user_incomplete_task_count = (
                user_overview_value[0] - user_overview_value[5])

            user_overdue_task_count = (
                (user_overview_value[4] / 100) * user_overview_value[0])
            user_overview_value.append(round(user_overdue_task_count))
            user_overdue_task_count = int(user_overview_value[6])
            # zero div
            try:
                user_overview_value[1] = (
                (user_overview_value[0] / task_overview_value[0]) * 100)
                user_overview_value[2] = (
                (user_overview_value[5] / user_overview_value[0]) * 100)
                user_overview_value[3] = (
                (user_incomplete_task_count / user_overview_value[0]) * 100)
                user_overview_value[4] = (
                (round(user_overdue_task_count) / user_overview_value[0]) * 100)
            except ZeroDivisionError:
                user_overview_value[1] = 0; user_overview_value[2] = 0
                user_overview_value[3] = 0; user_overview_value[4] = 0
    else: # if file does not exist, write starting count to new file
        for i in range(6):
            user_overview_value.append(0)
    # format data and write to file
    data = (f"{curr_user_list[0]} Overview:\n\
Number Of User Assigned Tasks:\t\t\t {user_overview_value[0]} \n\
Percentage Of Total Tasks Assigned To User:\t\
 {round(user_overview_value[1])} %\n\
Percentage Of Completed Tasks For User:\t\t\
 {round(user_overview_value[2])} %\n\
Percentage Of Incomplete Tasks For User:\t\
 {round(user_overview_value[3])} %\n\
Percentage Of Overdue Tasks For User:\t\t\
 {round(user_overview_value[4])} %")
    start_data = f"User Overview:\n\
Number Of Registered Users:\t\t {login()} \n\
Number Of Tasks Generated:\t\t {task_overview_value[0]}"
    with open(f"{curr_user_list[0]}_overview.txt", "w+") as user_overview:
        user_overview.write(data)
    # all user overview
    if replace_list != []:
        old_data = str(replace_list[0])
    else:
        old_data = []
    if os.path.exists("user_overview.txt"):
        with open("user_overview.txt", "r") as all_overview:
            all_overview.seek(0, 0); read_all = all_overview.read()
            old_start = read_all.split("\n")[0 : 3]
            old_start = "\n".join(old_start)
            if old_data in read_all:
                with open("user_overview.txt", "w") as all_overview:
                    read_all = read_all.replace(old_data, data)
                    read_all = read_all.replace(old_start, start_data)
                    all_overview.write(read_all)
            else:
                with open("user_overview.txt", "a") as all_overview:
                    all_overview.write(f"\n\n{data}")
    else:
        with open("user_overview.txt", "w+") as all_overview:
            all_overview.write(f"{start_data}\n\n{data}")
    """read overview documents and print to terminal"""
    report_str = ""
    report_str = "\n-Reports Generated-\n\n"
    with open("task_overview.txt", "r") as task_overview :
        report_str += f"{task_overview.read()}\n\n"
        
    with open(f"user_overview.txt", "r") as all_user_overview:
        report_str += f"{all_user_overview.read()}\n"
    return report_str
        
#====tasks====
task_list = []
def edit_task(old_task: list, chosen: list):
    write_list = []
    with open("tasks.txt", "r") as task_file:
        task_lines = task_file.readlines()
    old_task[5] = "No"
    old_task = str(old_task).replace("[", "")
    old_task = str(old_task).replace("]", "")
    old_task = str(old_task).replace("'", "")
    old_task = str(old_task).replace(", ", ";")
    chosen = str(chosen).replace("[", "")
    chosen = str(chosen).replace("]", "")
    chosen = str(chosen).replace("'", "")
    chosen = str(chosen).replace(", ", ";")
    with open("tasks.txt", "w") as task_file:
        for line in task_lines:
            line = line.replace("\n", "")
            if line == old_task: # previous version of edited task
                write_list.append(str(chosen))
            else:
                write_list.append(line)
        task_file.write("\n".join(write_list))

def write_task_list():
    """update task list when it is edited"""
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as task_file:
            pass
    """Reads tasks.txt data and formats accordingly"""
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]
    for t_str in task_data:
        curr_t = {}
        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = task_components[3]
        curr_t['assigned_date'] = task_components[4]
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)
        due_date = datetime.strptime(curr_t['due_date'], \
            DATETIME_STRING_FORMAT)
        # check date, add +1 to overdue task count if before current date
        if due_date < datetime.today() and task_components[5] == "No":
            task_overview_value[2] += 1 # overdue task count + 1
            if task_components[0] == curr_user_list[0]:
                user_overview_value[6] += 1 # user task overdue count + 1

def view_mine(list: list, int: int) -> str:
    """Reads the task from tasks.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling).
    [VM] - User can then select a task to edit or mark as complete"""
    disp_str = ""
    if list == []: # check for tasks
        disp_str = "No Tasks Available\n"
    else:
        for i, t in enumerate(list, int):
            if t['username'] == curr_user_list[0]:
                disp_str += f"Task [{i}]:\t\t{t['title']}\n"
                disp_str += f"Assigned to:\t\t{t['username']}\n"
                disp_str += f"Date Assigned:\t\t{t['assigned_date']}\n"
                disp_str += f"Due Date:\t\t{t['due_date']}\n"
                disp_str += f"Completed?\t\t\
{'Yes' if t['completed'] else 'No'}\n"
                disp_str += f"Task Description:\n {t['description']}\n\n"
            else:
                disp_str = "No Tasks Available\n"
    return disp_str

def view_all(list: list) -> str:
    disp_str = "" 
    if task_list == []: # check for tasks
        disp_str = "No Tasks Available\n"
    else:
        for i, t in enumerate(list, 1):
            disp_str += f"Task [{i}]:\t\t{t['title']}\n"
            disp_str += f"Assigned to:\t\t{t['username']}\n"
            disp_str += f"Date Assigned:\t\t{t['assigned_date']}\n"
            disp_str += f"Due Date:\t\t{t['due_date']}\n"
            disp_str += f"Completed?\t\t\
{'Yes' if t['completed'] else 'No'}\n"
            disp_str += f"Task Description:\n {t['description']}\n\n"
    return disp_str

def add_task():
    """Allow a user to add a new task to tasks.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task"""
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time.strftime(DATETIME_STRING_FORMAT),
        "assigned_date": curr_date.strftime(DATETIME_STRING_FORMAT),
        "completed": False
        }
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'],
                t['assigned_date'],
                'Yes' if t['completed'] else 'No'
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
        report()
        task_overview_value[0] += 1 # task count + 1
        user_overview_value[0] += 1 # user task count + 1

#====register user====
def reg_user():
    """Add a new user to the user.txt file"""
    username_password[new_username] = new_password
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_password:
            user_data.append(f"{k};{username_password[k]}")
        out_file.write("\n".join(user_data))
# - Otherwise you present a relevant message.

#====main loop====
while True:
    login(); task_list = []; write_task_list() 
    menu = input('''Select One Of The Following Options Below:
[R]\t- Registering A User
[A]\t- Adding A Task
[VA]\t- View All Tasks
[VM]\t- View My Task
[GR]\t- Generate Reports
[DS]\t- Display Statistics
[LO]\t- Log Out
[E]\t- Exit
: ''').lower()

    if menu == 'r':
        # - Request input of a new username
        invalid = False; current_entry = "username"
        registered = False
        while not registered:
            if current_entry == "username":
                new_username = input("New Username: ")
                # check if username already exists
                if new_username in username_password.keys():
                    print("Username Already In Use\n"); continue
                else:
                    print("Valid Username\n"); current_entry = "password"
            elif current_entry == "password":
                new_password = input("New Password: ")
                confirm_password = input("Confirm Password: ")
                if new_password == confirm_password:
                    print("New User Added\n"); reg_user(); registered = True
                else:
                    print("Passwords Do Not Match\n")

    elif menu == 'a':
        added_task = False; current_entry = "task_username"
        while not added_task:
            curr_date = date.today()
            if current_entry == "task_username":
                task_username = input("\nUsername Assigned To Task: ")
                if task_username not in username_password.keys():
                    print("User Does Not Exist. Please Enter Valid Username")
                    continue
                else:
                    current_entry = "task_title"
                    
            elif current_entry == "task_title":
                task_title = input("Title Of Task: ")
                current_entry = "task_description"
                
            elif current_entry == "task_description":
                task_description = input("Description Of Task: ")
                current_entry = "task_due_date"
                
            elif current_entry == "task_due_date":
                try:
                    task_due_date = input("Due Date Of Task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(
                        task_due_date, DATETIME_STRING_FORMAT)
                    current_entry = "done"
                except ValueError:
                    print("Invalid Datetime Format")
            elif current_entry == "done":
                added_task = True; add_task()
                print("Task Successfully Added.\n")

    elif menu == 'va':
        print(f"\nTask List:\n\n{view_all(task_list)}")

    elif menu == 'vm':
        done = False
        print(f"\nMy Task List:\n\n{view_mine(task_list, 1)}")
        if view_mine(task_list, 1) != "No Tasks Available\n":
            current_entry = "select_task"
            while not done:
                if current_entry == "select_task":
                    vm_menu = input("[-1] Main Menu\nEnter Task Number: ")
                    n = 1
                    for i in enumerate(task_list, 1):
                        n += 1
                    if vm_menu == "-1":
                        print("Back To Main Menu\n"); done = True
                    if vm_menu.isnumeric():
                        if int(vm_menu) in range(1, n):
                            vm_list = []
                            vm_list.append(vm_menu)
                            current_entry = "edit_task"
                        else:
                            print("\nInvalid Index")
                    else:
                        print("\nInvalid Index")

                elif current_entry == "edit_task":
                    write_task_list()
                    chosen = task_list.copy()
                    chosen = chosen[int(vm_list[0]) - 1]
                    chosen = dict(chosen)
                    chosen = chosen.values()
                    chosen = list(chosen)
                    old_task = chosen.copy()
                    vm_menu2 = input(
                        "\n[-1] Main Menu\n[1] Mark As Completed\n\
[2] Edit Assigned User\n[3] Edit Task Due Date\n\
Enter Selection: ")
                    if vm_menu2 == "-1":
                        print("Back To Main Menu\n"); done = True
                    if chosen[5] == False:
                        if vm_menu2 == "1":
                            chosen[5] = "Yes"
                            edit_task(old_task, chosen)
                            user_overview_value[5] += 1 # user completed + 1
                            task_overview_value[1] += 1 # task completed + 1
                            report()
                            print(f"Task [{vm_menu}] Marked As Completed\n")
                            done = True
                            
                        elif vm_menu2 == "2":
                            edit = input("Enter Assigned User: ")
                            if edit in username_password.keys():
                                chosen[0] = edit
                                print("Task Assigned User Changed\n")
                                edit_task(old_task, chosen)
                            else:
                                print("User Does Not Exist")
                                
                        elif vm_menu2 == "3":
                            edit = input("\nEnter Due Date (YYYY-MM-DD): ")
                            try:
                                edit == datetime.strptime(
                                    edit, DATETIME_STRING_FORMAT)
                                chosen[3] = edit
                                print("Task Due Date Changed\n")
                                edit_task(old_task, chosen)
                            except ValueError:
                                print("Invalid Date Format")
                    else:
                        print("Completed Tasks Cannot Be Edited\n")
    elif menu == 'gr':
        print(report())

    elif menu == 'ds' and curr_user_list[0] == 'admin':
        # If user is admin, display statistics 
        # about number of users and tasks
        print(f"-----------------------------------")
        print(f"Number Of Users: \t\t {login()}")
        print(f"Number Of Tasks: \t\t {task_overview_value[0]}")
        print("-----------------------------------")

    elif menu == "lo":
        print("Logged Out\n")
        log_list[0] = False; curr_user_list = []

    elif menu == 'e':
        print('Goodbye!!!'); exit()

    else: print("You Have Made A Wrong Choice, Please Try Again\n")