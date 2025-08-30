'''
Designed and Developed by Thomas Jino. (B.Tech CSE Student @ College of Engineering, Aranmula, Kerala, India)

Thank You for using this Software.

Please give a star to the repository if you like it.

Follow me on GitHub : https://github.com/Thomas-Jino
Follow me on Instagram : https://www.instagram.com/__thomaa_chayannn__/


Also, do check out my other projects on GitHub. Thank You.

'''

#Importing Modules
import mysql.connector as mysql #mysql-connector-python
from tkinter import *           #tkinter
from tkinter import messagebox  #messagebox
from tkinter import ttk         #ttk
from tkinter import Canvas      #Canvas

#Creating Database
try:
    mysql_connection = mysql.connect(host="<your-host-ip-here", user="<your-username>", password="your-password-here",database="your-database-name-here")
    cursor = mysql_connection.cursor()
    cursor.execute("Create table if not exists EMPLOYEE (EMPID int(12),Name varchar(30), DATE_OF_JOIN DATE,SALARY DECIMAL(12,2),GENDER VARCHAR(10),POSITION VARCHAR(100),PHONE int(10), EMAIL varchar(20))")
    mysql_connection._connection_timeout = 5
except mysql.InterfaceError:
    messagebox.showerror("Error", "Server seems down")
    exit()
else:
    messagebox.showinfo("Success", "Connected to the server Succesfully")
#Creating Main Window
win = Tk()
win.title("Human Resource Management System Software (HRMSS)")
win.geometry("800x600+200+50")
win.resizable(False, False)
win.config(bg="light blue")
win.attributes('-topmost', True)
#Creating Tree

#Treeview
treelabel = Label(win, text="Employee Details", font=("Arial", 12, "bold"), bg="light blue")
treelabel.place(x=405, y=70)
tree = ttk.Treeview(win, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"), show='headings', height=20)
tree.heading("#1", text="ID")
tree.heading("#2", text="Name")
tree.heading("#3", text="Date Joined")
tree.heading("#4", text="Salary")
tree.heading("#5", text="Gender")
tree.heading("#6", text="Position")
tree.heading("#7", text="Phone")
tree.heading("#8", text="Email")
tree.column("#1", width=30, anchor=CENTER)
tree.column("#2", width=45, anchor=CENTER)
tree.column("#3", width=75, anchor=CENTER)
tree.column("#4", width=50, anchor=CENTER)
tree.column("#5", width=56, anchor=CENTER)
tree.column("#6", width=50, anchor=CENTER)
tree.column("#7", width=50, anchor=CENTER)
tree.column("#8", width=40, anchor=CENTER)
tree.place(x=402, y=100)

#Adding Scrollbar
#scroll = Scrollbar(win, orient="vertical", command=tree.yview)
#scroll.place(x=780, y=100, height=400)
#tree.configure(yscrollcommand=scroll.set)

#Adding data to the tree
cursor.execute("Select * from EMPLOYEE")
data = cursor.fetchall()
for i in data:
    tree.insert("", END, values=i)

#Defining Functions

#Radio Button
select = StringVar()
select.set(0)
def gender():
    select.get()

#Frame3 Buttons

#clear
def clear():
    EMPID_entry.delete(0, END)
    Name_entry.delete(0, END)
    Date_entry_day.delete(0, END)
    Date_entry_month.delete(0, END)
    Date_entry_year.delete(0, END)
    select.set(0)
    Position_entry.set('')
    Salary_entry.delete(0, END)
    Phone_entry.delete(0, END)
    Email_entry.delete(0, END)

#ADD Button
def Add():
    empid = EMPID_entry.get()
    if empid.isnumeric():
        pass
    elif empid == '':
        messagebox.showerror("Error", "Employee ID cannot be empty")
        EMPID_entry.delete(0, END)
        return
    else:
        messagebox.showerror("Error", "Employee ID must be numeric")
        EMPID_entry.delete(0, END)
        return
    name = Name_entry.get()
    if name.isalpha() or ' ':
        pass
    else:
        messagebox.showerror("Error", "Name must be alphabetic")
        Name_entry.delete(0, END)
        return
    date_day = Date_entry_day.get()
    date_month = Date_entry_month.get()
    date_year = Date_entry_year.get()
    if select.get() == 'Male':
        gender=select.get()
    elif select.get() == 'Female':
        gender=select.get()
    else:
        gender=''
    position = Position_entry.get()
    salary = Salary_entry.get()
    if salary.isnumeric() or '.':
        pass
    else:
        messagebox.showerror("Error", "Salary must be numeric")
        Salary_entry.delete(0, END)
        return
    phone = Phone_entry.get()
    if phone.isnumeric() or "+" or " ":
        pass
    else:
        messagebox.showerror("Error", "Phone must be numeric")
        Phone_entry.delete(0, END)
        return
    email = Email_entry.get()
    #print([empid, name,date_day,date_month,date_year,gender,position,salary,phone,email])
    try:
        DATE_OF_JOIN = date_year + '-' + date_month + '-' + date_day
        cursor.execute("Insert into EMPLOYEE values(%s,%s,%s,%s,%s,%s,%s,%s)",(empid,name,DATE_OF_JOIN,salary,gender,position,phone,email))
        cursor.execute("commit")
        messagebox.showinfo("Success", "Employee record added successfully!")
        clear()
    except mysql.DatabaseError:
        messagebox.showerror("Error", "Employee ID already exists")
        clear() 
    else:
        tree.insert("", END, values=(empid,name,DATE_OF_JOIN,salary,gender,position,phone,email))
        clear()

# Function to delete selected item

def Remove():
    selected_item = tree.selection()  # Get selected item
    if selected_item:
        values = tree.item(selected_item, "values")  # Get selected item values
        emp_id = values[0]  # Extract EMPID from the selected row
        
        # Confirm deletion
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete Employee ID {emp_id}?")
        if confirm:
            cursor.execute("DELETE FROM EMPLOYEE WHERE EMPID=%s", (emp_id,))
            mysql_connection.commit()  # Commit the change to the database
            
            tree.delete(selected_item)  # Delete the item from the TreeView
            messagebox.showinfo("Success", "Employee record deleted successfully!")
        else:
            messagebox.showinfo("Cancelled", "Deletion cancelled")
    else:
        messagebox.showerror("Error", "No employee selected")

#Function to Upgrade

def Edit():
    selected_item = tree.selection()  # Get selected item from treeview
    if selected_item:
        values = tree.item(selected_item, 'values')  # Get selected item values
        emp_id = values[0]  # Get Employee ID
        
        # Confirmation Message Box
        confirm = messagebox.askyesno("Edit", f"Do you want to edit Employee ID = {emp_id}?")
        
        if not confirm:
            messagebox.showinfo("Cancelled", "No changes were made.")
            return

        # If Yes, fill the entry boxes with selected data
        EMPID_entry.delete(0, END)
        Name_entry.delete(0, END)
        Date_entry_day.delete(0, END)
        Date_entry_month.delete(0, END)
        Date_entry_year.delete(0, END)
        Salary_entry.delete(0, END)
        Phone_entry.delete(0, END)
        Email_entry.delete(0, END)

        EMPID_entry.insert(0, values[0])  # Employee ID
        Name_entry.insert(0, values[1])  # Name
        Date_entry_day.insert(0, values[2][8:10])  # Day
        Date_entry_month.insert(0, values[2][5:7])  # Month
        Date_entry_year.insert(0, values[2][0:4])  # Year
        select.set(values[4])  # Gender
        Position_entry.set(values[5])  # Position
        Salary_entry.insert(0, values[3])  # Salary
        Phone_entry.insert(0, values[6])  # Phone
        Email_entry.insert(0, values[7])  # Email

        # Remove from Database
        cursor.execute("DELETE FROM EMPLOYEE WHERE EMPID=%s", (emp_id,))
        mysql_connection.commit()  # Commit changes

        # Remove from TreeView
        tree.delete(selected_item)

        messagebox.showinfo("Success", f"Employee ID {emp_id} is ready to be updated.")

    else:
        messagebox.showerror("Error", "No employee selected")

#Window Widgets

#Header
header = Label(win, text="Employee Management System", font=("Arial", 20, "bold","underline"), bg="light blue")
header.place(x=200, y=10)

# body
frame1 = Frame(win, width=400, height=490, bg="light blue")
frame1.place(x=0, y=50)
frame3 = Frame(win, width=850, height=50, bg="light blue")
frame3.place(x=0, y=540)

#Verticallineseperator
line = Canvas(win, width=1, height=478, bg="black")
line.place(x=395, y=60)

#frame1 widgets

#Employee ID
EMPID_label = Label(frame1, text="Employee ID : ", font=("Arial", 12, "bold"), bg="light blue")
EMPID_label.place(x=10, y=50)
EMPID_entry = Entry(frame1, font=("Arial", 12), bg="white", width=28)
EMPID_entry.place(x=130, y=50)

#Name
Name_label = Label(frame1, text="Name : ", font=("Arial", 12, "bold"), bg="light blue")
Name_label.place(x=10,y=100)
Name_entry = Entry(frame1, font=("Arial", 12), bg="white", width=28)
Name_entry.place(x=130,y=100)

#Date_joined
Date_label = Label(frame1, text="Date Joined : ", font=("Arial", 12, "bold"), bg="light blue")
Date_label.place(x=10,y=150)
Date_entry_day = Spinbox(frame1, font=("Arial", 12), bg="white", width=4, from_=1, to=31, state="readonly")
Date_entry_day.place(x=130,y=150)
Date_entry_month = Spinbox(frame1, font=("Arial", 12), bg="white", width=4, from_=1, to=12, state="readonly")
Date_entry_month.place(x=210,y=150)
Date_entry_year = Spinbox(frame1, font=("Arial", 12), bg="white", width=8, from_=1990, to=2025, state="readonly")
Date_entry_year.place(x=290,y=150)

#Gender
Gender_label = Label(frame1,text="Gender : ", font=("Arial", 12, "bold"), bg="light blue")
Gender_label.place(x=10,y=200)
chk_male = Radiobutton(frame1, text="Male", font=("Arial", 12), bg="light blue", value='Male',variable=select,command=gender)
chk_male.place(x=130,y=200)
chk_female = Radiobutton(frame1, text="Female", font=("Arial", 12), bg="light blue", value='Female',variable=select,command=gender)
chk_female.place(x=210,y=200)

#Position
Position_label = Label(frame1, text="Position : ", font=("Arial", 12, "bold"), bg="light blue")
Position_label.place(x=10,y=250)
Position_entry = ttk.Combobox(frame1,width=38,background="white",values=["Manager", "Assistant Manager", "Supervisor", "Senior Software Engineer", "Software Engineer", "Intern", "Cleaners","Security","Kitchen Staff"],state="readonly")
Position_entry.place(x=130,y=250)

#Salary
Salary_label = Label(frame1, text="Salary : ", font=("Arial", 12, "bold"), bg="light blue")
Salary_label.place(x=10,y=300)
Salary_entry = Entry(frame1, font=("Arial", 12), bg="white", width=28)
Salary_entry.place(x=130,y=300)

#Phone
Phone_label = Label(frame1, text="Phone : ", font=("Arial", 12, "bold"), bg="light blue")
Phone_label.place(x=10,y=350)
Phone_entry = Entry(frame1, font=("Arial", 12), bg="white", width=28)
Phone_entry.place(x=130,y=350)

#Email
Email_label = Label(frame1, text="Email : ", font=("Arial", 12, "bold"), bg="light blue")
Email_label.place(x=10,y=400)
Email_entry = Entry(frame1, font=("Arial", 12), bg="white", width=28)
Email_entry.place(x=130,y=400)

#frame2 widgets

#lineseperator
line = Canvas(frame3, width=850, height=1, bg="black")
line.place(x=0, y=1)

#Buttons
btnAdd = Button(frame3, text="Add", font=("Arial", 12, "bold"), bg="green", fg="black",width=12,command=Add)
btnAdd.place(x=40, y=10)
btnfire = Button(frame3, text="Remove", font=("Arial", 12, "bold"), bg="red", fg="black",width=12,command=Remove)
btnfire.place(x=220, y=10)
btnUpgrade = Button(frame3, text="Edit", font=("Arial", 12, "bold"), bg="white", fg="black",width=12,command=Edit)
btnUpgrade.place(x=450, y=10)

#Setting Mainloop()
win.mainloop()