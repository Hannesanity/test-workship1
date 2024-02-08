from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk 
import os
import time

root=tk.Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)
root.iconbitmap()

#### GIF IMAGE ####

frameCnt = 34
frames = [PhotoImage(file='BJMPgif.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
 
### Frames GIF ###

def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
       	ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)
label = Label(root)
label.place(x=100, y=75)
root.after(100, update, 0)

############# Login ################

def signin():
    global hframe
    username = user.get()
    password = pword.get()

    if username == 'admin' and password == '1234':
        root.destroy()
        import dasboard

    elif username != 'admin' and password != '1234':
        messagebox.showerror("Invalid", "Invalid Username and Password")

    elif username != "admin":
        messagebox.showerror("Invalid", "Invalid Username")

    elif password != "1234":
        messagebox.showerror("Invalid", "Invalid Password")

def change_to_home():
   home.pack(fill='both', expand=1)

frame=Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading=Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100,y=5)

##### USERNAME #####
def on_enter(e):
	user.delete(0, 'end')

def on_leave(e):
	name = user.get()
	if name == '':
		user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black',border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30,y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

##### PASSWORD #####
def on_enter(e):
	pword.delete(0, 'end')

def on_leave(e):
	name = pword.get()
	if name == '':
		pword.insert(0, 'Password')

pword = Entry(frame, width=25, fg='black',border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
pword.place(x=30,y=150)
pword.insert(0, 'Password')
pword.bind('<FocusIn>', on_enter)
pword.bind('<FocusOut>', on_leave)


Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

##### BUTTONS #####

Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)

root.mainloop()