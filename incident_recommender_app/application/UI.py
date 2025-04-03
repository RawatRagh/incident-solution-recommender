# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 23:01:12 2022

@author: Karan Gupta
This is optional file and only to be used if the application is to be used as windows form
"""
# Creating GUI with tkinter
import os
from tkinter import *
from dotenv import load_dotenv
from prediction import predict
from os.path import join, dirname

def send():
    msg = EntryBox.get("1.0" ,'end-1c').strip()
    EntryBox.delete("0.0" ,END)
    print(msg)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END,"---------------------------------Start of Query----------------------------------------------" + '\n\n')
        ChatLog.insert(END, "You :" + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Arial", 10))
        output = ''
        res = predict(msg,True)
        print(res)
        if len(res) > 1:
            for o in res:
                output = output + "Record No. " + str(res.index(o) + 1) + '\n\n'
                o = o.replace(delimiter, "\n\n")
                output = output + o + "\n\n" + \
                         "-------------------------------------------------------------------------------------------------------------" + \
                         "\n"
        else:
            output = res[0]

        ChatLog.insert(END, "Recommender :"+ '\n\n'+ output + '\n\n')
        ChatLog.insert(END, "---------------------------------End of Query----------------------------------------------" + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("Welcome to Incident Solution Recommender")

base.geometry("550x550")
base.resizable(width=FALSE, height=FALSE)



# Create Chat window
ChatLog = Text(base, bd=1, bg="white", height="375", width="500", font="Arial", wrap="word")
def_msg = "Welcome to Incident Solution Recommender. Please enter the short description of the incident.!!!"
ChatLog.config(foreground="#442265", font=("Arial", 10))
ChatLog.insert(END, "Recommender :" + def_msg + '\n\n')
ChatLog.config(state=DISABLED)

# Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="arrow")
ChatLog['yscrollcommand'] = scrollbar.set

"""Setup to read env file for various parameters"""
dotenv_path = join(dirname(__file__), 'var.env')
load_dotenv(dotenv_path)

"""Read Parameters from env file"""
delimiter = os.getenv('delimiter')

# Create Button to send message
SendButton = Button(base, font=("Verdana", 9, 'bold'), text="Send", width="12", height=5,
                    bd=3, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                    command=send)

# Create the box to enter message
EntryBox = Text(base, bd=2, bg="light grey", width="375", height="5", font=("Arial", 10))
# EntryBox.bind("<Return>", send)


# Place all components on the screen
scrollbar.place(x=525, y=6, height=375)
ChatLog.place(x=6, y=6, height=375, width=500)
EntryBox.place(x=6, y=401, height=90, width=350)
SendButton.place(x=356, y=420, height=50)

base.mainloop()