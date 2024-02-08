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

def prevPage():
    root.destroy()
    import inmatereg

root = Tk()
root.title("Profile")
root.geometry("1180x620+210+100")
root.config(bg = "#ffffff")

lblprofile = Label(text="INMATE'S PROFILE", width = 10, height = 2, bg = "#07bdff", fg ='#fff', font = 'Arial 20 bold').pack(side = TOP, fill = X)

lblInmate2 = Label(text = "Inmate No:", font = ("arial", 20,"bold")).place(x = 30, y = 200)
lblDOB2 = Label(text = "Date of Birth:", font = ("arial", 20,"bold")).place(x = 30, y = 300)
lblGender2 = Label(text = "Gender:", font = ("arial", 20,"bold")).place(x = 30, y = 400)

lblAdd2 = Label(text = "Address:", font = ("arial", 20,"bold")).place(x = 500, y = 200)
lblCont2 = Label(text = "Contact No.:", font = ("arial", 20,"bold")).place(x = 500, y = 300)
lblNat2 = Label(text = "Nationality:", font = ("arial", 20,"bold")).place(x = 500, y = 400)

btnBack = Button(text = "Back", width = 19, height = 2, font = "arial 12 bold", bg = "lightblue", command=prevPage)
btnBack.place(x = 30, y = 500)

root.mainloop()

