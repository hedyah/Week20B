

from ast import While
from unittest import result
import mariadb
import dbcreds

def connect_db():
    conn = None
    cursor = None
    
    try:
        conn = mariadb.connect(
                            user = dbcreds.user,
                            password = dbcreds.password,
                            host = dbcreds.host,
                            port = dbcreds.port,
                            database = dbcreds.database
    )
        cursor = conn.cursor()
        return (conn, cursor)
    
    except mariadb.OperationalError as e:
        print("got an operational error")
        if ("access denied" in e.msg):
            print("failed to log in")
        disconnect_db(conn, cursor)
        
def disconnect_db(conn, cursor):
    if(cursor != None):
        cursor.close()
    if(conn != None):
        conn.rollback()
        conn.close()
        
def run_query(statement, args=None):
    
    try:
        (conn, cursor) = connect_db()
        if statement.startswith("SELECT"):
            cursor.execute(statement,args)
            result = cursor.fetchall()
            #print("total of {} users" .format(cursor.rowcount))
            
            return result
            
        else:
            cursor.execute(statement, args)
            if cursor.rowcount == 1:
                conn.commit()
                print("insert sucessful")
            else:
                print("failed to instert")
    
    except mariadb.OperationalError as e:
        print("got an operational error")
        if ("access denied" in e.msg):
            print("failed to log in")

    except mariadb.IntegrityError as e:
        # if("CONSTRAINT `user_CHECK_username`" in e.msg):
        #     print("error, all usernames must start with the letter J")
        # if ("CONSTRAINT `user_CHECK_age`" in e.msg):
        #     print("error user is outside of acceptable range")
    
            print("intergity error")
            print(e.msg)

    except mariadb.ProgrammingError as e:
        if("SQL syntax" in e.msg):
            print("There is an error in you code, check your code!!")
        else:
            print("got a different programing error")
            print(e.msg)

    except RuntimeError as e:
        print("caught a run time error")
        e.with_traceback

    except Exception as e :
        print(e.with_traceback)
        
    
print("Welcome to our site!")
user_login = input("Please enter your username:  ")
user_password = input("Please enter your password: ")

print('You are now logged in!')
print('Here are some options for you!')
print("1. Enter new exploits?")
print("2. See all of your exploits?")
print("3. See all other exploits?")
print("4. Exit the application?")

login = run_query("SELECT alias from hackers Where alias=?", [user_login])
if login==user_login:
    pw = run_query("SELECT password from hackers WHERE password=?", [user_password])
    if pw == user_password:
            print('You are now logged in!')
    
user_id = run_query("SELECT id from hackers WHERE alias=?",[user_login])
print (user_id)

while True:
    
            
            selected = input("enter your selection (1/2/3/4): ")
                
            if selected == '1':
                new_post = input("type your exploits here: ")
                run_query("INSERT INTO exploits(content, user_id) VALUES(?,?)",[new_post, user_id])
                print ("posted exploits sucesssfully!")
                
            elif selected == '2':
                see_post = run_query("SELECT * FROM exploits WHERE user_id=?", [user_id])
                print("here are all your exploits: ")
                print(result)
            elif selected == '3':
                see_users = run_query("SELECT * FROM exploits")
                print("Here are other exploits: ")
                print(result)

            elif selected == '4':
                exit_app = input("would you like to exit ? (yes/no): ")
                if exit_app == "yes":
                    break
                
            
            else:
                print("invalid input, try again please!")
print(result)


