import sqlite3

con = sqlite3.connect('DenoiseDB.sqlite')
cursor = con.cursor()
cont = True

sql = '''CREATE TABLE USERS(
	 UserID INTEGER PRIMARY KEY AUTOINCREMENT,
   Username TEXT NOT NULL,
	 HashPassword INTEGER NOT NULL 
)'''


#cursor.execute(sql)
#con.commit()

def createuser():
    uniqueuser = False
    while uniqueuser == False:
        inpname = str(input("Username?"))

        cursor.execute("SELECT Username FROM USERS")
        con.commit()
        Usernames = cursor.fetchall()
        for i in range(len(Usernames)):
            print(Usernames[i])
            if Usernames[i] == inpname:

                uniqueuser = False
                print("Username already exists")
                break
            else:
                uniqueuser = True
    inppassword = int(hash(input("Password?")))
    cursor.execute("INSERT INTO USERS (Username, HashPassword) VALUES (?, ?)", (inpname, inppassword))
    con.commit()


def viewdb():
    # viewrows = []
    cursor.execute("SELECT * FROM USERS")
    con.commit()
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def updateuser():
    ID = input("ID: ")
    cursor.execute("SELECT * FROM USERS WHERE UserID = (?)", (ID))
    con.commit()
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    fields = int(input("Name (1) - Password (2) - Both (3)"))
    if fields == 1:
        newname = input("New name: ")
        cursor.execute("UPDATE USERS SET Name = ? WHERE UserID = ?", (newname, ID))
        con.commit()

    if fields == 2:
        newpass = int(hash(input("Password?")))
        cursor.execute("UPDATE USERS SET HashPassword = ? WHERE UserID = ?", (newpass, ID))
        con.commit()

    if fields == 3:
        newname = input("New name: ")
        newpass = int(hash(input("New password: ")))
        cursor.execute("UPDATE USERS SET Name = ?, Length = ? WHERE UserID = ?", (newname, newpass, ID))
        con.commit()


def deleteuser():
    ID = input("ID: ")
    cursor.execute("DELETE FROM USERS WHERE UserID = ?", (ID))
    con.commit()


while cont == True:
    choice = input("Input (i) - View (v) - Update (u) - Delete (d) - Stop(s)")
    if choice == "v":
        viewdb()

    elif choice == "i":
        createuser()

    elif choice == "u":
        updateuser()

    elif choice == "d":
        deleteuser()

    elif choice == "s":
        cont = False

