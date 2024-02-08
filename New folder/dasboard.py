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

root=tk.Tk()
root.title('Bilang-Go')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)
root.iconbitmap()

def nextPage():
	root.destroy()
	import inmatereg

Button(width=30, pady=7, text='Home', bg ='#57a1f8', fg='white', border=0).place(x=23, y=100)
Button(width=30, pady=7, text='Recognizer', bg ='#57a1f8', fg='white', border=0).place(x=23, y=140)
Button(width=30, pady=7, text='Register Inmate', bg ='#57a1f8', fg='white', border=0, command=nextPage).place(x=23, y=180)
Button(width=30, pady=7, text='Settings', bg ='#57a1f8', fg='white', border=0).place(x=23, y=220)

root.mainloop()