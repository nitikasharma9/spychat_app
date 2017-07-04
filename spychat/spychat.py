from spy_details import spy, Spy, ChatMessage, friends
from steganography.steganography import Steganography
from datetime import datetime
from termcolor import colored

#older status message which can be updated
status_messages= [colored('Hello everyone','blue') ,colored('Finally onboard','blue'),colored('Solving the cases','blue'),colored('spy is available','blue')]
special = ['SOS','sos','help','HELP','save','SAVE']

#starting of spy chat app
#to continue with old account or create a new one
question = "Do you want to continue as " + colored(spy.salutation,'blue') + " " + colored(spy.name,'blue') + " (Y/N)? "
existing = raw_input(question)

def add_status():
    updated_status_message = None
#if status message update is not null
    if spy.current_status_message != None:

        print 'Your current status message is %s \n' % (spy.current_status_message)
    else:    #if spy dont have any status
        print colored("You don't have any status message currently !!!\n",'red')
    #if user wants to update old status
    default = raw_input("Do you want to select from the older status (y/n)? ")
   #if user wants to update new status
    if default.upper() == "N":
        new_status_message = raw_input("Write the status message do you want to set? ")

        #new message will be append or added at the end
        if len(new_status_message) > 0:
            status_messages.append(new_status_message)
            updated_status_message = new_status_message
    #if user wants to update old status
    elif default.upper() == 'Y':

        item_position = 1
        for message in status_messages:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1
        #code to select a status from older ones
        message_selection = int(raw_input(colored("\nChoose from the above messages ",'green')))

        #choose right status with the help if indexing
        if len(status_messages) >= message_selection:
            updated_status_message = status_messages[message_selection - 1]

    else:        #if user input wrong word
        print colored('The choice you Entered is not valid! Press either y or n .','red')

    if updated_status_message:
        print colored('Your updated status message is: %s','blue') % (updated_status_message)
    else:
        print colored("You current don't have a status update",'red')
    return updated_status_message
#function to add a new friend in a list
def add_friend():

    new_friend = Spy('','',0,0.0)
    #inputs will be taken from user
    new_friend.name = raw_input(colored("Please add your friend's name: ",'blue'))
    new_friend.salutation = raw_input(colored("what would u like to call Mr. or Ms.?: ",'blue'))
    new_friend.name = new_friend.salutation + " " + new_friend.name
    new_friend.age = raw_input("Age?")
    new_friend.age = int(new_friend.age)
    new_friend.rating = raw_input("Spy rating?")
    new_friend.rating = float(new_friend.rating)
    #if the entries like name , age and rating is correct
    if len(new_friend.name) > 0 and new_friend.age > 19 and new_friend.rating >= 4:
        friends.append(new_friend)
        print colored('Your Friend Is Added!','green')
    else:  #if above entries are invalid
        print colored("Sorry! Invalid entry. Your Friend is Not Eligible to be a Spy",'red')

    return len(friends)

def select_a_friend():
    item_number = 0
    #to slelect a friend to whom user send a message
    for friend in friends:
        print '%d. %s %s aged %d with rating %.2f is online' % (item_number +1, friend.salutation, friend.name, friend.age,friend.rating)
        item_number = item_number + 1
    #give user a choice to select its friend from the list
    friend_choice = raw_input(colored("Choose from your friends Lists",'blue'))
    friend_choice_position = int(friend_choice) - 1

    return friend_choice_position
#function  on how we can send  a message to the selected friend
def send_message():

    friend_choice = select_a_friend()
    #steganography will be used by uploading an png file
    original_image = raw_input(colored("Please Enter the name of the image?",'blue'))
    output_path = "output.jpg"
    text = raw_input(colored("What's the secret message u want to Convey? ",'blue'))
    Steganography.encode(original_image, output_path, text)

    new_chat = ChatMessage(text,True)

    friends[friend_choice].chats.append(new_chat)
    print colored("Your secret message in the image is ready!",'green')
#function how other can read a secret message
def read_message():
    #selecting a file from which we can read secret text
    sender = select_a_friend()
    output_path = raw_input(colored("Enter the name of the file in which secret Text is Hidden ?",'blue'))
    secret_text = Steganography.decode(output_path)
    secret_text = str(secret_text)
    #case if no secret text is hidden in the photo
    if secret_text == 'None':
        print colored("No secret message is coded in the image!!",'red')
    else:
        temp = secret_text.split(' ')
        for i in special:
            if i in temp:
                temp[temp.index(i)] = colored('Please Help me Spy,I am in Danger . Save me!!','red')
        if len(secret_text)>100:    #if friend send too big message..way to delete it from friend list
            question =raw_input("This friend is annoying you , do you want to delete it from friend list - Y or N :")
            if question== 'y':
                del[sender];
                print colored('The sender is deleted from your friend list','green')
            print colored("The friend which is annoying you is deleted from friend list ",'green')

        else:   #new chat will be added after the older chat
            new_chat = ChatMessage(secret_text, False)
            friends[sender].chats.append(new_chat)
            print colored("Secret message has been saved!",'green')
# function to read old chats
def read_chat_history():
    #first select a friend from the list
    read_for = select_a_friend()
    print '\n'
    # print the old chat with the help of if  statement
    for chat in friends[read_for].chats:
        time = chat.time.strftime("%d %B %Y")
        if chat.sent_by_me:
            print '[%s] %s: %s' % (colored(time,'blue'), colored('Sent By Me:','red'), chat.message)
        else:
            print '[%s] %s read: %s' % (colored(time,'blue'), colored(friends[read_for].name,'red'), chat.message)

def start_chat(spy):

    spy.name = spy.salutation + " " + spy.name
    #checking the valid age of user with the help of if statement
    if spy.age > 18 and spy.age < 50:
        print colored("Authentication complete. Welcome ",'green') + colored(spy.name,'blue') + colored(" of age ",'green') \
              + colored(str(spy.age),'blue') + colored(" and rating ",'green') + colored(str(spy.rating),'blue') + colored(" Good to see you on board",'green')

        show_menu = True

        while show_menu:
            menu_choices = "What do you want to do? \n 1. Add a status update \n 2. Add a friend \n 3. Send a secret message \n 4. Read a secret message \n 5. Read Chats from a user \n 6. Close Application \n"
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)
                #iptions to be selected in a menu
                if menu_choice == 1:
                    spy.current_status_message = add_status()
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends' % (number_of_friends)
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                else:
                    show_menu = False
    else:
        print colored('Sorry Your age is not correct to be a spy','red')
#if the choice of user is available in the list
if existing == "Y":
    start_chat(spy)
else:
    spy = Spy('','',0,0.0)
     #if user is a new to this spy chat...we collect its information
    spy.name = raw_input(colored("..Welcome to spy chat,\n Before proceeding tell me your spy name first: --->",'green'))
    #if spy name entered is valid..proceed further
    if len(spy.name) > 0:
        spy.salutation = raw_input(colored("Should I call you Mr. or Ms.?: ",'blue'))
        spy.age = raw_input(colored("Enter your age?",'blue'))
        spy.age = int(spy.age)
        spy.rating = raw_input(colored("What is your spy rating?",'blue'))
        spy.rating = float(spy.rating)

        start_chat(spy)
    else:  #if name eneterd is invalid
        print colored('Please give a valid spy name','red')

