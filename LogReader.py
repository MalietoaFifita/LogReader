#Function that executes on every line in the log, to build the dictionary object for that line, to return the valid_lines dictionary object
def read_log(line):
    #strip white space, basically remove all extra spaces in the line
    #if the line become empty, return None
    log_line = line.strip()
    if not log_line:
        return None

    #extract Timestamp, the first 19 characters
    #extract the rest of the line
    timestamp = log_line[:19]

    #split the rest of the line
    rest = log_line[21:].split()

    #defensive check to make sure line has at least two words
    if len(rest) < 2:
        return None
    #extract the first word after the comma --> severity, assign to a variable
    severity = rest[0]

    #extract system, second word after the comma
    #assign system to a variable
    system = rest[1]

    #everything after system --> extract as the message, assign to a variable
    message = " ".join(rest[2:])

    #Build the dictionary for this line
    log_line_dict = {
        "timestamp": timestamp , 
        "severity": severity , 
        "system": system , 
        "message": message
    }
    #return the dictionary
    return log_line_dict

#Function that will read the file, build the list to return the lists to the main loop
def load_file():
    valid_lines = []
    malformed_lines = []
    #ask user for file path
    while True:
        try:
            print("Enter the full file path of the log file you would like to read.")
            log_path = input("Enter Here: ")
            print()
            #try to open the file
            with open(log_path) as file:
                #loop through each line
                for line_number , line in enumerate(file, start= 1):
                    #call read_log()
                    result = read_log(line)
                    #why does this if not section work again?
                    if not result:
                        malformed_lines.append({
                            "line_number": line_number , 
                            "raw": line
                        })
                    #otherwise append the result to the valid_lines list object
                    else:
                        valid_lines.append(result)
            #return both lists to the main loop
            return valid_lines, malformed_lines
        except FileNotFoundError:
            print("Sorry, that is not a valid file path.")
            continue
    
#Function that will search the finished list of log dictionary objects, make a new list of the matching dictionary objects, and return the matching results to the submenu function
def search_logs(criteria, value):
    #make a list named matches
    matches = []

    #loop through each item in valid_lines
    for item in valid_lines:
        #If criteria is system:
        if criteria == "system":
            #check if system matches the value
            if item["system"].lower() == value.lower():
                matches.append(item)

        #if criteria is keyword:
        elif criteria == "keyword":
            #check if keyword matches the value
            if value.lower() in item["message"].lower():
                matches.append(item)

        #if criteria is timestamp:
        elif criteria == "timestamp":
            #check if timestamp matches the value
            if item["timestamp"].startswith(value):
                matches.append(item)
    return matches

#2 lists
valid_lines , malformed_lines = load_file()
#CLI Menu
while True: 

    print("Welcome to the LogReader Application")
    print("Choose the log action below:")
    print("1. Display an amount of valid log lines")
    print("2. Display an amount of malformed log lines")
    print("3. Search logs (System, keyword, timestamp)")
    print("4. Count severity levels")
    print("5. Quit")
    print()
    
    #input validation loop
    while True:
        try:
            log_action = int(input("Enter action here: "))
            if 1 <= log_action <= 5:
                break
            else: 
                print("Numbers only please")
                continue
        except:
            print("numbers 1-5 please")
    
    print()

#Display user choice of logs
    if log_action == 1:
        #Check if valid_lines is empty:
        if not valid_lines:
            print("No valid lines to display.")
            print()
            pass

        #ask user for the amount of logs to display
        #validation loop
            #check for numbers
            #check for length, can't be less than 0 or more than the list length
        while True:
            try:
                #let user know how many logs are in the list
                print(f"There are {len(valid_lines)} total log(s)")
                logs_displayed = int(input("How many valid logs would you like to display?: "))
                if 1 <= logs_displayed <= len(valid_lines):
                    break
                else:
                    print("Sorry that is not a valid number")
                    print()
            except: 
                print("Sorry that is not a valid number")
                print()
                continue

        #after confirming working input, loop through list n amount of times
        #print example

        for entry_number , item in enumerate(valid_lines[:logs_displayed], start= 1):
            print()
            print(f"Entry {entry_number}:")
            print(f"Timestamp: {item['timestamp']}")
            print(f"Severity: {item['severity']}")
            print(f"System: {item['system']}")
            print(f"Message: {item['message']}")
            print()

#Display user choice of malformed logs
    elif log_action == 2:
        #check if malformed_lines is empty
        if not malformed_lines:
            print("No malformed lines to display.")
            print()
            pass


        #ask user for the amount of logs to display
        #validation loop
            #check for numbers
            #check for length, can't be less than 0 or more than the list length
        while True:
            try:
                #Let user know how many logs are in the list
                print(f"There are {len(malformed_lines)} total log(s)")
                logs_displayed = int(input("How many malformed logs would you like to display?: "))
                if 1 <= logs_displayed <= len(malformed_lines):
                    break
                else:
                    print("Sorry that is not a valid number")
                    print()
            except: 
                print("Sorry that is not a valid number")
                print()
                continue

        #after confirming working input, loop through list n amount of times
        #print example

        for entry_number , item in enumerate(malformed_lines[:logs_displayed], start= 1):
            print()
            print(f"Malformed Entry {entry_number}:")
            print(f"Line Number in original file: {item['line_number']}")
            print(f"Raw Line Data: {item['raw']}")
            print()

#Search logs sub menu:
    elif log_action == 3:
        while True:
            try:
                print("1. System")
                print("2. Keyword")
                print("3. Timestamp")
                print("4. Return to Main Menu")
                print()
                submenu_action = int(input("Enter Choice Here: "))
                print()
                if 1 <= submenu_action <= 4:
                    break
                else:
                    print("Sorry, enter a number between 1-4")
                    print()
            except:
                print("Sorry, enter a number between 1-4")
                print()
                continue

        if submenu_action == 1:
            #validation loop check
            while True:
                try:
                    #ask user for system name and call search_logs function
                    system_name = input("Enter the system name you would like to search for:")
                    results = search_logs("system", system_name)
                    break
                except:
                    print("Sorry, there was an error searching for the system name.")
                    print()
                    continue

            #check if nothing was returned, if nothing is returned. Go back to CLI menu
            if len(results) == 0:
                print("Sorry, there are no results containing that system")
                print()
                continue

            #print to show user how many matches, ask user how many they want to see and print for them.
            print(f"There are {len(results)} total entries matching that system name.")

            #validation loop for user input
            while True:
                try:
                    results_displayed = int(input("How many entries would you like to display?"))
                    if 1 <= results_displayed <= len(results):
                        break
                    else:
                        print("Sorry that is not a valid number")
                        continue
                except:
                    print("Sorry, that is not a valid number")
                    continue


            for result_number, item in enumerate(results[:results_displayed], start= 1):
                print()
                print(f"Entry {result_number}:")
                print(f"Timestamp: {item['timestamp']}")
                print(f"Severity: {item['severity']}")
                print(f"System: {item['system']}")
                print(f"Message: {item['message']}")
                print()

        elif submenu_action == 2:
            #validation loop check
            while True:
                try:
                    #ask user for keyword and call search_logs function
                    keyword = input("What keyword would you like to search for?: ")
                    results = search_logs("keyword", keyword)
                    break
                except:
                    print("Sorry, there was an error with the search")

            #check if nothing was returned, if nothing is returned. Go back to CLI menu
            if len(results) == 0:
                print("Sorry, there are no results containing that keyword")
                print()
                continue

            #print to show user how many matches, ask user how many they want to see and print for them.
            print(f"There are {len(results)} total entries matching that keyword.")
            #validation loop, for user input
            while True:
                try:
                    results_displayed = int(input("How many would you like to display?: "))
                    if 1 <= results_displayed <= len(results):
                        break
                    else:
                        print("Sorry not a valid number")
                        continue
                except:
                    print("Sorry not a valid number")
                    continue

            for result_number, item in enumerate(results[:results_displayed], start= 1):
                print()
                print(f"Entry {result_number}:")
                print(f"Timestamp: {item['timestamp']}")
                print(f"Severity: {item['severity']}")
                print(f"System: {item['system']}")
                print(f"Message: {item['message']}")
                print()

        elif submenu_action == 3:
            #validation loop check
            while True:
                try:
                    #ask user for timestamp, and give user format. call search_logs function
                    print("Enter the timestamp as either YYYY-MM-DD or YYYY-MM-DD HH:MM:SS")
                    timestamp_input = input("Enter the timestamp here: ")
                    print()
                    results = search_logs("timestamp", timestamp_input)
                    break
                except:
                    print("Sorry, there was an error with your search")

            #check if nothing was returned, if nothing is returned. Go back to sub-menu
            if len(results) == 0:
                print("Sorry, there are no results containing that timestamp")
                print()
                continue

            #print to show user how many matches
            print(f"There are {len(results)} total entries matching that timestamp.")
            #ask user how many they want to see and print for them.
            #validation loop for user input
            while True:
                try:
                    results_displayed = int(input("How many entries would you like to display?: "))
                    if 1 <= results_displayed <= len(results):
                        break
                    else:
                        print("Sorry that is not a valid number")
                        continue
                except:
                    print("Sorry that is not a valid number")
                    continue
            
            for entry_number, item in enumerate(results[:results_displayed], start= 1):
                print()
                print(f"Entry {entry_number}:")
                print(f"Timestamp: {item['timestamp']}")
                print(f"Severity: {item['severity']}")
                print(f"System: {item['system']}")
                print(f"Message: {item['message']}")
                print()

#Count severity levels?
    elif log_action == 4:
        info_count = 0
        warning_count = 0
        error_count = 0
        unknown_count = 0
        for item in valid_lines:
            if item["severity"].lower() == "info":
                info_count += 1
            elif item["severity"].lower() == "warning":
                warning_count += 1
            elif item["severity"].lower() == "error":
                error_count += 1
            else:
                unknown_count += 1
        
        print("Severity Statics")
        print(f"Info logs: {info_count}")
        print(f"Warning logs: {warning_count}")
        print(f"Error logs: {error_count}")
        print(f"Unknown Logs: {unknown_count}")
        print()


#Quit
    else:
        print("Thank you for using the LogReader Application!")
        break
