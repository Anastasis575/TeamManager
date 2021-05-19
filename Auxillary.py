from typing import Tuple

from pandas._libs.tslibs import Timestamp
import ClubPage as pg
import OperationFunctions as of
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import tkinter.messagebox as mb
import pandas as pd
import numpy as np

class viewDetails(tk.Frame):
    def __init__(self,master,coach: pd.DataFrame,salaries: pd.DataFrame,choice: Tuple):
        self.master=master
        self.coach=coach
        self.salaries=salaries
        self.choice=choice
        # Reduce the dataframe to just the part that contains the selected coach
        reduced=self.salaries.where((self.salaries["Όνομα"].str.contains(self.choice[1]))&(self.salaries["Επώνυμο"].str.contains(self.choice[0]))).dropna()
        if len(reduced)<1:
            # If there are no entries on this coach 
            mb.showwarning("Ενημέρωση","μισθοδοτούμενος δεν έχει μισθοδωσίες")
            return 
        elif len(reduced)==1:
            # If there is only one entry of a wage for this certain coach
            # Define the the last date the coach was payed
            # Isolate the latest instanse of the coach's payment and it's index
            self.lastDate=reduced["Ημερομηνία"].iloc[0]
            self.TrueCoach=reduced[reduced["Ημερομηνία"]==self.lastDate]
            self.index=self.TrueCoach.index
        else:
            # Define the the most recent date of the coach's wage registration
            self.lastDate=reduced["Ημερομηνία"].max()
            self.TrueCoach=reduced[reduced["Ημερομηνία"]==self.lastDate]
        # If between the last wage and today the month has changed, a new wage is created
        self.createCondition=len(pd.date_range(start=self.lastDate,end=pd.Timestamp.now(),freq="MS"))!=0
        self.root=tk.Toplevel(self.master.root,bg="#1b2135")
        self.master.w_c["EditSalary"]=self.root
        self.root.title("Στοιχεία Μισθοδοσίας")
        self.root.geometry("700x750")
        mainFrame=tk.Frame(self.root,bg="#1b2135")
        mainFrame.place(relwidth=1,relheight=1)
        # Intro Information
        tk.Label(mainFrame,text="Μισθοδοτικά στοιχεία",bg="#1b2135",fg="#fff",font=("Arial",28)).pack(fill=tk.X,anchor=tk.N)#.place(relwidth=1,relheight=0.1)
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(fill=tk.X,pady=15)
        # Defines whom the wage is addreshed
        tk.Label(labelFrame,text="Tου μισθοδοτούμενου: {} {}".format(self.choice[0],self.choice[1]),bg="#1b2135",fg="#fff",font=("Arial",16)).pack()
        smallframe=tk.Frame(labelFrame,bg="#1b2135")
        smallframe.pack()
        # The date of this month's wage creation or the today's date if no wage info exist for this month
        tk.Label(smallframe,text="Ημερομηνία:".format(self.choice[0],self.choice[1]),bg="#1b2135",fg="#fff",font=("Arial",16)).pack(side=tk.LEFT,anchor=tk.CENTER,padx=105,fill=tk.X)
        option=[str(frame["Ημερομηνία"].iloc[0].to_period("D")) for group,frame in reduced.groupby(level=0)]
        if self.createCondition  and self.lastDate!=pd.to_datetime("1-1-2020"):
            option.append(str(pd.Timestamp.now().to_period("D")))
        if len(option)>1:
            option.sort(key=lambda x:pd.to_datetime(x),reverse=True)
        self.dateStr=tk.StringVar()
        self.dateStr.set(option[0])
        op=tk.OptionMenu(smallframe,self.dateStr,option[0],*option,command=lambda value: self.PastSalary(value))
        op.config(font=("Arial",16))
        op["menu"].config(font=("Arial",16))
        op.pack(side=tk.LEFT,anchor=tk.CENTER,padx=75,fill=tk.X)
        
        # Add Data 
        tk.Label(mainFrame,text="Αναλυτικά",bg="#1b2135",fg="#fff",font=("Arial",20)).pack()

        # Daily wage info
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(padx=25,pady=20,fill=tk.X)
        label=tk.Label(labelFrame,text="Μέρος από Ημερήσιες Αποδοχές:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.pack(anchor=tk.NW)
        self.dailyVar=tk.StringVar()
        self.dailyVar.set(float(self.TrueCoach["Ημερήσιες Αποδοχές"].iloc[0]) if not self.createCondition else 0)
        self.dailyentry=tk.Entry(labelFrame,textvariable=self.dailyVar,bg="#fff",font=("Arial",18))
        self.dailyentry.pack(side=tk.LEFT,fill=tk.X)
        self.dailyentry["state"]=tk.DISABLED

        # Hourly wage info
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(padx=25,pady=20,fill=tk.X)
        label=tk.Label(labelFrame,text="Μέρος από Ωριαίες Αποδοχές:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.pack(anchor=tk.NW)
        self.hourlyVar=tk.StringVar()
        self.hourlyVar.set(float(self.TrueCoach["Ωριαίες Αποδοχές"].iloc[0])if not self.createCondition else 0)
        self.hourlyentry=tk.Entry(labelFrame,textvariable=self.hourlyVar,bg="#fff",font=("Arial",18))
        self.hourlyentry.pack(side=tk.LEFT,fill=tk.X)
        self.hourlyentry["state"]=tk.DISABLED

        # Other Bonus wage info
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(padx=25,pady=20,fill=tk.X)
        label=tk.Label(labelFrame,text="Μέρος από Bonus:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.pack(anchor=tk.NW)
        self.bonusVar=tk.StringVar()
        self.bonusVar.set(float(self.TrueCoach["Bonus"].iloc[0]) if not self.createCondition else 0)
        self.bonusentry=tk.Entry(labelFrame,textvariable=self.bonusVar,bg="#fff",font=("Arial",18))
        self.bonusentry.pack(side=tk.LEFT,fill=tk.X)
        self.bonusentry["state"]=tk.DISABLED


        # Total
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(padx=25,pady=20,fill=tk.X)
        label=tk.Label(labelFrame,text="Σύνολο:",bg="#1b2135",fg="#fff",font=("Arial",18,"bold"))
        label.pack(anchor=tk.NW)
        self.final=tk.Label(labelFrame,text=str(int(float(self.hourlyVar.get()))+int(float(self.bonusVar.get()))+int(float(self.dailyVar.get())))+"\t\t",fg="#010101",bg="#fff",font=("Arial",18),anchor="w")
        self.final.pack(side=tk.LEFT,fill=tk.X)

        # Control Buttons
        buttonFrame=tk.Frame(mainFrame,bg="#1b2135")
        buttonFrame.pack(side=tk.BOTTOM,anchor=tk.S,fill=tk.X, expand=True)
        tk.Button(buttonFrame,text="Επεξεργασία",command=self.enable,bg="#bec1c4",font=('Arial',18)).pack(padx=75,expand=True,side=tk.LEFT,anchor=tk.N)
        self.doneButton=tk.Button(buttonFrame,text="Ολοκλήρωση",command=self.complete,bg="#bec1c4",font=('Arial',18))
        self.doneButton.pack(padx=75,expand=True,side=tk.LEFT,anchor=tk.N)
        self.doneButton["state"]=tk.DISABLED
        tk.Label(buttonFrame,text="\t\t\t\t",bg="#1b2135",fg="#1b2135").pack(fill=tk.X,expand=True)

        self.root.protocol("WM_DELETE_WINDOW",self.exit)
        self.root.mainloop()

    def exit(self):
        ''' Method to safely exit the window
        '''
        self.master.w_c["EditSalary"]=""
        self.root.destroy()

    def enable(self):
        """Enables the Entry Widgets and allows them to be interacted with.
        """
        self.dailyentry["state"]=tk.NORMAL
        self.hourlyentry["state"]=tk.NORMAL
        self.bonusentry["state"]=tk.NORMAL
        self.doneButton["state"]=tk.NORMAL

    def complete(self):
        """Corrects the data and saves it in the excel.
        """
        try:
            # If the wage in the window represents an update event
            if not self.createCondition or self.lastDate==pd.to_datetime("1-1-2020"):
                self.salaries.loc[self.TrueCoach.index,"Ημερήσιες Αποδοχές"]=float(self.dailyVar.get())
                self.salaries.loc[self.TrueCoach.index,"Ωριαίες Αποδοχές"]=float(self.hourlyVar.get())
                self.salaries.loc[self.TrueCoach.index,"Bonus"]=float(self.bonusVar.get())
                self.salaries.loc[self.TrueCoach.index,"Σύνολο"]=float(self.dailyVar.get())+float(self.hourlyVar.get())+float(self.bonusVar.get())
                self.bonusVar.set(float(self.dailyVar.get())+float(self.hourlyVar.get())+float(self.bonusVar.get()))
                self.salaries.loc[self.TrueCoach.index,"Ημερομηνία"]=pd.Timestamp.now().to_period("D")
            else:
                temp=self.TrueCoach.copy()
                temp["Ημερήσιες Αποδοχές"]=float(self.dailyVar.get())
                temp["Ωριαίες Αποδοχές"]=float(self.hourlyVar.get())
                temp["Bonus"]=float(self.bonusVar.get())
                temp["Σύνολο"]=float(self.dailyVar.get())+float(self.hourlyVar.get())+float(self.bonusVar.get())
                temp["Τελευταία Μισθοδοσία"]=pd.Timestamp.now().to_period("D")
                temp["Ημερομηνία"]=pd.Timestamp.now()
                self.salaries=self.salaries.append(temp)
                self.salaries=self.salaries.reset_index().drop("Index",axis=1)
                self.salaries.index=self.salaries.index.rename("Index")
            pg.writeSalaries(self.salaries)
            self.master.redraw()
        except ValueError:
            mb.showinfo("Λάθος Είσοδος","Στα πεδία αποδοχών πρέπει να αναγραφεί το ποσό της αποδοχής, το οποίο είναι ένας ακέραιος αριθμός.")
    def PastSalary(self,value):
        #self.Past.set(self.lastDate)
        if len(pd.date_range(start=self.dateStr.get(),end=Timestamp.today(),freq="MS"))<1:
            return
        reduced=self.salaries.where((self.salaries["Όνομα"].str.contains(self.choice[1]))&(self.salaries["Επώνυμο"].str.contains(self.choice[0]))).dropna()
        selected=reduced.where((reduced["Ημερομηνία"]==pd.to_datetime(self.dateStr.get()))).dropna()
        miniroot=tk.Toplevel(self.root,bg="#1b2135")
        miniroot.title("Μισθοδωσία {}".format(value))
        miniroot.resizable(True,True)
        miniroot.geometry("700x750")
        mainFrame=tk.Frame(miniroot,bg="#1b2135")
        mainFrame.place(relheight=1,relwidth=1)
         # Intro Information
        tk.Label(mainFrame,text="Μισθοδοτικά στοιχεία",bg="#1b2135",fg="#fff",font=("Arial",28)).pack(fill=tk.X,anchor=tk.N)#.place(relwidth=1,relheight=0.1)
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(fill=tk.X,pady=15)
        # Defines whom the wage is addreshed
        tk.Label(labelFrame,text="Tου μισθοδοτούμενου: {} {}".format(self.choice[0],self.choice[1]),bg="#1b2135",fg="#fff",font=("Arial",16)).pack()
        smallframe=tk.Frame(labelFrame,bg="#1b2135")
        smallframe.pack()
        # The date of this month's wage creation or the today's date if no wage info exist for this month
        tk.Label(smallframe,text="Ημερομηνία:",bg="#1b2135",fg="#fff",font=("Arial",16)).pack(side=tk.LEFT,anchor=tk.CENTER,padx=105,fill=tk.X)
        tk.Label(smallframe,text=value,bg="#fff",fg="#010101",font=("Arial",16)).pack(side=tk.LEFT,anchor=tk.CENTER,padx=55,fill=tk.X)#Date of last paycheck

        tk.Label(mainFrame,text="Αναλυτικά",bg="#1b2135",fg="#fff",font=("Arial",20)).pack()

        # Daily wage info
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(padx=25,pady=20,fill=tk.X)
        label=tk.Label(labelFrame,text="Μέρος από Ημερήσιες Αποδοχές:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.pack(anchor=tk.NW)
        self.dailyentry=tk.Label(labelFrame,text=str(selected["Ημερήσιες Αποδοχές"].iloc[0])+"\t\t",bg="#fff",font=("Arial",18)).pack(side=tk.LEFT,fill=tk.X)


        # Hourly wage info
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(padx=25,pady=20,fill=tk.X)
        label=tk.Label(labelFrame,text="Μέρος από Ωριαίες Αποδοχές:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.pack(anchor=tk.NW)
        self.hourlyentry=tk.Label(labelFrame,text=str(selected["Ωριαίες Αποδοχές"].iloc[0])+"\t\t",bg="#fff",font=("Arial",18)).pack(side=tk.LEFT,fill=tk.X)

        # Other Bonus wage info
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(padx=25,pady=20,fill=tk.X)
        label=tk.Label(labelFrame,text="Μέρος από Bonus:",fg="#fff",bg="#1b2135",font=("Arial",18))
        label.pack(anchor=tk.NW)
        self.bonusentry=tk.Label(labelFrame,text=str(selected["Bonus"].iloc[0])+"\t\t",bg="#fff",font=("Arial",18)).pack(side=tk.LEFT,fill=tk.X)


        # Total
        labelFrame=tk.Frame(mainFrame,bg="#1b2135")
        labelFrame.pack(padx=25,pady=20,fill=tk.X)
        label=tk.Label(labelFrame,text="Σύνολο:",bg="#1b2135",fg="#fff",font=("Arial",18,"bold"))
        label.pack(anchor=tk.NW)
        self.final=tk.Label(labelFrame,text=str(float(self.hourlyVar.get())+float(selected["Bonus"].iloc[0])+float(selected["Ημερήσιες Αποδοχές"].iloc[0]))+"\t\t",fg="#010101",bg="#fff",font=("Arial",18),anchor="w")
        self.final.pack(side=tk.LEFT,fill=tk.X)

        self.root.protocol("WM_DELETE_WINDOW",self.exit)
        self.root.mainloop()

class editCoach(tk.Frame):
    def __init__(self,master,coach,choice):
        self.master=master
        self.coach=coach
        self.choice=choice
        self.root=tk.Toplevel(self.master.root,bg="#1b2135")
        self.root.title("Δημιουργία Μισθοδοτούμενου")
        self.root.geometry("1000x900")
        self.root.resizable(True,True)
        self.master.w_c["Edit"]=self.root
        mainFrame=tk.Frame(self.root,bg="#1b2135")
        mainFrame.place(relheight=1,relwidth=1)
        self.entries={}
        self.widget={}

        message="Τα Στοιχεία του Μισθοδοτούμενου"
        label=tk.Label(mainFrame,bg="#1b2135",text=message,font=("Arial",24),fg="#bdbcb9")
        label.place(relheigh=0.125,relwidth=0.9,relx=0.05)
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
        textVar.set(self.coach.loc[self.choice,"Σταθερό"])
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
        textVar.set(self.coach.loc[self.choice,"Κινητό"])
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
        textVar.set(self.coach.loc[self.choice,"Email"])
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
        textVar.set(self.coach.loc[self.choice,"Διεύθυνση"])
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
        textVar.set(self.coach.loc[self.choice,"Ημερομηνία Δημιουργίας"].to_period("D"))
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Ημερομηνία Δημιουργίας"]=textVar
        #self.widget["Ημερομηνία Δημιουργίας"]=entry


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
            if data["Όνομα"]!=self.choice[1] or  data["Επώνυμο"]==self.choice[0]:
                salaries=pg.readSalaries()
                ids=[]
                for group,frame in salaries.groupby(level=0):
                    if frame.loc[group,"Όνομα"]==self.choice[1] and frame.loc[group,"Επώνυμο"]==self.choice[0]:
                        ids.append(group)
                for id in ids:
                    salaries.loc[id,"Όνομα"]=data["Όνομα"]
                    salaries.loc[id,"Επώνυμο"]=data["Επώνυμο"]
                pg.writeSalaries(salaries)
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
    def __init__(self,master,coach,salaries,choice=None):
        self.master=master
        self.coach=coach
        self.salaries=salaries
        self.choice=choice
        self.root=tk.Toplevel(self.master.root,bg="#1b2135")
        self.master.w_c["Create"]=self.root
        self.root.title("Δημιουργία Μισθοδοτούμενου")
        self.root.resizable(True,True)
        self.root.geometry("1000x900")
        mainFrame=tk.Frame(self.root,bg="#1b2135")
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
        data={"Ημερομηνία Δημιουργίας":pd.Timestamp.now()}
        for i in self.entries:
            data[i]=self.entries[i].get() if self.entries[i].get()!=""else "-"
        if data["Όνομα"]=="-" or  data["Επώνυμο"]=="-":
            mb.showinfo("Σφάλμα Εισόδου","Για να ολοκληρωθεί η δημιουργία του μισθοδοτούμενου πρέπει να δωθεί το όνομα και το επώνυμο του.")
        else:
            self.exit()
            temp=pd.Series(data)
            self.coach=self.coach.reset_index().append(temp,ignore_index=True).set_index(["Επώνυμο","Όνομα"])
            self.salaries=self.salaries.reset_index().drop("Index",axis=1)
            tempS={"Ημερομηνία":pd.to_datetime("1-1-2020"),
                    "Τελευταία Μισθοδοσία":pd.to_datetime("1-1-2020").to_period("D"),
                    "Ημερήσιες Αποδοχές":0,
                    "Ωριαίες Αποδοχές":0,
                    "Bonus":0,
                    "Σύνολο":0,
                    "Επώνυμο":data["Επώνυμο"],
                    "Όνομα":data["Όνομα"]}
            tempS=pd.Series(tempS)
            self.salaries=self.salaries.append(tempS,ignore_index=True)
            self.salaries.index=self.salaries.index.rename("Index")
            pg.writeSalaries(self.salaries)
            pg.writeCoaches(self.coach)
            self.master.redraw()
    def enable(self):
        pass
class createMovement(tk.Frame):
    def __init__(self,root,window,notes):
        self.master=window
        self.window=root
        self.notes=notes
        self.root=tk.Toplevel(self.master,bg="#1b2135")
        self.root.resizable(True,True)
        self.root.geometry("800x800")
        self.root.title("Δήλωση Οικονομικού Γεγονότος")
        self.window.w_c["Create"]=self.root
        mainFrame=tk.Frame(self.root,bg="#1b2135")
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
        self.root=tk.Toplevel(self.master.root,bg="#1b2135")
        self.root.geometry("800x800")
        self.root.resizable(True,True)
        self.master.w_c["Edit"]=self.root
        mainFrame=tk.Frame(self.root,bg="#1b2135")
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

