# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:28:48 2020

@author: aks273
"""

import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import Entry
from tkinter import simpledialog
from tkinter import filedialog
import glob
import os
import pandas

def fileget():
    global originfile, originfilepath
    originfile = []
    originfilepath = []
    originfile = filedialog.askopenfilename(initialdir = originfilepath,
                                             title = "Select a file")
    print(originfile)
    return originfile, originfilepath

def bottlevalues():
    global leftbottle, centerbottle, rightbottle
    leftbottle = []
    centerbotte = []
    rightbottle = []
    
    leftbottle = simpledialog.askstring("New Analysis","Enter left bottle descriptor")
    centerbottle = simpledialog.askstring("New Analysis","Enter center bottle descriptor")
    rightbottle = simpledialog.askstring("New Analysis","Enter right bottle descriptor")
    
    print("left = " + leftbottle)
    print("center = " + centerbottle)
    print("right = " + rightbottle)
    
    return leftbottle, centerbottle, rightbottle

def newfile():
    global originfile, originfilepath, leftbottle, centerbottle, rightbottle
    data = pandas.read_csv(originfile) #read in the csv
    
    select = data[['Squeeze1', 'rating.response']] #select just the data
    
    select = select.dropna() #dropping missing values
    select = select.reset_index(drop = True) #resetting the row numbers
    
    select['Squeeze1'] = select['Squeeze1'].replace(['left'], leftbottle) #replace values for Squeeze1
    select['Squeeze1'] = select['Squeeze1'].replace(['center'], centerbottle)
    select['Squeeze1'] = select['Squeeze1'].replace(['right'], rightbottle)
    
    select.rename(columns = {'Squeeze1':'Given_Stimulus'}, inplace = True) #rename columns
    select.rename(columns = {'rating.response':'Subject_Response'}, inplace = True)
    
    #match = [] #for loop to redefine responses as numerical values
    select['Match'] = np.where(select["Given_Stimulus"] == select["Subject_Response"],
                               'Yes', 'No')
    
    print(select)
    
    filelocation = originfile[:-4]
    select.to_csv(filelocation + "_screened.csv", line_terminator = '\r', index = False)

top = tk.Tk()

LoadFile = tk.Button(top, text = "Choose File", command = fileget)
LoadFile.pack()

Bottles = tk.Button(top, text = "Enter Bottle Values", command = bottlevalues)
Bottles.pack()

FileCreate = tk.Button(top, text = "Make File", command = newfile)
FileCreate.pack()

top.mainloop()
