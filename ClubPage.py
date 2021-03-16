import OperationFunctions as of
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import tkinter.messagebox as mb
import pandas as pd
import numpy as np
import Auxillary as aux

notes=None
coaches=None

def readCalendar(first=False):
    notes=pd.read_excel("assets\\Calendar.xlsx")
    return notes


def writeCalendar(notes):
    notes.to_excel("assets\\Calendar.xlsx",columns=["Ημερομηνία","Όνομα","Τύπος","Ποσό","Έσοδο","Έξοδο","Αιτιολογία","Ιδιωτικό"])


def readCoaches(first=False):
    coaches=pd.read_excel("assets\\Coaches.xlsx",parse_dates=["Τελευταία Μισθοδοσία"])
    coaches["Τελευταία Μισθοδοσία"]=coaches["Τελευταία Μισθοδοσία"].apply(lambda x: x.to_period("D"))
    coaches=coaches.set_index(["Επώνυμο","Όνομα"])
    return coaches


def writeCoaches(coaches):
    for i in coaches.columns:
        if i!="Τελευταία Μισθοδοσία":
            coaches[i]=coaches[i].astype("str")
    coaches.to_excel("assets\\Coaches.xlsx")#,columns=["Επώνυμο","Όνομα","Σταθερό","Ποσό","Έσοδο","Έξοδο","Αιτιολογία","Ιδιωτικό"])


class Club(tk.Frame):
    def __init__(self,window,cha):
        self.window=window
        self.changes=cha
        self.notes=readCalendar()
        self.coaches=readCoaches()
        self.w_c={"Create":"",
                  "Edit":"",
                  "EditSalary":""}
        window.iconify()

        #Initialisation and main instance variables initialization
        self.root=tk.Toplevel(window)
        rootCanvas=tk.Canvas(self.root,height=1200,width=1400)
        rootCanvas.pack()
        super().__init__(self.root,bg="#4e73c2")
        super().place(relheight=1,relwidth=1)
        self.root.state("zoomed")

        #Two basic operational frames
        self.headerFrame = tk.Frame(self,bg="light grey")
        self.headerFrame.place(relwidth=0.8,relheight=0.35,relx=0.1,rely=0)

        self.subHeaderFrame=tk.Frame(self,bg="grey")
        self.subHeaderFrame.place(relwidth=0.8,relheight=0.65,relx=0.1,rely=0.35)

        #Esperos Emblem
        photo=ImageTk.PhotoImage(Image.open("assets\\Esperos.png").resize((350,350)))#Be Careful
        self.logo=tk.Label(self.headerFrame,image=photo,bg="light grey")
        self.logo.place(relheight=1,relwidth=0.3,relx=0,rely=0)

        #Window Title
        self.title=tk.Label(self.headerFrame,text="Στοιχεία Συλλόγου",bg="#c1c1c1")
        self.title.config(font=("Arial",36))
        self.title.place(relwidth=0.6,relheight=0.45,relx=0.3,rely=0)

        #Back Button
        backphoto=ImageTk.PhotoImage(Image.open("assets\\back.png").resize((75,75)))
        backButton=tk.Button(self.headerFrame,image=backphoto,command=self.goBack,bg="light grey",borderwidth=0)
        backButton.place(relheight=0.225,relwidth=0.05,relx=0.9,rely=0.7)

        #Forward Button
        forphoto=ImageTk.PhotoImage(Image.open("assets\\next.png").resize((75,75)))
        forwardButton=tk.Button(self.headerFrame,image=forphoto,command=self.goForward,bg="light grey",borderwidth=0)
        forwardButton.place(relheight=0.225,relwidth=0.05,relx=0.95,rely=0.7)

        values=["Επιλέξτε κάποια όψη",
                "Οικονομικές Κινήσεις",
                "Ταμείο Συλλόγου",
                "Μισθοδοσίες"]
        self.Variable=tk.StringVar()
        self.Variable.set(values[0])
        self.view=tk.OptionMenu(self.headerFrame,self.Variable,*values,command=self.chooseView)
        self.view.config(font=("Arial",18))
        self.view["menu"].config(font=("Arial",18))
        self.view.place(relwidth=0.3,relx=0.35,relheight=0.1,rely=0.75)

        options1=["Από"]
        self.rangeA=tk.StringVar()
        self.rangeA.set(options1[0])
        self.begin_time=tk.OptionMenu(self.headerFrame,self.rangeA,*options1,command=lambda value: self.rangeA.set(value))
        self.begin_time.config(font=("Arial",18))
        self.begin_time["menu"].config(font=("Arial",18))
        self.begin_time.place(relwidth=0.125,relx=0.5,relheight=0.1,rely=0.6)
        options2=["Μέχρι"]
        self.rangeB=tk.StringVar()
        self.rangeB.set(options2[0])
        self.end_time=tk.OptionMenu(self.headerFrame,self.rangeB,*options2,command=lambda value: self.rangeB.set(value))
        self.end_time.config(font=("Arial",18))
        self.end_time["menu"].config(font=("Arial",18))
        self.end_time.place(relwidth=0.125,relx=0.35,relheight=0.1,rely=0.6)
        #Main Content frame
        self.contentFrame=tk.Frame(self.subHeaderFrame,bg="#474a48")
        self.contentFrame.place(relheight=1,relwidth=0.7,relx=0.3)
        #movements=ttk.Treeview(contentFrame)

        #Athlete creation Button
        AthleteCreation=tk.Button(self.subHeaderFrame,text="Δεδομένα\nΜελών",command=self.initAthlete,bg="#494949",fg="#fff")
        AthleteCreation.config(font=("Arial",36))
        AthleteCreation.place(relwidth=0.25,relheight=0.2,relx=0.025,rely=0.05)

        languages={
            "January":"Ιανουάριος",
            "February":"Φεβρουάριος",
            "March":"Μάρτιος",
            "April":"Απρίλιος",
            "May":"Μάιος",
            "June":"Ιούνιος",
            "July":"Ιούλιος",
            "August":"Αύγουστος",
            "September":"Σεπτέμβριος",
            "October":"Οκτώβριος",
            "November":"Νοέμβριος",
            "December":"Δεκέμβριος",
            }
        #DropBar
        #self.dates=list(pd.date_range(pd.Timestamp.today()-pd.Timedelta(days=365),end=pd.Timestamp.today(),freq="MS"))
        #self.acronyms=[languages[i.month_name()] + " " + str(i.year) for i in self.dates]

        #self.search=ttk.Combobox(self.subHeaderFrame,value=self.acronyms,font=("Arial",18))
        #self.search.current(len(self.acronyms)-1)
        #self.search.bind("<<ComboboxSelected>>",self.chooseMonth)
        #self.search.place(relheight=0.1,relwidth=0.25,relx=0.025,rely=0.3)

        #Create Button
        self.Create=tk.Button(self.subHeaderFrame,text="Δημιουργία",command=self.createEntry,bg="#b4b8b5",font=("Arial",18))
        self.Create.place(relheight=0.1,relwidth=0.25,relx=0.025,rely=0.3)
        self.Create["state"]=tk.DISABLED
        #Delete Button
        self.Delete=tk.Button(self.subHeaderFrame,text="Διαγραφή",command=self.deleteEntry,bg="#b4b8b5",font=("Arial",18))
        self.Delete.place(relheight=0.1,relwidth=0.25,relx=0.025,rely=0.425)
        self.Delete["state"]=tk.DISABLED
        #Edit Button
        self.Edit=tk.Button(self.subHeaderFrame,text="Προβολή/Ενημέρωση",command=self.editEntry,bg="#b4b8b5",font=("Arial",18))
        self.Edit.place(relheight=0.1,relwidth=0.25,relx=0.025,rely=0.55)
        self.Edit["state"]=tk.DISABLED

        #Coach Salary Button
        self.Salary=tk.Button(self.subHeaderFrame,text="Λεπτομέρειες Μισθοδοσίας",command=self.viewSalary,bg="#b4b8b5",font=("Arial",18))
        self.Salary.place(relheight=0.1,relwidth=0.25,relx=0.025,rely=0.675)
        self.Salary["state"]=tk.DISABLED

        self.root.protocol("WM_DELETE_WINDOW",func=self.exit)
        self.root.mainloop()

    def redraw(self):
        self.root.destroy()
        init=Club(self.window,self.changes)

    def goBack(self):#Back command
        self.changes.moveBack(self.root,"Club")

    def goForward(self):#Forward command
        self.changes.moveForward(self.root,"Club")

    def exit(self):
        self.changes.clear()
        self.window.deiconify()
        self.root.destroy()
    def setStart(self):
        pass
    def setEnd(self):
        pass
    def initAthlete(self):
        if self.changes.peekType()=="Athletes":
            self.changes.moveBack(self.root,"Club")
        elif self.changes.peekType(1)=="Athletes":
            self.changes.moveForward(self.root,"Club")
        else:
            self.changes.addBack(self.root,"Club")
            init=of.Athletes(self.root,self.changes)


    def chooseView(self,value):
        self.Create["state"]=tk.DISABLED
        self.Delete["state"]=tk.DISABLED
        self.Edit["state"]=tk.DISABLED
        self.Salary["state"]=tk.DISABLED
        if self.Variable.get()=="Οικονομικές Κινήσεις":
            self.begin_time["state"]=tk.NORMAL
            self.end_time["state"]=tk.NORMAL
            self.rangeA.set("")
            self.begin_time["menu"].delete(0,'end')
            max=pd.to_datetime("1/1/2020")
            for column in self.notes["Ημερομηνία"].unique():
                temp=pd.to_datetime(column)
                max=max if temp<=max else temp
                self.begin_time["menu"].add_command(label=temp.to_period("D"),command=lambda value=temp.to_period("D"): self.set_date(value,"A"))
            self.rangeA.set(max.to_period("D"))
            self.rangeB.set("")
            self.end_time["menu"].delete(0,'end')
            max=pd.to_datetime("1/1/2020")
            for column in self.notes["Ημερομηνία"].unique():
                temp=pd.to_datetime(column)
                max=max if temp<=max else temp
                self.end_time["menu"].add_command(label=temp.to_period("D"),command=lambda value=temp.to_period("D"): self.set_date(value,"B"))
            self.rangeB.set(max.to_period("D"))
            #self.update(0)
            self.notes=readCalendar()
            self.Create["state"]=tk.NORMAL
            self.Delete["state"]=tk.NORMAL
            self.Edit["state"]=tk.NORMAL
            if len(self.contentFrame.winfo_children())!=0:
                for i in self.contentFrame.winfo_children():
                    i.destroy()
            self.movementScroll=ttk.Scrollbar(self.contentFrame)
            self.movementScroll.pack(side=tk.RIGHT,fill=tk.Y)

            style=ttk.Style()
            style.configure('Treeview', rowheight=40)
            style.configure("mystyle.Treeview",font=('Arial', 16)) # Modify the font of the body
            style.configure("mystyle.Treeview.Heading", font=('Arial', 18,'bold')) # Modify the font of the headings
            self.movements=ttk.Treeview(self.contentFrame,style="mystyle.Treeview",select=tk.EXTENDED,columns=["Ημερομηνία","Όνομα","Τύπος","Έσοδο","Έξοδο"],yscrollcommand=self.movementScroll.set)



            self.movements.column("#0",width=0,stretch=tk.NO)
            self.movements.column("Ημερομηνία",anchor=tk.CENTER,width=80)
            self.movements.column("Όνομα",anchor=tk.CENTER,width=220)
            self.movements.column("Τύπος",anchor=tk.CENTER,width=220)
            self.movements.column("Έσοδο",anchor=tk.CENTER,width=80)
            self.movements.column("Έξοδο",anchor=tk.CENTER,width=80)

            self.movements.heading("#0",text='',anchor=tk.W)
            self.movements.heading("Ημερομηνία",text="Ημερομηνία",anchor=tk.W)
            self.movements.heading("Όνομα",text="Όνομα",anchor=tk.W)
            self.movements.heading("Τύπος",text="Τύπος",anchor=tk.W)
            self.movements.heading("Έσοδο",text="Έσοδο",anchor=tk.W)
            self.movements.heading("Έξοδο",text="Έξοδο",anchor=tk.W)
            self.refreshMovements(0,self.rangeA.get(),self.rangeB.get())

            self.movements.pack(expand=True,fill=tk.BOTH)
            self.movementScroll.config(command=self.movements.yview)
        elif self.Variable.get()=="Ταμείο Συλλόγου":
            self.rangeA.set("")
            self.begin_time["menu"].delete(0,'end')
            self.begin_time["menu"].add_command(label="Από",command=lambda value="Από": self.rangeA.set("Από"))
            self.rangeA.set("Από")
            self.begin_time["state"]=tk.DISABLED
            self.rangeB.set("")
            self.end_time["menu"].delete(0,'end')
            self.end_time["menu"].add_command(label="Μέχρι",command=lambda value="Μέχρι": self.rangeB.set("Μέχρι"))
            self.end_time["state"]=tk.DISABLED
            self.rangeB.set("Μέχρι")
            if len(self.contentFrame.winfo_children())!=0:
               for i in self.contentFrame.winfo_children():
                   i.destroy()
            note=self.notes[self.notes["Ιδιωτικό"]==False]
            self.createReceipt(note,self.rangeA.get(),self.rangeB.get())
            #contentCanvas=tk.Canvas(self.contentFrame,bg="#474a48")
            #contentCanvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
            #contentScroll=ttk.Scrollbar(self.contentFrame,command=contentCanvas.yview)
            #contentScroll.pack(side=tk.RIGHT,fill=tk.Y)
            #contentCanvas.configure(yscrollcommand=contentScroll.set)
            #contentCanvas.bind("<Configure>",lambda e: contentCanvas.configure(scrollregion=contentCanvas.bbox("all")))
            #actualFrame=tk.Frame(self.contentFrame,bg="#474a48")
            #contentCanvas.create_window((0,0),window=actualFrame,anchor=tk.NW,)
            #label=tk.Label(actualFrame,text="Αναλυση Ταμείου Συλλόγου",bg="#474a48",fg="#fff",font=("Arial Black",22),justify=tk.CENTER)
            #label.pack()
            #revenue={}
            #cost={}
            #for i in note["Τύπος"].unique():
            #    temp=note[note["Τύπος"].str.match(i)]
            #    if temp["Έσοδο"].sum()!=0:
            #        revenue[i]=temp["Έσοδο"].sum()
            #    if temp["Έξοδο"].sum()!=0:
            #        cost[i]=temp["Έξοδο"].sum()
            #labelFrame=tk.Frame(actualFrame,bg="#474a48")
            #labelFrame.pack(fill=tk.X)
            #label=tk.Label(labelFrame,text="\nΕξόδα:",bg="#474a48",fg="#fff",font=("Arial",20),justify=tk.LEFT)
            #label.pack(fill=tk.X,side=tk.LEFT)
            #for content in cost:
            #    labelFrame=tk.Frame(actualFrame,bg="#474a48")
            #    labelFrame.pack(fill=tk.X)
            #    label=tk.Label(labelFrame,text=content+":",bg="#474a48",fg="#fff",font=("Arial",16),justify=tk.LEFT,width=15)
            #    label.pack(fill=tk.X,side=tk.LEFT)
            #    label=tk.Label(labelFrame,text=str(cost[content])+"€",bg="#474a48",fg="#fff",font=("Arial",16),justify=tk.LEFT)
            #    label.pack(fill=tk.X)
            #labelFrame=tk.Frame(actualFrame,bg="#474a48")
            #labelFrame.pack(fill=tk.X)
            #label=tk.Label(labelFrame,text="\nΕσόδα:",bg="#474a48",fg="#fff",font=("Arial",20),justify=tk.LEFT)
            #label.pack(fill=tk.X,side=tk.LEFT)
            #for content in revenue:
            #    labelFrame=tk.Frame(actualFrame,bg="#474a48")
            #    labelFrame.pack(fill=tk.X)
            #    label=tk.Label(labelFrame,text=content+":",bg="#474a48",fg="#fff",font=("Arial",16),justify=tk.LEFT,width=15)
            #    label.pack(fill=tk.X,side=tk.LEFT)
            #    label=tk.Label(labelFrame,text=str(revenue[content])+"€",bg="#474a48",fg="#fff",font=("Arial",16),justify=tk.LEFT)
            #    label.pack(fill=tk.X)
            #labelFrame=tk.Frame(actualFrame,bg="#474a48")
            #labelFrame.pack(fill=tk.X)
            #label=tk.Label(labelFrame,text="\n\nΣυνολικό Ταμείο: "+str(self.notes.iloc[0]["Ποσό"])+"€",bg="#474a48",fg="#fff",font=("Arial",20),justify=tk.CENTER)
            #label.pack(fill=tk.X,side=tk.LEFT)
        elif self.Variable.get()=="Μισθοδοσίες":
            self.coach=readCoaches()
            self.rangeA.set("")
            self.begin_time["menu"].delete(0,'end')
            self.begin_time["menu"].add_command(label="Από",command=lambda value="Από": self.rangeA.set("Από"))
            self.rangeA.set("Από")
            self.begin_time["state"]=tk.DISABLED
            self.rangeB.set("")
            self.end_time["menu"].delete(0,'end')
            self.end_time["menu"].add_command(label="Μέχρι",command=lambda value="Μέχρι": self.rangeB.set("Μέχρι"))
            self.end_time["state"]=tk.DISABLED
            self.rangeB.set("Μέχρι")
            self.Create["state"]=tk.NORMAL
            self.Delete["state"]=tk.NORMAL
            self.Edit["state"]=tk.NORMAL
            self.Salary["state"]=tk.NORMAL
            if len(self.contentFrame.winfo_children())!=0:
                for i in self.contentFrame.winfo_children():
                    i.destroy()
            self.salaryScroll=ttk.Scrollbar(self.contentFrame)
            self.salaryScroll.pack(side=tk.RIGHT,fill=tk.Y)
            now=pd.Timestamp.today()
            for group,frame in self.coaches.groupby(level=0):
                condition=len(list(pd.date_range(start=frame["Τελευταία Μισθοδοσία"].iloc[0].to_timestamp(freq="D"),end=now,freq="MS")))>0
                frame["Σύνολο"].iloc[0]=0 if condition else frame["Σύνολο"].iloc[0]
                frame["Ημερήσιες Αποδοχές"].iloc[0]=0 if condition else frame["Ημερήσιες Αποδοχές"].iloc[0]
                frame["Ωριαίες Αποδοχές"].iloc[0]=0 if condition else frame["Ωριαίες Αποδοχές"].iloc[0]
                frame["Bonus"].iloc[0]=0 if condition else frame["Bonus"].iloc[0]

            style=ttk.Style()
            style.configure("mystyle.Treeview",font=('Arial', 16)) # Modify the font of the body
            style.configure("mystyle.Treeview.Heading", font=('Arial', 18,'bold')) # Modify the font of the headings
            self.salary=ttk.Treeview(self.contentFrame,style="mystyle.Treeview",select=tk.EXTENDED,columns=["Τελευταία Μισθοδοσία","Όνομα","Επώνυμο","Σύνολο"],yscrollcommand=self.salaryScroll.set)



            self.salary.column("#0",width=0,stretch=tk.NO)
            self.salary.column("Τελευταία Μισθοδοσία",anchor=tk.CENTER,width=220)
            self.salary.column("Όνομα",anchor=tk.CENTER,width=180)
            self.salary.column("Επώνυμο",anchor=tk.CENTER,width=180)
            self.salary.column("Σύνολο",anchor=tk.CENTER,width=80)

            self.salary.heading("#0",text='',anchor=tk.W)
            self.salary.heading("Τελευταία Μισθοδοσία",text="Τελευταία Μισθοδοσία",anchor=tk.W)
            self.salary.heading("Όνομα",text="Όνομα",anchor=tk.W)
            self.salary.heading("Επώνυμο",text="Επώνυμο",anchor=tk.W)
            self.salary.heading("Σύνολο",text="Σύνολο",anchor=tk.W)
            self.refreshSalaries(0)

            self.salary.pack(expand=True,fill=tk.BOTH)
            self.salaryScroll.config(command=self.salary.yview)





    def refreshMovements(self,value,dateA=None,dateB=None):
        """Recreates the Treeview with the desired information(Specifically Movements
            @value: a non-avoidable 
        """
        if len(self.movements.get_children())!=0:
            for item in self.movements.get_children():
                self.movements.delete(item)
        count=0
        if dateA==None and dateB==None:
            if len(self.notes)!=0:
                move=self.notes[self.notes["Ιδιωτικό"]==False].sort_values("Ημερομηνία")
                for group,frame in move.groupby(level=0):
                    if len(pd.date_range(start=pd.to_datetime(frame["Ημερομηνία"].iloc[0]),end=pd.Timestamp.now(),freq="MS"))==0:
                        self.movements.insert(parent="",index=tk.END,iid=count,values=(str(frame["Ημερομηνία"].iloc[0]),frame["Όνομα"].iloc[0],frame["Τύπος"].iloc[0],frame["Έσοδο"].iloc[0],frame["Έξοδο"].iloc[0]))
                        count+=1
        else:
             if len(self.notes)!=0:
                move=self.notes[self.notes["Ιδιωτικό"]==False].sort_values("Ημερομηνία")
                startT=pd.to_datetime(dateA)
                endT=pd.to_datetime(dateB)
                for group,frame in move.groupby(level=0):
                    if startT<=pd.to_datetime(frame["Ημερομηνία"].iloc[0])<=endT:
                        self.movements.insert(parent="",index=tk.END,iid=count,values=(str(frame["Ημερομηνία"].iloc[0]),frame["Όνομα"].iloc[0],frame["Τύπος"].iloc[0],frame["Έσοδο"].iloc[0],frame["Έξοδο"].iloc[0]))
                        count+=1


    def refreshSalaries(self,value):
        if len(self.salary.get_children())!=0:
            for item in self.salary.get_children():
                self.salary.delete(item)
        count=0
        if len(self.coaches)!=0:
            for group,frame in self.coaches.sort_values("Τελευταία Μισθοδοσία").groupby(level=0):
                temp=list(frame.index[0])
                if len(frame["Τελευταία Μισθοδοσία"])==1:
                    requestedDate=frame["Τελευταία Μισθοδοσία"].iloc[0]
                else:
                    requestedDate=frame["Τελευταία Μισθοδοσία"].max()
                self.salary.insert(parent="",index=tk.END,iid=count,values=(str(requestedDate),temp[1],temp[0],frame["Σύνολο"].iloc[0]))
                count+=1
    
    def createReceipt(self,note,start,end):
        contentCanvas=tk.Canvas(self.contentFrame,bg="#474a48")
        contentCanvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        contentScroll=ttk.Scrollbar(self.contentFrame,command=contentCanvas.yview)
        contentScroll.pack(side=tk.RIGHT,fill=tk.Y)
        contentCanvas.configure(yscrollcommand=contentScroll.set)
        contentCanvas.bind("<Configure>",lambda e: contentCanvas.configure(scrollregion=contentCanvas.bbox("all")))
        actualFrame=tk.Frame(self.contentFrame,bg="#474a48")
        contentCanvas.create_window((0,0),window=actualFrame,anchor=tk.NW,)
        label=tk.Label(actualFrame,text="Αναλυση Ταμείου Συλλόγου",bg="#474a48",fg="#fff",font=("Arial Black",22),justify=tk.CENTER)
        label.pack()
        revenue={}
        cost={}
        for i in note["Τύπος"].unique():
            temp=note[note["Τύπος"].str.match(i)]
            if temp["Έσοδο"].sum()!=0:
                revenue[i]=temp["Έσοδο"].sum()
            if temp["Έξοδο"].sum()!=0:
                cost[i]=temp["Έξοδο"].sum()
        labelFrame=tk.Frame(actualFrame,bg="#474a48")
        labelFrame.pack(fill=tk.X)
        label=tk.Label(labelFrame,text="\nΕξόδα:",bg="#474a48",fg="#fff",font=("Arial",20),justify=tk.LEFT)
        label.pack(fill=tk.X,side=tk.LEFT)
        for content in cost:
            labelFrame=tk.Frame(actualFrame,bg="#474a48")
            labelFrame.pack(fill=tk.X)
            label=tk.Label(labelFrame,text=content+":",bg="#474a48",fg="#fff",font=("Arial",16),justify=tk.LEFT,width=15)
            label.pack(fill=tk.X,side=tk.LEFT)
            label=tk.Label(labelFrame,text=str(cost[content])+"€",bg="#474a48",fg="#fff",font=("Arial",16),justify=tk.LEFT)
            label.pack(fill=tk.X)
        labelFrame=tk.Frame(actualFrame,bg="#474a48")
        labelFrame.pack(fill=tk.X)
        label=tk.Label(labelFrame,text="\nΕσόδα:",bg="#474a48",fg="#fff",font=("Arial",20),justify=tk.LEFT)
        label.pack(fill=tk.X,side=tk.LEFT)
        for content in revenue:
            labelFrame=tk.Frame(actualFrame,bg="#474a48")
            labelFrame.pack(fill=tk.X)
            label=tk.Label(labelFrame,text=content+":",bg="#474a48",fg="#fff",font=("Arial",16),justify=tk.LEFT,width=15)
            label.pack(fill=tk.X,side=tk.LEFT)
            label=tk.Label(labelFrame,text=str(revenue[content])+"€",bg="#474a48",fg="#fff",font=("Arial",16),justify=tk.LEFT)
            label.pack(fill=tk.X)
        labelFrame=tk.Frame(actualFrame,bg="#474a48")
        labelFrame.pack(fill=tk.X)
        label=tk.Label(labelFrame,text="\n\nΣυνολικό Ταμείο: "+str(self.notes.iloc[0]["Ποσό"])+"€",bg="#474a48",fg="#fff",font=("Arial",20),justify=tk.CENTER)
        label.pack(fill=tk.X,side=tk.LEFT)




    def correctDate(self):
        month=self.dates[self.search.current()].month
        for group,frame in self.notes.groupby(lambda x:"a" if x["Ημερομηνία"].month==month else "b"):
            if group=="a":
                return frame

    def createEntry(self):
        if self.w_c["Create"]=="":
            if self.Variable.get()=="Οικονομικές Κινήσεις":
                aux.createMovement(self,self.root,self.notes)
            elif self.Variable.get()=="Μισθοδοσίες":
                aux.createCoach(self,self.coach)
        else:
            try:
                self.w_c["Create"].deiconify()
            except:
                self.w_c["Create"].iconify()
                self.w_c["Create"].deiconify();

    def viewSalary(self):
        if self.w_c["EditSalary"]=="":
            temp=self.salary.selection()
            if len(temp)!=0:
                for item in temp:
                    choices=self.salary.item(item,option="values")[1:3]
                init=aux.viewDetails(self,self.coaches,(choices[1],choices[0]))
        else:
            try:
                self.w_c["EditSalary"].deiconify()
            except:
                self.w_c["EditSalary"].iconify()
                self.w_c["EditSalary"].deiconify()


    def deleteEntry(self):
        if self.Variable.get()=="Οικονομικές Κινήσεις":
            temp=self.movements.selection()
            if len(temp)!=0:
                for item in temp:
                    choices=self.movements.item(item,option="values")[:3]
                    self.notes["Ποσό"].iloc[0]+=int(self.movements.item(item,option="values")[-1])-int(self.movements.item(item,option="values")[-2])
                    self.notes=self.notes.drop(self.notes[(self.notes["Ημερομηνία"].astype("str").str.match(choices[0])) &(self.notes["Όνομα"].str.match(choices[1]))&(self.notes["Τύπος"].str.match(choices[2]))].index[0])
                writeCalendar(self.notes)
                self.redraw()
        elif self.Variable.get()=="Μισθοδοσίες":
            temp=self.salary.selection()
            if len(temp)!=0:
                for item in temp:
                    choices=self.salary.item(item,option="values")[1:3]
                    print(self.coach.drop((choices[1],choices[0])))
                    self.coach=self.coach.drop((choices[1],choices[0]))
                writeCoaches(self.coach)
                self.redraw()

    def editEntry(self):
        if self.w_c["Edit"]=="":
            if self.Variable.get()=="Οικονομικές Κινήσεις":
                temp=self.movements.selection()
                if len(temp)!=0:
                    for item in temp:
                        choices=self.movements.item(item,option="values")[:3]
                        individual=self.notes[(self.notes["Ημερομηνία"].astype("str").str.match(choices[0])) &(self.notes["Όνομα"].str.match(choices[1]))&(self.notes["Τύπος"].str.match(choices[2]))].index[0]
                    init=aux.EditMovement(self,individual,self.notes)
            elif self.Variable.get()=="Μισθοδοσίες":
                temp=self.salary.selection()
                if len(temp)!=0:
                    for item in temp:
                        individual=self.salary.item(item,option="values")[1:3]
                    init=aux.editCoach(self,self.coach,(individual[1],individual[0]))
        else:
            try:
                self.w_c["Edit"].deiconify()
            except:
                self.w_c["Edit"].iconify()
                self.w_c["Edit"].deiconify()

    def set_date(self,value,begin):
        """Set date in the oprtion box and apply the changes to the Treeview
        """
        if begin=="A":
            self.rangeA.set(value)
            if self.Variable.get()=="Οικονομικές Κινήσεις":
                self.rangeA.set(value)
                self.refreshMovements(0,self.rangeA.get(),self.rangeB.get())
            elif self.Variable.get()=="Οικονομικές Κινήσεις":
                pass
        else:
            self.rangeB.set(value)
            if self.Variable.get()=="Οικονομικές Κινήσεις":
                self.refreshMovements(0,self.rangeA.get(),self.rangeB.get())
            elif self.Variable.get()=="Οικονομικές Κινήσεις":
                pass

