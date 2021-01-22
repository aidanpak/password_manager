import hashlib # used for hashing password
import os # also used in hashing
from Python_Robofrom_dbConnection import DatabaseConnection
import time


#links to database and establishes connection object using class from import..
#creates a one time set_password
def set_Script_password():
    with DatabaseConnection('python_roboform.db') as connection:
        cursor=connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS manager_info(password text)')
        cursor.execute('SELECT password FROM manager_info')
        users = cursor.fetchall()
        if users==[]:
            print('Welcome to your Private Password Manager..')
            script_password = input('Please enter your one time password.. This password cannot be changed.. ').strip()
            set_password= input(f'Your set your Password as: "{script_password}" Would you like to to save this password? Type "yes" or "no" ').strip()
            if set_password=='no':
                print('Program is quitting... Please Relaunch to try again.. ')
                time.sleep(2)
                quit()
            cursor.execute('INSERT INTO manager_info(password) VALUES (?)', (script_password,))
            print("Password set successfully")



# creates table in database.. the password_manager
def create_table():
    with DatabaseConnection('python_roboform.db') as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS password_manager(website text, username text, password text)')



#creates random password for you automatically.. maybe using regex.. or random library #returns password
def create_randomPassword():
    edit = 'Sample Random Password'
    return edit


#adds new entries to database
def add_entry():
    website= input('Enter the name of the website you would like to enter: ').strip()
    username = input(f'Enter your username for {website} ').strip()
    generate = input('Would you like to generate a random password for source? Type "yes" or "no" ').strip()
    if generate == 'yes':
        create_randomPassword()
    else:
        password = input(f'Enter your password for {website} ').strip()


    with DatabaseConnection('python_roboform.db') as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO password_manager(website, username, password) VALUES (?,?,?)', (website.lower(), username, password))
    print('Your entry was saved successfully')
    return_to_menu()


# allows for an entries username of password to be edited. Can also generate random password
def edit_entry():
    website = input('Enter the website you are trying to edit. ').strip()
    edit_options= input('What would you like to edit. Type "username" or "password". ').strip()
    if edit_options == 'username':
        edit=input('What would you like to change your username to: ').strip()
    elif edit_options =='password':
        random = input(f'Would you like to generate a random password or enter a new password? Type "random" or "new" ').strip()
        if random == 'random':
            create_randomPassword()
        else:
            edit = input('What would you like to change your password to: ').strip()

    with DatabaseConnection('python_roboform.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM password_manager WHERE website=?', (website.lower(),))
        entry_edit = cursor.fetchall()
        if entry_edit == []:
            print(
                f'The entry:{website} was not found in the database. Make sure you entered the website name correctly.')
        else:
            if edit_options=='username':
                cursor.execute('UPDATE password_manager SET username=? WHERE website=?', (edit, website))
            elif edit_options=='password':
                cursor.execute('UPDATE password_manager SET password=? WHERE website=?', (edit,website))
            print('The new information was saved successfully!')
    return_to_menu()



#this function deletes sources from the database
def delete_entry():
    website=input('What is the name of the entry you are trying to delete? ').strip()
    with DatabaseConnection('python_roboform.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM password_manager WHERE website=?', (website.lower(),))
        entry_deleted = cursor.fetchall()
        cursor.execute('DELETE FROM password_manager WHERE website=?', (website.lower(),))
    if entry_deleted == []:
        print(f'The entry:{website} was not deleted from the database because no entry was found.')
    else:
        print('Entry successfully deleted')
    return_to_menu()


#this function will print the username and password for the desired source to the screen..
def find_entry():
    website = input('Enter the website you are looking for: ').strip()
    with DatabaseConnection('python_roboform.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM password_manager where website=?', (website.lower(),))
        entry = cursor.fetchone()
        try:
            print(f'{entry[0]} -- username:{entry[1]} -- password:{entry[2]}\n')
        except TypeError:
            print(f'There was no information found for {website}. Make sure you entered the website name correctly.\n')
        finally:
            return_to_menu()



#this function will first return all entries... then will ask if wanting to edit an entry
def view_entries():
    with DatabaseConnection('python_roboform.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM password_manager')
        entries = [{'website':website, 'username':username, 'password':password} for website,username, password in cursor.fetchall()]
        if entries == []:
            print('There are no entries in your database.')
        else:
            for entry in entries:
                print(f'Information found for:\n{entry["website"].title()}\n')
    return_to_menu()


#requiring a password to enter the manager.. will return 1 if valid master password..
def enter_manager():
    with DatabaseConnection('python_roboform.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT password FROM manager_info')
        tuple = cursor.fetchone()

    master_password = tuple[0]
    encode = master_password.encode('utf-8')
    salt = os.urandom(32)
    hash = hashlib.pbkdf2_hmac('sha256', encode, salt, 100000)
    guess = input("Enter your password ")
    encoded_guess = guess.encode('utf-8')
    hashed_guess = hashlib.pbkdf2_hmac('sha256', encoded_guess, salt, 100000)
    if hashed_guess == hash:
        return True
    else:
        print('Invalid Password')
        another_attempt = input("Type any key to try again or type 'q' to quit: ").strip()
        if another_attempt == "q":
            quit()
        else:
            enter_manager()
    return False




def return_to_menu():
    close = input('type "menu" to return to the main menu or "q" to quit: ').strip()
    if close != 'menu':
        quit()


def main():
    set_Script_password()
    create_table()
    enter_manager() # will return True if correct password...
    if True:
        message = '''
        Welcome to Roboform
        -------------------
        
        Type 'a' to add a new entry to the database
        Type 'f' to find an entry and return its information 
        Type 'v' to view all entries stored in the database
        Type 'd' to delete an entry
        Type 'e' to edit an entry 
        Type 'q' to quit 
        
        
        '''
        menu = input(message)
        while menu != 'q':
            if menu == 'a':
                add_entry()
            elif menu == 'f':
                find_entry()
            elif menu =='v':
                view_entries()
            elif menu =='d':
                delete_entry()
            elif menu == 'e':
                edit_entry()
            menu=input(message)


if __name__ == '__main__':
    main()



