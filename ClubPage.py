import OperationFunctions as of
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import tkinter.messagebox as mb
import pandas as pd
import numpy as np

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
                self.salary.insert(parent="",index=tk.END,iid=count,values=(str(frame["Τελευταία Μισθοδοσία"].iloc[0]),temp[1],temp[0],frame["Σύνολο"].iloc[0]))
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
                createMovement(self,self.root,self.notes)
            elif self.Variable.get()=="Μισθοδοσίες":
                createCoach(self,self.coach)
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
                init=viewDetails(self,self.coaches,(choices[1],choices[0]))
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
                    init=EditMovement(self,individual,self.notes)
            elif self.Variable.get()=="Μισθοδοσίες":
                temp=self.salary.selection()
                if len(temp)!=0:
                    for item in temp:
                        individual=self.salary.item(item,option="values")[1:3]
                    init=editCoach(self,self.coach,(individual[1],individual[0]))
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
        self.window.w_c["EditSalary"]=""
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
            writeCalendar(self.notes)
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
        entry=tk.OptionMenu(labelFrame,textVar,*values,command=lambda choice: self.modifyChoices(True if choice=="Έσοδo" else False))
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
        writeCalendar(self.notes)
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
            writeCoaches(self.coach)
            self.master.redraw()
    def enable(self):
        pass


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
        textVar.set(self.coach.loc[self.choice,"Ημερομηνία Δημιουργίας"])
        entry=tk.Entry(labelFrame,textvariable=textVar,font=('Arial',18))
        entry.place(relheight=0.5,relwidth=1,rely=0.5)
        entry["state"]=tk.DISABLED
        self.entries["Ημερομηνία Δημιουργίας"]=textVar
        self.widget["Ημερομηνία Δημιουργίας"]=entry


        editButton=tk.Button(mainFrame,text="Επεξεργασία",command=self.enable,bg="#bec1c4",font=('Arial',18))
        editButton.place(relheight=0.075,relwidth=0.4,relx=0.05,rely=0.9)
        doneButton=tk.Button(mainFrame,text="Ολοκλήρωση",command=self.complete,bg="#bec1c4",font=('Arial',18))
        doneButton.place(relheight=0.075,relwidth=0.4,relx=0.55,rely=0.9)

        self.root.protocol("WM_WINDOW_DESTROY",self.exit)
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
            writeCoaches(self.coach)
            self.master.redraw()
    def enable(self):
        for i in self.widget:
            self.widget[i]['state']=tk.NORMAL


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
            if len(pd.date_range(start=self.TrueCoach["Τελευταία Μισθοδοσία"].to_timestamp(freq="D"),end=pd.Timestamp.now(),freq="MS"))==0:
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
            writeCoaches(self.coach)
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