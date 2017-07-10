# using hash(#) to  put comments
from spy_details import spy, Spy, ChatMessage, friends        # Importing files containing detail of spy and its class,  friend
from steganography.steganography import Steganography        # Importing steganography library to hide secret message
from datetime import datetime                                # Importing date time
from termcolor import colored                                # Importing Term color to make text colorful...

#odl status messages which can be updated again
status_messages = ['Bingo' ,'Love is in the air','Solving mystery', 'Spy 007 on duty']
special = ['SOS','sos','help','HELP','save','SAVE']           #special words lists
print colored(".... Hello! Let's start your verification....","green")   #print statement to show this line on the very starting of app
#ask for an input whether user is old or a new user
question = colored("Do you want to continue as ",'blue') + colored(spy.salutation,'red') + " " + colored(spy.name,'red') + " (Y/N)? "
existing = raw_input(question)

#function for a new status input from user or it can be updating the old status
def add_status():

    updated_status_message = None

    if spy.current_status_message != None:
       print 'Your current status message is %s \n' % (spy.current_status_message)
    else:
        print colored("You don't have any status message currently \n",'red')

    default = raw_input(colored("Do you want to select from the older status (y/n)? ",'blue'))       #statement to know how user wants to update status

    if default.upper() == "N":                #if user choose to write a new status message
        new_status_message = raw_input(colored("Write the status message you want to set? ",'blue'))

        if len(new_status_message) > 0:                               # Check whether status input is empty or not....
            status_messages.append(new_status_message)                  #input new status will be added at the end of the status list with the help of append function
            updated_status_message = new_status_message

    elif default.upper() == 'Y':
        item_position = 1
        for message in status_messages:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1                             #status message index position will be increased by one after appending new status in tthe end

        message_selection = int(raw_input(colored("\nChoose from the above messages ",'green')))    # Selecting the status from older statuses...

        if len(status_messages) >= message_selection:
            updated_status_message = status_messages[message_selection - 1]  # Updating zero indexing

    else:
        print colored('The choice you have entered is invalid ! Please either press y or n :','red')

    if updated_status_message:                                             #print statement will use to print the status entered by the user
        print colored('Your updated status message is: %s','blue') % (updated_status_message)
    else:
        print colored("You current don't have a status update",'red')
    return updated_status_message

def add_friend():                                                           # add a friend function

    new_friend = Spy('','',0,0.0)                                           # initially age,rating will be zero

    new_friend.name = raw_input("Please add your friend's name: ",'green')   #input from the user regarding friend to be add
    new_friend.salutation = raw_input(colored("what would u like to call Mr. or Ms.?: ",'blue'))

    new_friend.name = new_friend.salutation + " " + new_friend.name

    new_friend.age = raw_input("Age?")
    new_friend.age = int(new_friend.age)                    # converting string into int data type

    new_friend.rating = raw_input("Spy rating?")
    new_friend.rating = float(new_friend.rating)           # converting string into float

    if len(new_friend.name) > 0 and new_friend.age > 19 and new_friend.rating >= 3:    #  set paramters to add a friend in list
        friends.append(new_friend)                                                     # Adding a friend using append function
        print colored('Your Friend Is Added!','green')
    else:
        print colored("Sorry! Invalid entry. Your Friend is Not Eligible to be a Spy",'red')

    return len(friends)                                                         # Return the total no. of friends in a list


def select_a_friend():                                                         # function to select a friend
    item_number = 0

    for friend in friends:
        print '%d. %s %s aged %d with rating %.2f is online' % (item_number +1, friend.salutation, friend.name, friend.age,friend.rating)
        item_number = item_number + 1

    friend_choice = raw_input(colored("Choose from your friends Lists",'blue'))

    friend_choice_position = int(friend_choice) - 1

    return friend_choice_position                                             # return the index position of friend selected


def send_message():                                                 # Here we defining the send_message function..which basically selects the friend & sending the secret message in form of text in a image..

    friend_choice = select_a_friend()

    original_image = raw_input(colored("Please Enter the name of the image?",'blue'))  # Name of the image in which u wanna to hide the text..
    output_path = "output.jpg"                                                         # Output path or name which is basically totally different from initial original image .and format changes here ..
    text = raw_input(colored("What's the secret message u wan't to Convey? ",'blue'))  # Secret text u wanna to hide in that image ..
    Steganography.encode(original_image, output_path, text)                            # Encoding the text in image via function..

    temp = text.split(' ')
    for i in special:
        if i in temp:
            temp[temp.index(i)] = colored('Please Help Me !! I Am in Danger..','red')  # Replacing special words with a special type of emergency message ...
    text = str.join(' ',temp)
    friends[friend_choice].chats_avg[0] = (friends[friend_choice].chats_avg[0] + len(temp))/(len(friends[friend_choice].chats)+1)
    new_chat = ChatMessage(text,True)

    friends[friend_choice].chats.append(new_chat)                                      # Appending the secret code in the chat list of that particular friend-->

    print colored("Your secret message in the image is ready!",'green')


def read_message():                               #function to read a secret chat

    sender = select_a_friend()

    output_path = raw_input(colored("Enter the name of the file In which secret Text is Hidden ?",'blue'))

    try:
        secret_text = Steganography.decode(output_path)
    except ValueError:
        print colored("NO message",'red')
        exit()

    secret_text = str(secret_text)
    if secret_text == 'None':
        print colored("No secret message is coded in the image!!",'red')         # error handling case if input secret text is none
    else:
        temp = secret_text.split(' ')
        for i in special:
            if i in temp:
                temp[temp.index(i)] = colored('Please Help Me,I am in Danger!!','red')
        secret_text = str.join(' ',temp)

        if len(secret_text)>100:                                                     # Handling special case where friend is annoying u by sending a long text message
            print colored("One of your friend is annoying you ,Do u Want to Delete him or her From your Friend lists.",'red')
            choice = raw_input(colored("If u want to Delete ur friend choose: 'Y' , If not choose: 'N' ",'blue'))

            if choice == "Y":
                del [sender]                              # That particular friend is deleted from the friend lists..
                print colored("Friend which is annoying you is deleted from the list",'green')
                print colored("Select your choices below.",'blue')
            else:
                print colored(secret_text,'blue')

        else:
            new_chat = ChatMessage(secret_text, False)

            friends[sender].chats.append(new_chat)

            print colored("Your secret message has been saved!",'green')


def read_chat_history():                          #read the older chat messages stored in chat lists..

    read_for = select_a_friend()                  # select particular friend's chat

    print '\n'

    for chat in friends[read_for].chats:
        time = chat.time.strftime("%A,%b %d %Y %H:%M:%S")    # Assigning the date and time parameter ..
        if chat.sent_by_me:
            print '[%s] %s: %s' % (colored(time,'blue'), colored('Sent By Me:','red'), chat.message)
        else:
            print '[%s] %s read: %s' % (colored(time,'blue'), colored(friends[read_for].name,'red'), chat.message)


def start_chat(spy):                              # Start the application by defining chat function..

    spy.name = spy.salutation + " " + spy.name


    if spy.age > 18 and spy.age < 50:           # Setting the validity parameter to be a spy..


        print colored("Authentication complete. Welcome ",'blue') + colored(spy.name,'red') + colored(" age ",'blue') \
              + str(spy.age) + colored(" and rating  ",'blue') + str(spy.rating) + colored(" Good To See you",'blue')

        show_menu = True                      # Showing the main menu to the user

        while show_menu:
            menu_choices = "What do you want to do? \n 1. Add a status update \n 2. Add a friend \n 3. Send a secret message \n 4. Read a secret message \n 5. Read Chats from a user \n 6. Close Application \n"  # Lists of things offered by spychat application..
            menu_choice = raw_input(colored(menu_choices,'green'))

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)

                if menu_choice == 1:            # 1 will give you different options for status ..
                    spy.current_status_message = add_status()
                elif menu_choice == 2:         # it will shown friends lists..
                    number_of_friends = add_friend()
                    print 'You have %d friends' % (number_of_friends)
                elif menu_choice == 3:
                    send_message()             # 3 for sending the message to a particular friend ..
                elif menu_choice == 4:
                    read_message()             # 4 for reading the chats of a particular friend ..
                elif menu_choice == 5:
                    read_chat_history()        # 5 for reading previous chats history
                else:
                    show_menu = False
    else:
        print colored('Sorry you are not of the correct age to be a spy','red')

if existing.upper() == "Y":
    start_chat(spy)
else:

    spy = Spy('','',0,0.0)


    spy.name = raw_input("...Welcome to spy chat, To Further proceed you must tell me your spy name first: ..")

    if len(spy.name) > 0:      # checking Validation of empty name ..
        spy.salutation = raw_input(colored("Should I call you Mr. or Ms.?: ",'blue'))

        spy.age = raw_input(colored("Enter your age?",'blue'))
        spy.age = int(spy.age)             # Converting Age of spy into int data type ..

        spy.rating = raw_input(colored("What is your spy rating?",'blue'))
        spy.rating = float(spy.rating)      # Converts the rating into float .bcz Raw_input returns string type .
        if spy.rating > 4.5:
            print 'Great ace!'
        elif spy.rating > 3.5 and spy.rating <= 4.5:
              print 'You are one of the good ones.'
        elif spy.rating >= 2.5 and spy.rating <= 3.5:
              print 'You can always do better'
        else:
              print 'We can always use somebody to help in the office.'
        start_chat(spy)
    else:
        print colored('You must have to enter a valid spy name','red')     # User Must have to fill valid name
        #end of coding