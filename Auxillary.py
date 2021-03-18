import ClubPage as pg
import OperationFunctions as of
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import tkinter.messagebox as mb
import pandas as pd
import numpy as np

class viewDetails(tk.Frame):
    def __init__(self,master,coach,choice):
        self.master=master
        self.coach=coach
        self.choice=choice
        if len(self.coach.loc[self.choice])==1:
            self.lastDate=self.coach.loc[self.choice,"Τελευταία Μισθοδοσία"].iloc[0]
            self.TrueCoach=self.coach.loc[self.choice]
        else:
            self.lastDate=self.coach.loc[self.choice,"Τελευταία Μισθοδοσία"].max()
            self.TrueCoach=self.coach.loc[self.choice].where(self.coach.loc[self.choice]["Τελευταία Μισθοδοσία"]==self.lastDate).dropna()
        createCondition=len(pd.date_range(start=self.lastDate.to_timestamp(),end=pd.Timestamp.now(),freq="MS"))==0
        self.root=tk.Toplevel(self.master.root)
        self.master.w_c["EditSalary"]=self.root
        self.root.title("Στοιχεία Μισθοδοσίας")
        topCanvas=tk.Canvas(self.root,height=800,width=700,bg="#1b2135")
        topCanvas.pack()
        mainFrame=tk.Frame(topCanvas,bg="#1b2135")
        mainFrame.place(relheight=1,relwidth=1)
        #Intro Information
        message="Μισθοδοτικά στοιχεία"
        label=tk.Label(mainFrame,text=message,bg="#1b2135",fg="#fff",font=("Arial",28))
        label.place(relheight=0.15,relwidth=0.9,relx=0.05,rely=0.05)
        message="Tου μισθοδοτούμενου: "
        label=tk.Label(mainFrame,text=message,bg="#1b2135",fg="#bdbcb9",font=("Arial",16))#Name of employee
        label.place(relheight=0.1,relwidth=0.4,relx=0.0,rely=0.15)
        message=self.choice[0]+" "+self.choice[1]
        label=tk.Label(mainFrame,text=message,bg="#1b2135",fg="#bdbcb9",font=("Arial",16))
        label.place(relheight=0.1,relwidth=0.4,relx=0.35,rely=0.15)
        message="Ημερομηνία Μισθοδοσίας: "
        label=tk.Label(mainFrame,text=message,bg="#1b2135",fg="#bdbcb9",font=("Arial",16))
        label.place(relheight=0.1,relwidth=0.5,relx=0.0,rely=0.225)
        if len(self.coach.loc[self.choice])==1:
            options=[self.coach.loc[self.choice]["Τελευταία Μισθοδοσία"].iloc[0]]
        else:
            options=list(self.coach.loc[self.choice]["Τελευταία Μισθοδοσία"])
        self.Past=tk.StringVar()#string variable to determine which month's
        self.Past.set(options[-1])
        #message=str(self.TrueCoach["Τελευταία Μισθοδοσία"].iloc[0])
        Date=tk.OptionMenu(mainFrame,self.Past,*options,command=lambda value:self.PastSalary(value) if value!=self.lastDate else self.Past.set(self.lastDate))#Date of last paycheck
        Date.config(bg="#fff",fg="#010101",font=("Arial",16))
        Date["menu"].config(bg="#fff",fg="#010101",font=("Arial",16))
        Date.place(relheight=0.05,relwidth=0.2,relx=0.45,rely=0.25)

        label=tk.Label(mainFrame,text="Αναλυτικά",bg="#1b2135",fg="#fff",font=("Arial",20))
        label.place(relheight=0.1,relwidth=0.4,relx=0.3,rely=0.3)

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.075,relwidth=0.85,relx=0.05,rely=0.4)
        label=tk.Label(labelFrame,text="Μέρος από Ημερήσιες Αποδοχές:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.place(relheight=1,relwidth=0.6)
        self.dailyVar=tk.StringVar()
        self.dailyVar.set(self.TrueCoach["Ημερήσιες Αποδοχές"].iloc[0] if createCondition else 0)
        self.dailyentry=tk.Entry(labelFrame,textvariable=self.dailyVar,bg="#fff",font=("Arial",18))
        self.dailyentry.place(relheight=1,relwidth=0.4,relx=0.6)
        self.dailyentry["state"]=tk.DISABLED

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.075,relwidth=0.8,relx=0.05,rely=0.525)
        label=tk.Label(labelFrame,text="Μέρος από Ωριαίες Αποδοχές:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.place(relheight=1,relwidth=0.6)
        self.hourlyVar=tk.StringVar()
        self.hourlyVar.set(self.TrueCoach["Ωριαίες Αποδοχές"].iloc[0] if createCondition else 0)
        self.hourlyentry=tk.Entry(labelFrame,textvariable=self.hourlyVar,bg="#fff",font=("Arial",18))
        self.hourlyentry.place(relheight=1,relwidth=0.4,relx=0.6)
        self.hourlyentry["state"]=tk.DISABLED

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.075,relwidth=0.6,relx=0.05,rely=0.65)
        label=tk.Label(labelFrame,text="Μέρος από Bonus:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.place(relheight=1,relwidth=0.5)
        self.bonusVar=tk.StringVar()
        self.bonusVar.set(self.TrueCoach["Bonus"].iloc[0] if createCondition else 0)
        self.bonusentry=tk.Entry(labelFrame,textvariable=self.bonusVar,bg="#fff",font=("Arial",18))
        self.bonusentry.place(relheight=1,relwidth=0.5,relx=0.5)
        self.bonusentry["state"]=tk.DISABLED



        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.075,relwidth=0.6,relx=0.05,rely=0.775)
        label=tk.Label(labelFrame,text="Σύνολο:",bg="#1b2135",fg="#fff",font=("Arial",18,"bold"))
        label.place(relheight=1,relwidth=0.3,relx=0.2)
        self.final=tk.Label(labelFrame,text=str(int(float(self.hourlyVar.get()))+int(float(self.bonusVar.get()))+int(float(self.dailyVar.get()))),fg="#010101",bg="#fff",font=("Arial",18),anchor="w")
        self.final.place(relheight=1,relwidth=0.5,relx=0.5)


        editButton=tk.Button(mainFrame,text="Επεξεργασία",command=self.enable,bg="#bec1c4",font=('Arial',18))
        editButton.place(relheight=0.075,relwidth=0.4,relx=0.05,rely=0.9)
        self.doneButton=tk.Button(mainFrame,text="Ολοκλήρωση",command=self.complete,bg="#bec1c4",font=('Arial',18))
        self.doneButton.place(relheight=0.075,relwidth=0.4,relx=0.55,rely=0.9)
        self.doneButton["state"]=tk.DISABLED

        self.root.protocol("WM_DELETE_WINDOW",self.exit)
        self.root.mainloop()

    def exit(self):
        self.master.w_c["EditSalary"]=""
        self.root.destroy()

    def enable(self):
        self.dailyentry["state"]=tk.NORMAL
        self.hourlyentry["state"]=tk.NORMAL
        self.bonusentry["state"]=tk.NORMAL
        self.doneButton["state"]=tk.NORMAL

    def complete(self):
        try:
            if len(pd.date_range(start=self.lastDate.to_timestamp(freq="D"),end=pd.Timestamp.now(),freq="MS"))==0 or self.lastDate.to_timestamp(freq="D")==pd.to_datetime("1-1-2020"):
                self.coach.loc[self.choice,"Ημερήσιες Αποδοχές"]=int(self.dailyVar.get())
                self.coach.loc[self.choice,"Ωριαίες Αποδοχές"]=int(self.hourlyVar.get())
                self.coach.loc[self.choice,"Bonus"]=int(self.bonusVar.get())
                self.coach.loc[self.choice,"Σύνολο"]=int(self.dailyVar.get())+int(self.hourlyVar.get())+int(self.bonusVar.get())
                self.bonusVar.set(int(self.dailyVar.get())+int(self.hourlyVar.get())+int(self.bonusVar.get()))
                self.coach.loc[self.choice,"Τελευταία Μισθοδοσία"]=pd.Timestamp.now().to_period("D")
            else:
                temp=self.TrueCoach.copy()
                temp["Ημερήσιες Αποδοχές"]=int(self.dailyVar.get())
                temp["Ωριαίες Αποδοχές"]=int(self.hourlyVar.get())
                temp["Bonus"]=int(self.bonusVar.get())
                temp["Σύνολο"]=int(self.dailyVar.get())+int(self.hourlyVar.get())+int(self.bonusVar.get())
                self.bonusVar.set(int(self.dailyVar.get())+int(self.hourlyVar.get())+int(self.bonusVar.get()))
                temp["Τελευταία Μισθοδοσία"]=pd.Timestamp.now().to_period("D")
                self.coach=self.coach.append(temp)
            pg.writeCoaches(self.coach)
            self.master.redraw()
        except ValueError:
            mb.showinfo("Λάθος Είσοδος","Στα πεδία αποδοχών πρέπει να αναγραφεί το ποσό της αποδοχής, το οποίο είναι ένας ακέραιος αριθμός.")
    def PastSalary(self,value):
        self.Past.set(self.lastDate)
        selected=self.coach.loc[self.choice].where(self.coach.loc[self.choice]["Τελευταία Μισθοδοσία"]==value).dropna()
        miniroot=tk.Toplevel(self.root)
        miniroot.title("Μισθοδωσία {}".format(value))
        topCanvas=tk.Canvas(miniroot,height=800,width=700,bg="#1b2135")
        topCanvas.pack()
        mainFrame=tk.Frame(topCanvas,bg="#1b2135")
        mainFrame.place(relheight=1,relwidth=1)
        #Intro Information
        message="Μισθοδοτικά στοιχεία"
        label=tk.Label(mainFrame,text=message,bg="#1b2135",fg="#fff",font=("Arial",28))
        label.place(relheight=0.15,relwidth=0.9,relx=0.05,rely=0.05)
        message="Tου μισθοδοτούμενου: "
        label=tk.Label(mainFrame,text=message,bg="#1b2135",fg="#bdbcb9",font=("Arial",16))#Name of employee
        label.place(relheight=0.1,relwidth=0.4,relx=0.0,rely=0.15)
        message=self.choice[0]+" "+self.choice[1]
        label=tk.Label(mainFrame,text=message,bg="#1b2135",fg="#bdbcb9",font=("Arial",16))
        label.place(relheight=0.1,relwidth=0.4,relx=0.35,rely=0.15)
        message="Ημερομηνία Μισθοδοσίας: "
        label=tk.Label(mainFrame,text=message,bg="#1b2135",fg="#bdbcb9",font=("Arial",16))
        label.place(relheight=0.1,relwidth=0.5,relx=0.0,rely=0.225)

        Date=tk.Label(mainFrame,text=value,bg="#fff",fg="#010101",font=("Arial",16))#Date of last paycheck
        Date.place(relheight=0.05,relwidth=0.2,relx=0.475,rely=0.25)

        label=tk.Label(mainFrame,text="Αναλυτικά",bg="#1b2135",fg="#fff",font=("Arial",20))
        label.place(relheight=0.1,relwidth=0.4,relx=0.3,rely=0.3)

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.075,relwidth=0.85,relx=0.05,rely=0.4)
        label=tk.Label(labelFrame,text="Μέρος από Ημερήσιες Αποδοχές:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.place(relheight=1,relwidth=0.6)
        label=tk.Label(labelFrame,text=str(selected["Ημερήσιες Αποδοχές"].iloc[0]),fg="#010101",bg="#fff",font=("Arial",18))
        label.place(relheight=1,relwidth=0.4,relx=0.61)

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.075,relwidth=0.8,relx=0.05,rely=0.525)
        label=tk.Label(labelFrame,text="Μέρος από Ωριαίες Αποδοχές:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.place(relheight=1,relwidth=0.6)
        label=tk.Label(labelFrame,text=str(selected["Ωριαίες Αποδοχές"].iloc[0]),fg="#010101",bg="#fff",font=("Arial",18))
        label.place(relheight=1,relwidth=0.4,relx=0.61)

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.075,relwidth=0.6,relx=0.05,rely=0.65)
        label=tk.Label(labelFrame,text="Μέρος από Bonus:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.place(relheight=1,relwidth=0.5)
        label=tk.Label(labelFrame,text=str(selected["Bonus"].iloc[0]),fg="#010101",bg="#fff",font=("Arial",18))
        label.place(relheight=1,relwidth=0.3,relx=0.61)
      
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.075,relwidth=0.6,relx=0.05,rely=0.775)
        label=tk.Label(labelFrame,text="Σύνολο:",bg="#1b2135",fg="#fff",font=("Arial",18,"bold"))
        label.place(relheight=1,relwidth=0.5)
        self.final=tk.Label(labelFrame,text=str(int(selected["Ωριαίες Αποδοχές"].iloc[0])+int(selected["Bonus"].iloc[0])+int(selected["Ημερήσιες Αποδοχές"].iloc[0])),fg="#010101",bg="#fff",font=("Arial",18),anchor="w")
        self.final.place(relheight=1,relwidth=0.5,relx=0.4)

        self.root.protocol("WM_DELETE_WINDOW",self.exit)
        self.root.mainloop()

class editCoach(tk.Frame):
    def __init__(self,master,coach,choice):
        self.master=master
        self.coach=coach
        self.choice=choice
        self.root=tk.Toplevel(self.master.root)
        self.root.title("Δημιουργία Μισθοδοτούμενου")
        self.master.w_c["Edit"]=self.root
        topCanvas=tk.Canvas(self.root,height=1000,width=900,bg="#1b2135")
        topCanvas.pack()
        mainFrame=tk.Frame(topCanvas,bg="#1b2135")
        mainFrame.place(relheight=1,relwidth=1)
        self.entries={}
        self.widget={}

        message="Τα Στοιχεία του Μισθοδοτούμενου"
        label=tk.Label(mainFrame,bg="#1b2135",text=message,font=("Arial",24),fg="#bdbcb9")
        label.place(relheigh=0.125,relwidth=0.9,relx=0.05,rely=0.025)
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.1)
        label=tk.Label(labelFrame,text="Επώνυμο",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set(self.choice[0])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Επώνυμο"]=textVar
        self.widget["Επώνυμο"]=entry


        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.1)
        label=tk.Label(labelFrame,text="Όνομα",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set(self.choice[1])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Όνομα"]=textVar
        self.widget["Όνομα"]=entry

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.3)
        label=tk.Label(labelFrame,text="Σταθερό",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set(self.coach.loc[self.choice,"Σταθερό"].iloc[0])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Σταθερό"]=textVar
        self.widget["Σταθερό"]=entry

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.3)
        label=tk.Label(labelFrame,text="Κινητό",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set(self.coach.loc[self.choice,"Κινητό"].iloc[0])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Κινητό"]=textVar
        self.widget["Κινητό"]=entry


        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.5)
        label=tk.Label(labelFrame,text="Email",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set(self.coach.loc[self.choice,"Email"].iloc[0])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Email"]=textVar
        self.widget["Email"]=entry

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.5)
        label=tk.Label(labelFrame,text="Διεύθυνση",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set(self.coach.loc[self.choice,"Διεύθυνση"].iloc[0])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Διεύθυνση"]=textVar
        self.widget["Διεύθυνση"]=entry

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.175,relwidth=0.4,relx=0.3,rely=0.7)
        label=tk.Label(labelFrame,text="Ημερομηνία Δημιουργίας",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set(self.coach.loc[self.choice,"Ημερομηνία Δημιουργίας"].iloc[0])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Ημερομηνία Δημιουργίας"]=textVar
        self.widget["Ημερομηνία Δημιουργίας"]=entry


        editButton=tk.Button(mainFrame,text="Επεξεργασία",command=self.enable,bg="#bec1c4",font=('Arial',18))
        editButton.place(relheight=0.075,relwidth=0.4,relx=0.05,rely=0.9)
        doneButton=tk.Button(mainFrame,text="Ολοκλήρωση",command=self.complete,bg="#bec1c4",font=('Arial',18))
        doneButton.place(relheight=0.075,relwidth=0.4,relx=0.55,rely=0.9)

        self.root.protocol("WM_DELETE_WINDOW",self.exit)
        self.root.mainloop()

    def exit(self):
        self.master.w_c["Edit"]=""
        self.root.destroy()
    def complete(self):
        data={}
        for i in self.entries:
            data[i]=self.entries[i].get() if self.entries[i].get()!=""else "-"
        if data["Όνομα"]=="-" or  data["Επώνυμο"]=="-":
            mb.showinfo("Σφάλμα Εισόδου","Για να ολοκληρωθεί η δημιουργία του μισθοδοτούμενου πρέπει να δωθεί το όνομα και το επώνυμο του.")
        else:
            self.coach=self.coach.reset_index()
            ind=self.coach[(self.coach["Επώνυμο"].str.match(self.choice[0]))&(self.coach["Όνομα"].str.match(self.choice[1]))].index[0]
            for i in data:
                self.coach.loc[ind,i]=data[i]
            self.exit()
            self.coach=self.coach.set_index(["Επώνυμο","Όνομα"])
            pg.writeCoaches(self.coach)
            self.master.redraw()
    def enable(self):
        for i in self.widget:
            self.widget[i]['state']=tk.NORMAL
class createCoach(tk.Frame):
    def __init__(self,master,coach,choice=None):
        self.master=master
        self.coach=coach
        self.choice=choice
        self.root=tk.Toplevel(self.master.root)
        self.master.w_c["Create"]=self.root
        self.root.title("Δημιουργία Μισθοδοτούμενου")
        topCanvas=tk.Canvas(self.root,height=1000,width=900,bg="#1b2135")
        topCanvas.pack()
        mainFrame=tk.Frame(topCanvas,bg="#1b2135")
        mainFrame.place(relheight=1,relwidth=1)
        self.entries={}


        message="Παρακαλώ δώστε τα Στοιχεία του Νέου Μισθοδωτούμενου"
        label=tk.Label(mainFrame,bg="#1b2135",text=message,font=("Arial",24),fg="#bdbcb9")
        label.place(relheigh=0.125,relwidth=0.9,relx=0.05,rely=0.025)
        message="(Υπενθύμηση:Κατα την Δημιουργία του δεν θα έχει Μισθοδοτικά Στοιχεία)"
        label=tk.Label(mainFrame,bg="#1b2135",text=message,font=("Arial",16),fg="#bdbcb9")
        label.place(relheigh=0.05,relwidth=0.9,relx=0.05,rely=0.115)
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.175)
        label=tk.Label(labelFrame,text="Επώνυμο",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set("" if self.choice==None else self.coach.loc[self.choice,"Επώνυμο"])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Επώνυμο"]=textVar

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.175)
        label=tk.Label(labelFrame,text="Όνομα",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set("" if self.choice==None else self.coach.loc[self.choice,"Όνομα"])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Όνομα"]=textVar

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.375)
        label=tk.Label(labelFrame,text="Σταθερό",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set("" if self.choice==None else self.coach.loc[self.choice,"Σταθερό"])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Σταθερό"]=textVar

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.375)
        label=tk.Label(labelFrame,text="Κινητό",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set("" if self.choice==None else self.coach.loc[self.choice,"Κινητό"])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Κινητό"]=textVar

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.575)
        label=tk.Label(labelFrame,text="Email",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set("" if self.choice==None else self.coach.loc[self.choice,"Email"])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Email"]=textVar

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.575)
        label=tk.Label(labelFrame,text="Διεύθυνση",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set("" if self.choice==None else self.coach.loc[self.choice,"Διεύθυνση"])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Διεύθυνση"]=textVar


        doneButton=tk.Button(mainFrame,text="Ολοκλήρωση",command=self.complete,bg="#bec1c4",font=('Arial',18))
        doneButton.place(relheight=0.075,relwidth=0.9,relx=0.05,rely=0.9)

        self.root.protocol("WM_WINDOW_DESTROY",self.exit)
        self.root.mainloop()

    def exit(self):
        self.master.w_c["Create"]=self.root
        self.root.destroy()
    def complete(self):
        data={"Τελευταία Μισθοδοσία":pd.to_datetime("1/1/2020",dayfirst=True).to_period("D"),"Σύνολο":0,"Ημερήσιες Αποδοχές":0,"Bonus":0,"Ημερομηνία Δημιουργίας":pd.Timestamp.now().to_period("D")}
        for i in self.entries:
            data[i]=self.entries[i].get() if self.entries[i].get()!=""else "-"
        if data["Όνομα"]=="-" or  data["Επώνυμο"]=="-":
            mb.showinfo("Σφάλμα Εισόδου","Για να ολοκληρωθεί η δημιουργία του μισθοδοτούμενου πρέπει να δωθεί το όνομα και το επώνυμο του.")
        else:
            self.exit()
            temp=pd.Series(data)
            self.coach=self.coach.reset_index().append(temp,ignore_index=True).set_index(["Επώνυμο","Όνομα"])
            pg.writeCoaches(self.coach)
            self.master.redraw()
    def enable(self):
        pass
class createMovement(tk.Frame):
    def __init__(self,root,window,notes):
        self.master=window
        self.window=root
        self.notes=notes
        self.root=tk.Toplevel(self.master)
        self.root.title("Δήλωση Οικονομικού Γεγονότος")
        self.window.w_c["Create"]=self.root
        createCanvas=tk.Canvas(self.root,bg="#1b2135",height=800,width=800)
        createCanvas.pack()
        mainFrame=tk.Frame(createCanvas,bg="#1b2135")
        mainFrame.place(relheight=1,relwidth=1)

        self.entries={}
        label=tk.Label(mainFrame,text="Εισάγετε τα Δεδομένα για τον Ορισμό του Οικονομικού Γεγονότος",bg="#1b2135",fg="#bdbcb9",font=('Arial',18))
        label.place(relheight=0.1,relwidth=0.9,relx=0.05,rely=0.025)
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.125)
        label=tk.Label(labelFrame,text="Όνομα",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set("")
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Όνομα"]=textVar

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.125)
        label=tk.Label(labelFrame,text="Τύπος",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        values=["Επιλέξτε τον τύπο\n της κίνησης",
                "Συνδρομή",
                "Εγγραφή",
                "Πώληση προωθητικού\n Υλικού",
                "Χορηγίες",
                "Διαφήμιση Εμφανίσεων",
                "Διαφήμιση Χώρων",
                "Εκδηλώσεις",
                "Τουρνουά Βόλλευ",
                "Πώληση Παικτών/ριών",
                "Επιστροφή ΦΠΑ"]
        self.typeVar=tk.StringVar()
        self.typeVar.set(values[0])
        self.typeEntry=tk.OptionMenu(labelFrame,self.typeVar,*values)
        self.typeEntry.config(font=('Arial',18))
        self.typeEntry["menu"].config(font=('Arial',18))
        self.typeEntry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Τύπος"]=self.typeVar

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.325)
        label=tk.Label(labelFrame,text="Ποσό",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set("")
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Ποσό"]=textVar

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.325)
        label=tk.Label(labelFrame,text="Είδος",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        values=["Έσοδο",
                "Έξοδο"]
        textVar=tk.StringVar()
        textVar.set(values[0])
        entry=tk.OptionMenu(labelFrame,textVar,*values,command=lambda choice: self.modifyChoices(True if choice=="Έσοδο" else False))
        entry.config(font=('Arial',18))
        entry["menu"].config(font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Είδος"]=textVar

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.3,relwidth=0.9,relx=0.05,rely=0.55)
        label=tk.Label(labelFrame,text="Αιτιολογία",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.2,relwidth=1)
        entry=tk.Text(labelFrame,height=4,font=('Arial',18))
        entry.insert(tk.INSERT,"")
        entry.place(relheight=0.8,relwidth=1,rely=0.2)
        self.entries["Αιτιολογία"]=entry

        doneButton=tk.Button(mainFrame,text="Ολοκλήρωση",command=self.complete,bg="#bec1c4",font=('Arial',18))
        doneButton.place(relheight=0.075,relwidth=0.9,relx=0.05,rely=0.9)

        self.root.protocol("WM_DELETE_WINDOW",func=self.exit)
        self.root.mainloop()
    def exit(self):
        self.window.w_c["Create"]=""
        self.root.destroy()
    def modifyChoices(self,Income):
        if Income:
            values=["Επιλέξτε τον τύπο\n της κίνησης"
                "Συνδρομή",
                "Εγγραφή",
                "Πώληση προωθητικού Υλικού",
                "Χορηγίες",
                "Διαφήμιση Εμφανίσεων",
                "Διαφήμιση Χώρων",
                "Εκδηλώσεις",
                "Τουρνουά Βόλλευ",
                "Πώληση Παικτών /ριών",
                "Επιστροφή ΦΠΑ"]
        else:
            values=["Επιλέξτε τον τύπο\n της κίνησης",
                "Μισθοδοσία",
                "Προμήθεια Ρουχισμού",
                "Αθλητικό Υλικό",
                "Διαιτητές",
                "Τέλος συμμετοχής",
                "Αναλώσιμα",
                "Οδοιπορικά",
                "Διαφημιστικό και\n Προωθητικο υλικο",
                "Φαρμακευτικο Υλ.",
                "Ιατρικές Συνεργασίες"]
        self.typeVar.set("")
        self.typeEntry["menu"].delete(0,'end')
        for column in values:
            self.typeEntry["menu"].add_command(label=column,command=lambda value=column: self.typeVar.set(value))
        self.typeVar.set("Επιλέξτε τον τύπο\n της κίνησης")
    def complete(self):
        data={"Ημερομηνία":pd.Period.now("D"),"Ιδιωτικό":False}
        for i in self.entries:
            if i=="Είδος":
                try:
                    data["Έσοδο"]=int(self.entries["Ποσό"].get()) if self.entries[i].get()=="Έσοδο" else 0
                    data["Έξοδο"]=int(self.entries["Ποσό"].get()) if self.entries[i].get()=="Έξοδο" else 0
                except ValueError:
                    mb.showinfo("Λάθος Είσοδος","Στο πεδίο ποσό πρέπει να αναγραφεί το ποσό του γεγονότος, το οποίο είναι ένας ακέραιος αριθμός.")
            elif i!="Αιτιολογία":
                data[i]=self.entries[i].get()
            else:
                data[i]=self.entries[i].get("1.0","end-1c") if self.entries[i].get("1.0","end-1c") else ""
        if data["Όνομα"]!="" and data["Τύπος"]!="Επιλέξτε τον τύπο\n της κίνησης":
            temp=pd.Series(data)
            self.notes["Ποσό"].iloc[0]+=data["Έσοδο"]-data["Έξοδο"]
            self.notes=self.notes.append(temp,ignore_index=True)
            pg.writeCalendar(self.notes)
            self.exit()
            self.window.redraw()
        else:
            mb.showinfo("Ελλειπή Δεδομένα","Για να ολοκληρωθεί η δημιουργία της κίνησης θα πρέπει να δωθούν απαραίτητα\n τιμές στα πεδία Ονομα και Τύπος.")

class EditMovement(tk.Frame):
    def __init__(self,root,indi,notes):
        self.master=root
        self.choice=indi
        self.notes=notes
        self.root=tk.Toplevel(self.master.root)
        self.master.w_c["Edit"]=self.root
        createCanvas=tk.Canvas(self.root,bg="#1b2135",height=800,width=800)
        createCanvas.pack()
        mainFrame=tk.Frame(createCanvas,bg="#1b2135")
        mainFrame.place(relheight=1,relwidth=1)
        self.widgets={}
        self.entries={}
        label=tk.Label(mainFrame,text="Εδώ μπορείτε να Εξετάσετε και να Επεξεργαστήτε\nτα Οικονομικά δεδομένα",bg="#1b2135",fg="#bdbcb9",font=('Arial',18))
        label.place(relheight=0.1,relwidth=0.9,relx=0.05,rely=0.025)
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.125)
        label=tk.Label(labelFrame,text="Όνομα",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set(self.notes.loc[self.choice,"Όνομα"])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry["state"]=tk.DISABLED
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Όνομα"]=textVar
        self.widgets["Όνομα"]=entry

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.125)
        label=tk.Label(labelFrame,text="Τύπος",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        values=["Επιλέξτε τον τύπο\n της κίνησης",
                "Συνδρομή",
                "Εγγραφή",
                "Πώληση προωθητικού\n Υλικού",
                "Χορηγίες",
                "Διαφήμιση Εμφανίσεων",
                "Διαφήμιση Χώρων",
                "Εκδηλώσεις",
                "Τουρνουά Βόλλευ",
                "Πώληση Παικτών/ριών",
                "Επιστροφή ΦΠΑ"]
        self.typeVar=tk.StringVar()
        self.typeVar.set(self.notes.loc[self.choice,"Τύπος"])
        self.typeEntry=tk.OptionMenu(labelFrame,self.typeVar,*values)
        self.typeEntry.config(font=('Arial',18))
        self.typeEntry["menu"].config(font=('Arial',18))
        self.typeEntry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.typeEntry['state']=tk.DISABLED
        self.entries["Τύπος"]=self.typeVar
        self.widgets["Τύπος"]= self.typeEntry

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.05,rely=0.325)
        label=tk.Label(labelFrame,text="Ποσό",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        textVar=tk.StringVar()
        textVar.set(str(self.notes.loc[self.choice,"Ποσό"]))
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry['state']=tk.DISABLED
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        self.entries["Ποσό"]=textVar
        self.widgets["Ποσό"]=entry

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.2,relwidth=0.4,relx=0.55,rely=0.325)
        label=tk.Label(labelFrame,text="Είδος",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.5,relwidth=1)
        values=["Έσοδο",
                "Έξοδο"]
        textVar=tk.StringVar()
        entry=tk.OptionMenu(labelFrame,textVar,*values,command=lambda choice: self.modifyChoices(True if choice=="Έσοδo" else False,self.typeEntry.get()))
        entry.config(font=('Arial',18))
        entry["menu"].config(font=('Arial',18))
        textVar.set("Έσοδο" if self.notes.loc[self.choice,"Έσοδο"]!=0 else "Έξοδο")
        self.modifyChoices(True if textVar.get()=="Έσοδο" else False,preset=self.notes.loc[self.choice,"Τύπος"])
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Είδος"]=textVar
        self.widgets["Είδος"]=entry

        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.place(relheight=0.3,relwidth=0.9,relx=0.05,rely=0.55)
        label=tk.Label(labelFrame,text="Αιτιολογία",bg="#1b2135",fg="#fff",font=('Arial',18))
        label.place(relheight=0.2,relwidth=1)
        entry=tk.Text(labelFrame,height=4,font=('Arial',18))
        entry.insert(tk.INSERT,self.notes.loc[self.choice,"Αιτιολογία"])
        entry["state"]=tk.DISABLED
        entry.place(relheight=0.8,relwidth=1,rely=0.2)
        self.entries["Αιτιολογία"]=entry
        self.widgets["Αιτιολογία"]=entry

        doneButton=tk.Button(mainFrame,text="Ολοκλήρωση",command=self.complete,bg="#bec1c4",font=('Arial',18))
        doneButton.place(relheight=0.075,relwidth=0.4,relx=0.55,rely=0.9)

        editButton=tk.Button(mainFrame,text="Επεξεργασία",command=self.enable,bg="#bec1c4",font=('Arial',18))
        editButton.place(relheight=0.075,relwidth=0.4,relx=0.05,rely=0.9)

        self.root.protocol("WM_DELETE_WINDOW",self.exit)
        self.root.mainloop()
    def complete(self):
        self.notes["Ποσό"].iloc[0]+=self.notes.loc[self.choice,"Έξοδο"]-self.notes.loc[self.choice,"Έσοδο"]
        for i in self.entries:
            if i=="Είδος":
                try:
                    self.notes.loc[self.choice,"Έσοδο"]=int(self.entries["Ποσό"].get()) if self.entries[i].get()=="Έσοδο" else 0
                    self.notes.loc[self.choice,"Έξοδο"]=int(self.entries["Ποσό"].get()) if self.entries[i].get()=="Έξοδο" else 0
                except ValueError:
                    mb.showinfo("Λάθος Είσοδος","Στο πεδίο ποσό πρέπει να αναγραφεί το ποσό του γεγονότος, το οποίο είναι ένας ακέραιος αριθμός.")
            elif i!="Αιτιολογία":
                self.notes.loc[self.choice,i]=self.entries[i].get()
            else:
                self.notes.loc[self.choice,i]=self.entries[i].get("1.0","end-1c")
        self.notes["Ποσό"].iloc[0]+=self.notes.loc[self.choice,"Έσοδο"]-self.notes.loc[self.choice,"Έξοδο"]
        pg.writeCalendar(self.notes)
        self.exit()
        self.master.redraw()
    def modifyChoices(self,Income,preset=None):
        if Income:
            values=["Επιλέξτε τον τύπο\n της κίνησης"
                "Συνδρομή",
                "Εγγραφή",
                "Πώληση προωθητικού Υλικού",
                "Χορηγίες",
                "Διαφήμιση Εμφανίσεων",
                "Διαφήμιση Χώρων",
                "Εκδηλώσεις",
                "Τουρνουά Βόλλευ",
                "Πώληση Παικτών /ριών",
                "Επιστροφή ΦΠΑ"]
        else:
            values=["Επιλέξτε τον τύπο\n της κίνησης",
                "Μισθοδοσία",
                "Προμήθεια Ρουχισμού",
                "Αθλητικό Υλικό",
                "Διαιτητές",
                "Τέλος συμμετοχής",
                "Αναλώσιμα",
                "Οδοιπορικά",
                "Διαφημιστικό και\n Προωθητικο υλικο",
                "Φαρμακευτικο Υλ.",
                "Ιατρικές Συνεργασίες"]
        self.typeVar.set("")
        self.typeEntry["menu"].delete(0,'end')
        for column in values:
            self.typeEntry["menu"].add_command(label=column,command=lambda value=column: self.typeVar.set(value))
        if preset==None:
            self.typeVar.set("Επιλέξτε τον τύπο\n της κίνησης")
        else:
            self.typeVar.set(preset)
    def enable(self):
        for i in self.widgets:
            self.widgets[i]["state"]=tk.NORMAL
    def exit(self):
        self.master.w_c["Edit"]=""
        self.root.destroy()

