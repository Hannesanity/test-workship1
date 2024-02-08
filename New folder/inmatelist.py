import numpy as np
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os
import tkinter as tk
import random
import time
from datetime import datetime
from tkinter import messagebox
import mysql.connector as mycon
from mysql.connector import Error

root = Tk()
root.title("Registered List")
root.geometry("1180x620+210+100")



y_scroll = tk.Scrollbar(orient = tk.VERTICAL)
x_scroll = tk.Scrollbar(orient = tk.HORIZONTAL)

inmate_table = ttk.Treeview(columns=("Registered No.","Inmate No.", "DOB", "Gender", "Address", "Contact No.", "Nationality"),yscrollcommand = y_scroll.set, xscrollcommand = x_scroll.set)
inmate_table.pack(fill=tk.BOTH, expand = True)

y_scroll.config(command= inmate_table.yview)
x_scroll.config(command= inmate_table.xview)

y_scroll.pack(side= tk.RIGHT, fill = tk.Y)
x_scroll.pack(side= tk.BOTTOM, fill = tk.X)

inmate_table.heading("Registered No.", text="Registered No.")
inmate_table.heading("Inmate No.", text="Inmate No.")
inmate_table.heading("DOB", text="DOB")
inmate_table.heading("Gender", text="Gender")
inmate_table.heading("Address", text="Address")
inmate_table.heading("Contact No.", text="Contact No.")
inmate_table.heading("Nationality", text="Nationality")


inmate_table['show'] = 'headings'

inmate_table.pack(fill = tk.BOTH, expand = True)
				
conn = mycon.connect(host="localhost", user="root", password="", database="cvtest")
curr = conn.cursor()
curr.execute("SELECT * FROM detainees")
rows = curr.fetchall()
if len(rows)!=0:
		inmate_table.delete(*inmate_table.get_children())
		for row in rows:
			inmate_table.insert('', tk.END, value = row)
			conn.commit()
		conn.close()

root.mainloop()
