import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import tkinter.messagebox as mb
import ClubPage as pg
data = None
debug=True

def run(first=False):
    #innitializes the info dataframe
    data=None
    data = pd.read_excel("assets\\Data.xlsx")
    if first:
        tempData=pd.Timestamp.today()
        for group,frame in data.groupby(level=0):
            if frame["Ιδιότητα"].iloc[0]=="Αθλητής/τρια":
                data.loc[group,"Εκρεμμότητες"]+=len(list(pd.date_range(start=data.loc[group,"Τελευταία επεξεργασία"],end=tempData,freq="MS")))*30
                data.loc[group,"Τελευταία επεξεργασία"]=tempData
                if len(list(pd.date_range(start=data.loc[group,"Τελευταία Πληρωμή"],end=tempData,freq="MS")))>=1:
                    data.loc[group,"Κατάσταση"]=3
            else:
                data.loc[group,"Κατάσταση"]=0
    data=data.set_index(["Επώνυμο","Όνομα"])
    for i in data.columns:
        if i!="Τελευταία επεξεργασία"and i!="Ημερομηνία Δημιουργίας" and i!="Τελευταία Πληρωμή":
            data[i]=data[i].astype("object")
    return data

def write_data(data):
    #updates the excel file
    data.to_excel("assets\\Data.xlsx",index=True,header=True)

def update(data,name,surname,field,value):
    #data is the main data frame
    # surname the name index
    # name the surname index
    # field is the field we want to update
    # value is updated value of the field
    # throws ...  exception
    data[field].loc[(surname,name)] = value
class Athletes(tk.Frame):
    def __init__(self,window,cha):
        window.iconify()
        #Initialisation and main instance variables initialization
        self.root=tk.Toplevel(window,bg="#4e73c2")
        self.root.geometry("1000x900")
        self.root.resizable(True,True)
        super().__init__(self.root,bg="#4e73c2")
        super().place(relheight=1,relwidth=1)
        self.changes = cha
        self.window=window
        self.data=run()
        self.root.state("zoomed")
        self.w_c={"Create":"",
                    "Delete":"",
                    "Person":"",
                    "Project":""}

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
        self.title=tk.Label(self.headerFrame,text="Στοιχεία Μελών",bg="#c1c1c1")
        self.title.config(font=("Arial",36))
        self.title.place(relwidth=0.6,relheight=0.45,relx=0.3,rely=0)

        #Back Button
        backphoto=ImageTk.PhotoImage(Image.open("assets\\back.png").resize((75,75)))
        self.backButton=tk.Button(self.headerFrame,image=backphoto,command=self.goBack,bg="light grey",borderwidth=0)
        self.backButton.place(relheight=0.225,relwidth=0.05,relx=0.9,rely=0.7)

        #Forward Button
        forphoto=ImageTk.PhotoImage(Image.open("assets\\next.png").resize((75,75)))
        self.forwardButton=tk.Button(self.headerFrame,image=forphoto,command=self.goForward,bg="light grey",borderwidth=0)
        self.forwardButton.place(relheight=0.225,relwidth=0.05,relx=0.95,rely=0.7)

        #Create button, to create a new entry
        self.createButton=tk.Button(self.headerFrame,bg="#c1c1c1",text="Δημιουργία Καινούργιας Εγγραφής",command=self.createEntry,borderwidth=0)
        self.createButton.config(font=("Arial",15))
        self.createButton.place(relheight=0.15,relwidth=0.25,relx=0.3,rely=0.5)

        #Delete button, to delete an existing entry
        self.deleteButton=tk.Button(self.headerFrame,bg="#c1c1c1",text="Διαγραφή Υπάρχουσας Εγγραφής",command=self.deleteEntry,borderwidth=0)
        self.deleteButton.config(font=("Arial",16))
        self.deleteButton.place(relheight=0.15,relwidth=0.25,relx=0.3,rely=0.7)

        #Choice box about the category of the data
        options=["Επιλέξτε μια κατηγορία μέλους"]
        for i in self.data["Κατηγορία"].unique():
            options.append(str(i))
        self.formVar=tk.StringVar(self.headerFrame)
        self.formVar.set(options[0])
        self.forms=tk.OptionMenu(self.headerFrame,self.formVar,*options,command=self.updateForm)
        self.forms.config(font=("Arial",18),bg="#c1c1c1")
        self.forms['menu'].config(font=("Arial",18),bg="#c1c1c1")
        self.forms.place(relwidth=0.25,relheight=0.1,relx=0.58,rely=0.75)

        #List of data options
        self.typeOptions=["Στοιχεία"]
        for i in self.data.dropna(axis=1).columns:
            if str(i)!="Τελευταία επεξεργασία"and str(i)!="Τελευταία Πληρωμή" and str(i)!="Ημερομηνία Δημιουργίας"and str(i)!="Κατάσταση":
                self.typeOptions.append(str(i))
        self.typeVar=tk.StringVar(self.subHeaderFrame)
        self.typeVar.set(self.typeOptions[0])
        self.type=tk.OptionMenu(self.subHeaderFrame,self.typeVar,*self.typeOptions,command=self.update)
        self.type.config(font=("Arial",24),bg="#494949",fg="#fff")
        self.type['menu'].config(font=("Arial",18),bg="#494949")
        self.type.place(relwidth=0.25,relheight=0.15,relx=0.025,rely=0.27)
        self.type["state"]=tk.DISABLED

        #Club page creation button
        self.teamButton=tk.Button(self.subHeaderFrame,text="Δεδομένα\nΣυλόγου",command=self.initClub,bg="#494949",fg="#fff")
        self.teamButton.config(font=("Arial",36))
        self.teamButton.place(relwidth=0.25,relheight=0.2,relx=0.025,rely=0.05)

        #Main data frame for objects
        basicFrame=tk.Frame(self.subHeaderFrame,bg="#1b2135")
        basicFrame.place(relheight=1,relwidth=0.7,relx=0.3,rely=0)
        self.mainCanvas=tk.Canvas(basicFrame)
        self.mainCanvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.scroll=ttk.Scrollbar(basicFrame,command=self.mainCanvas.yview)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.mainCanvas.configure(yscrollcommand=self.scroll.set)
        self.mainCanvas.bind("<Configure>",lambda e: self.mainCanvas.configure(scrollregion=self.mainCanvas.bbox("all")))
        self.listFrame=ItemList(self,self.data,"#1b2135")
        self.mainCanvas.create_window((0,0),window=self.listFrame,anchor=tk.NW,width=1060,height=1330) #Be Careful

        self.ProjectButton=tk.Button(self.subHeaderFrame,bg="#494949",fg="#fff",text="Εμφάνιση Λίστας Εκκρεμοτήττων",command=self.projectData,borderwidth=0)
        self.ProjectButton.config(font=("Arial",16))
        self.ProjectButton.place(relwidth=0.25,relheight=0.15,relx=0.025,rely=0.45)
        #Save button
        # saveButton=tk.Button(self.subHeaderFrame,text="Αποθήκευση",command=self.save,bg="#494949",fg="#fff")
        # saveButton.config(font=("Arial",38))
        # saveButton.place(relwidth=0.25,relheight=0.175,relx=0.025,rely=0.675)

        self.root.protocol("WM_DELETE_WINDOW",self.exit)
        self.root.mainloop()

    def getWindow(self):
        return self.window
    def getChanges(self):
        return self.changes
    def exit(self):#The exit function
        write_data(self.data)
        self.changes.clear()
        self.window.deiconify()
        self.root.destroy()
    def disableAll(self):
        self.forms['state']=tk.DISABLED
        self.type['state']=tk.DISABLED
        self.ProjectButton['state']=tk.DISABLED
        self.createButton['state']=tk.DISABLED
        self.deleteButton['state']=tk.DISABLED
        self.teamButton['state']=tk.DISABLED
    def enableAll(self):
        self.forms['state']=tk.NORMAL
        self.type['state']=tk.NORMAL
        self.ProjectButton['state']=tk.NORMAL
        self.createButton['state']=tk.NORMAL
        self.deleteButton['state']=tk.NORMAL
        self.teamButton['state']=tk.NORMAL
    def initClub(self):
        if self.changes.checkExisting("Club")==1:
            self.changes.openExisting(self.root,"Athletes","Club",1)
        elif self.changes.checkExisting("Club")==-1:
            self.changes.openExisting(self.root,"Athletes","Club",-1)
        else:
            self.changes.addBack(self.root,"Athletes")
            init=pg.Club(self.root,self.changes)

    def goBack(self):#Back command
        self.changes.moveBack(self.root,"Athletes")

    def goForward(self):#Forward command
        self.changes.moveForward(self.root,"Athletes")

    def updateForm(self,value):
        if self.formVar.get()!="Επιλέξτε μια κατηγορία μέλους":
            self.type["state"]=tk.NORMAL
            tempdata=self.listFrame.check(self.formVar.get(),self.data)
            self.typeVar.set("")
            self.type["menu"].delete(0,'end')
            self.type["menu"].add_command(label="Στοιχεία",command=lambda value= "Στοιχεία": self.updateEntry(value))
            for column in tempdata.columns.unique():
                if column!="Τελευταία επεξεργασία" and column!="Τελευταία Πληρωμή" and column!="Ημερομηνία Δημιουργίας"and column!="Κατάσταση":
                    self.type["menu"].add_command(label=column,command=lambda value=column: self.updateEntry(value))
            self.typeVar.set("Στοιχεία")
            self.update(0)
        else:
            for i in self.listFrame.winfo_children():
                i.destroy()
                self.listFrame.items=[]
            self.type["state"]=tk.DISABLED

    def update(self,value):#Update list
        if self.formVar.get()!= "Επιλέξτε μια κατηγορία μέλους":
            self.listFrame.update(self.formVar.get(),self.typeVar.get() if self.typeVar.get()!="Στοιχεία" else None)


    def updateEntry(self,value):
        self.typeVar.set(value)
        self.update(0)

    def createEntry(self):#Create New entry
        if self.w_c["Create"]=="":
            self.top=tk.Toplevel(self.root,bg="#1b2135")
            self.top.geometry("500x200")
            self.top.resizable(True,True)
            self.w_c["Create"]=self.top
            self.top.title("Είδος Νέου Μέλους")
            frame=tk.Frame(self.top,bg="#1b2135")
            frame.pack(fill=tk.BOTH,expand=True)
            label=tk.Label(frame,text="Επιλεξτε το είδος του νέου μέλους")
            label.config(font=("Arial",18))
            label.pack(anchor=tk.CENTER)
            options=["Αθλητής/τρια","Προπονητικο Team","Χορηγος","Θεατης","Παλαιος Αθλητης","Παθητικο Μελος","Γονέας"]
            self.tempvar=tk.StringVar(frame)
            self.tempvar.set("Ιδιότητα")
            self.choicebox=tk.OptionMenu(frame,self.tempvar,"Ιδιότητα",*options,command=self.create)
            self.choicebox.config(font=("Arial",18))
            self.choicebox["menu"].config(font=("Arial",18))
            self.choicebox.pack(anchor=tk.CENTER)
            self.listFrame.disableAll()
            self.top.protocol("WM_DELETE_WINDOW",lambda :self.endAction("Create"))
            self.top.mainloop()
        else:
            try:
                self.w_c["Create"].deiconify()
            except :
                self.w_c["Create"].iconify()
                self.w_c["Create"].deiconify()

    def save(self):#Save button command
        write_data(self.data)

    def deleteEntry(self):
        if self.w_c["Delete"]=="":
            self.top=self.top=tk.Toplevel(self.root,bg="#1b2135")
            self.top.geometry("950x800")
            self.top.resizable(True,True)
            self.top.title("Διαγραφή Στοιχείου")
            self.w_c["Delete"]=self.top
            self.topFrame=tk.Frame(self.top,bg="#1b2135")
            self.topFrame.pack(fill=tk.BOTH,expand=True)
            self.titleFrame=tk.Frame(self.topFrame,bg="#1b2135")
            self.titleFrame.pack(fill=tk.X)
            tk.Label(self.titleFrame,text="Διαγραφή Μέλους",bg="#1b2135",fg="#fff",font=("Arial",24)).pack(anchor=tk.W,side=tk.LEFT)
            self.deleteVariable=tk.StringVar()
            self.deleteVariable.set("Αναζήτηση")
            self.deleteSearch=tk.Entry(self.titleFrame,textvariable=self.deleteVariable,bg="grey")
            self.deleteSearch.bind("<FocusIn>",func=self.clearDeleteInput)
            self.deleteSearch.bind("<Return>",func=self.refreshTreeview)
            self.deleteSearch.pack(padx=25,pady=25,side=tk.RIGHT)
            self.deleteSearch.config(font=("Arial",16))
            deleteButton=tk.Button(self.titleFrame,text="Διαγραφή Επιλεγμένων",command=self.deleteSelected)
            deleteButton.pack(pady=25,padx=10,side=tk.RIGHT)
            deleteButton.config(font=("Arial",16))

            self.treeframe=tk.Frame(self.topFrame)
            self.treeframe.pack(padx=10,pady=25,fill=tk.BOTH,expand=True)
            style=ttk.Style()
            style.configure("mystyle.Treeview",rowheight=25,font=("Arial",16))
            style.configure("mystyle.Treeview.Heading",rowheight=30,font=("Arial",18))
            tree_scroll=ttk.Scrollbar(self.treeframe)
            tree_scroll.pack(side=tk.RIGHT,fill=tk.Y)

            self.treeview=ttk.Treeview(self.treeframe,style="mystyle.Treeview",select=tk.EXTENDED,columns=["Όνομα","Επώνυμο","Κατηγορία"],yscrollcommand=tree_scroll.set)
            self.treeview.column("#0",width=0,stretch=tk.NO)
            self.treeview.column("Επώνυμο",anchor=tk.CENTER,width=120,minwidth=50)
            self.treeview.column("Όνομα",anchor=tk.W,width=120,minwidth=50)
            self.treeview.column("Κατηγορία",anchor=tk.W,width=120,minwidth=70)
            self.treeview.heading("#0",text='',anchor=tk.W)
            self.treeview.heading("Επώνυμο",text="Επώνυμο",anchor=tk.W)
            self.treeview.heading("Όνομα",text="Όνομα",anchor=tk.W)
            self.treeview.heading("Κατηγορία",text="Κατηγορία",anchor=tk.W)
            self.treeview.pack(anchor=tk.CENTER,expand=True,fill=tk.BOTH)
            self.refreshTreeview(0)

            tree_scroll.config(command=self.treeview.yview)


            self.top.protocol("WM_DELETE_WINDOW",lambda :self.endAction("Delete"))
            self.top.mainloop()
        else:
            try:
                self.w_c["Delete"].deiconify()
            except :
                self.w_c["Delete"].iconify()
                self.w_c["Delete"].deiconify()

    def create(self,event):
        if self.tempvar.get()!="Ιδιότητα":
            self.top.destroy()
            newWindow=ItemCreated(self,self.root,self.tempvar.get(),self.data,bg="#1b2135")




    def deleteSelected(self):
        temp=self.treeview.selection()
        for item in temp:
            self.data=self.data.drop(self.treeview.item(item,option="values")[:2])
            write_data(self.data)
            self.refreshTreeview(0)
            if mb.askyesno("Τέρματισμός Διαγραφής", "Είστε σίγουρος/η για την επιλογή σας;\nΗ σελίδα θα ανανεωθεί"):
                self.redraw()
            

    def redraw(self):
        tempWindow=self.getWindow()
        tempChanges=self.getChanges()
        self.root.destroy()
        init=Athletes(tempWindow,tempChanges)

    def clearDeleteInput(self,value):
        self.deleteVariable.set("")

    def refreshTreeview(self,event):
        if len(self.treeview.get_children())!=0:
            for item in self.treeview.get_children():
                self.treeview.delete(item)
        count=0
        searchResults=self.deleteVariable.get()
        if searchResults!="Αναζήτηση":
            for group,frame in self.data.reset_index().groupby(level=0):
                if (searchResults in frame["Όνομα"].iloc[0]) or (searchResults in frame["Επώνυμο"].iloc[0]) or (searchResults in frame["Κατηγορία"].iloc[0]):
                    self.treeview.insert(parent="",index=tk.END,iid=count,values=(frame["Επώνυμο"].iloc[0],frame["Όνομα"].iloc[0],frame["Κατηγορία"].iloc[0]))
                    count+=1
        else:
            for group,frame in self.data.reset_index().groupby(level=0):
                self.treeview.insert(parent="",index=tk.END,iid=count,values=(frame["Επώνυμο"].iloc[0],frame["Όνομα"].iloc[0],frame["Κατηγορία"].iloc[0]))
                count+=1

    def projectData(self):
        if self.w_c["Project"]=="":
            init=ProjectList(self,self.data)
        else:
            try:
                self.w_c["Project"].deiconify()
            except:
                self.w_c["Project"].iconify()
                self.w_c["Project"].deiconify()
    def refresh(self,data=None):
        self.data=run() if type(data)==None else data

    def endAction(self,origin):
        self.w_c[origin]=""
        self.top.destroy()
        self.listFrame.enableAll()


class ItemList(tk.Frame):
    def __init__(self,root,data,bco):
        self.data=data
        self.bco=bco
        self.items=[]
        self.scrollbar=None
        super().__init__(root.mainCanvas,bg=bco)
        self.root=root

    def setScrollBar(self,obj):
        self.scrollbar=obj
    def disableAll(self):
        self.root.disableAll()
        if len(self.items)!=0:
            for item in self.items:
                item["state"]=tk.DISABLED
    def enableAll(self):
        self.root.enableAll()
        if len(self.items)!=0:
            for item in self.items:
                item["state"]=tk.NORMAL
            self.root.update(0)

    def update(self,category,parameter=None):
        self.data=run()
        self.root.refresh(self.data)
        for i in self.winfo_children():
            i.destroy()
            self.items=[]
        if category!=None:
            counter=0
            tempdata=self.check(category,self.data)

            for group,frame in tempdata.where(tempdata["Κατηγορία"].str.match(category)).dropna().groupby(level=0):
                self.items.append(ItemButton(self,self.data,frame,self.bco,parameter,width=100))
                self.items[-1].pack(fill=tk.X)
                counter+=1
    def check(self,cat,data):
        if len(data)==0:
            return pd.DataFrame()
        return data[["Έτος Γέννησης","Σταθερό","Κατηγορία","Ιδιότητα","Κινητό","Email","Επάγγελμα","Χόμπυ","Σχέση με τον Αθλητισμό"]] if data[data["Κατηγορία"].str.match(cat)]["Ιδιότητα"].unique()[0]!="Αθλητής/τρια" else data.drop(columns=["Επάγγελμα","Χόμπυ","Σχέση με τον Αθλητισμό"])

class ItemButton(tk.Button):
    def __init__(self,root,data,personObj,bgc,param=None,**kwargs):
        self.root=root
        self.data=data
        self.DueChange=""
        self.person= personObj
        self.textName=" ".join(list(self.person.index[0])) + "  | {}: {}".format(param,self.person.loc[self.person.index[0]][param]) if param!=None else " ".join(list(self.person.index[0]))
        super().__init__(root,text=self.textName,fg="#fff",command=self.produceData,bg=bgc)
        super().config(font=("Arial",18))
    def produceData(self):
        #The more information window
        self.root.disableAll()
        self.top=tk.Toplevel(bg="#1b2135")
        self.top.geometry("800x750")
        self.top.resizable(True,True)
        self.top.title(self.textName)
        self.topFrame=tk.Frame(self.top,bg="#1b2135")
        self.topFrame.place(relheight=1,relwidth=1,relx=0,rely=0)
        self.frames={}
        self.entries={}
        namevar=tk.StringVar()
        namevar.set(list(self.person.index[0])[0])
        self.nameFrame=tk.Frame(self.topFrame,bg="#1b2135")
        self.nameFrame.place(relheight=0.1,relwidth=0.4,relx=0.05,rely=0.025)
        self.nameLabel=tk.Label(self.nameFrame,text="Επώνυμο",bg="#1b2135",fg="#fff")
        self.nameLabel.config(font=("Arial",18))
        self.nameLabel.place(relheight=0.5,relwidth=1,relx=0,rely=0)
        self.nameEntry=tk.Entry(self.nameFrame,textvariable=namevar,bg="#fff")
        self.nameEntry.config(font=("Arial",18))
        self.nameEntry.place(relheight=0.5,relwidth=1,relx=0,rely=0.5)
        self.nameEntry["state"]=tk.DISABLED
        self.frames["Επώνυμο"]=self.nameEntry
        self.entries["Επώνυμο"]=namevar

        surNamevar=tk.StringVar()
        surNamevar.set(list(self.person.index[0])[1])
        surNameFrame=tk.Frame(self.topFrame,bg="#1b2135")
        surNameFrame.place(relheight=0.1,relwidth=0.4,relx=0.55,rely=0.025)
        self.surNameLabel=tk.Label(surNameFrame,text="Όνομα",bg="#1b2135",fg="#fff")
        self.surNameLabel.config(font=("Arial",18))
        self.surNameLabel.place(relheight=0.5,relwidth=1,relx=0,rely=0)
        self.surNameEntry=tk.Entry(surNameFrame,textvariable=surNamevar,bg="#fff")
        self.surNameEntry.config(font=("Arial",18))
        self.surNameEntry.place(relheight=0.5,relwidth=1,relx=0,rely=0.5)
        self.surNameEntry["state"]=tk.DISABLED
        self.frames["Όνομα"]=self.surNameEntry
        self.entries["Όνομα"]=surNamevar

        categories=list(self.root.data["Κατηγορία"].unique())
        catvar=tk.StringVar()
        catvar.set(self.person["Κατηγορία"].iloc[0])
        self.catFrame=tk.Frame(self.topFrame,bg="#1b2135")
        self.catFrame.place(relheight=0.1,relwidth=0.4,relx=0.3,rely=0.15)
        self.catLabel=tk.Label(self.catFrame,text="Κατηγορία",bg="#1b2135",fg="#fff")
        self.catLabel.config(font=("Arial",18))
        self.catLabel.place(relheight=0.5,relwidth=1,relx=0,rely=0)
        self.catEntry=tk.Entry(self.catFrame,textvariable=catvar,bg="#fff")
        self.catEntry.config(font=("Arial",18))
        self.catEntry.place(relheight=0.5,relwidth=1,relx=0,rely=0.5)
        self.catEntry["state"]=tk.DISABLED
        self.frames["Κατηγορία"]=self.catEntry
        self.entries["Κατηγορία"]=catvar

        self.rest=tk.Frame(self.top,bg="#1b2135")
        self.rest.place(relheight=0.5,relwidth=0.9,relx=0.05,rely=0.275)
        counter=0
        self.frames={}
        for cat in self.person.iloc[0].index:
            if cat!="Κατηγορία" and cat!="Τελευταία επεξεργασία"and cat!="Τελευταία Πληρωμή" and cat!="Ημερομηνία Δημιουργίας"and cat!="Κατάσταση":
               tempFrame=tk.LabelFrame(self.rest,bg="#1b2135")
               tempFrame.place(relheight=0.1,relwidth=1,relx=0,rely=0+0.075*counter)
               tempVar=tk.StringVar()
               tempVar.set(self.person[cat].iloc[0])
               tempLabel=tk.Label(tempFrame,text="{:20s}".format(cat),bg="#1b2135",fg="#fff",justify=tk.LEFT,anchor='w')
               tempLabel.config(font=("Arial",14))
               tempLabel.place(relwidth=0.5,relheight=1)
               tempEntry=tk.Entry(tempFrame,textvariable=tempVar,bg="#fff")
               tempEntry.config(font=("Arial",14))
               tempEntry.place(relwidth=0.5,relheight=1,relx=0.5)
               tempEntry["state"]=tk.DISABLED
               self.frames[cat]=tempEntry
               self.entries[cat]=tempVar
               if cat=="Εκκρεμότητες":
                   self.DueChange=self.person[cat].iloc[0]
               counter+=1

        temp=None
        tempLabel=None
        tempEntry=None
        tempVar=None

        self.editButton=tk.Button(self.topFrame,text="Επεξεργασία",command=self.enable)
        self.editButton.place(relheight=0.05,relwidth=0.35,relx=0.1,rely=0.9)
        self.doneButton=tk.Button(self.topFrame,text="Ολοκλήρωση",command=self.complete)
        self.doneButton.place(relheight=0.05,relwidth=0.35,relx=0.55,rely=0.9)
        self.doneButton["state"]=tk.DISABLED

        self.top.protocol("WM_DELETE_WINDOW",self.endAction)
        self.top.mainloop()
    def updateData(self,event):
        try:
            self.data["Ημερομηνία Δημιουργίας"].loc[self.person.index]=pd.to_datetime(self.dateVar.get(),dayfirst=True)

            write_data(self.data)
            self.data=run()
        except Exception:
            print(pd.to_datetime(self.dateVar.get()))

    def endAction(self):
        self.top.destroy()
        self.root.root.redraw()
    def enable(self):
        self.doneButton["state"]=tk.NORMAL
        self.nameEntry["state"]=tk.NORMAL
        self.surNameEntry["state"]=tk.NORMAL
        self.catEntry["state"]=tk.NORMAL
        for i in self.frames:
            self.frames[i]["state"]=tk.NORMAL

    def complete(self):
        index=self.person.index
        data={}
        for i in self.entries:
            data[i]=self.entries[i].get()
        if data["Όνομα"]!="" and data["Επώνυμο"]!="" and data["Κατηγορία"]!="":
            ind=self.data.index.get_loc(index[0])
            self.data=self.data.reset_index()
            self.data.loc[ind,"Όνομα"]=data["Όνομα"] if data["Όνομα"]!="" else "-"
            self.data.loc[ind,"Επώνυμο"]=data["Επώνυμο"] if data["Επώνυμο"]!="" else "-"
            index=(self.data.loc[ind,"Επώνυμο"],self.data.loc[ind,"Όνομα"])
            self.data=self.data.set_index(["Επώνυμο","Όνομα"])
            for i in data:
                if i!="Όνομα" and i!="Επώνυμο":
                    if i=="Μπλούζες Δωρεάν" or i=="Μπλούζες Χρεωμένες" or i=="Σύνολο για Μπλούζες" or i=="Εκρεμμότητες":
                        self.data.loc[index,i]=int(data[i]) if data[i]!="" else 0
                    elif i=="Ημερομηνία Δημιουργίας":
                        self.data.loc[index,i]=pd.to_datetime(data[i]) if data[i]!="" else self.data.loc[index,i]
                    elif i=="Όνομα" or i=="Επώνυμο":
                        ind=self.data.index.get_loc(index[0])
                        self.data=self.data.reset_index()
                        self.data.loc[ind,i]=data[i] if data[i]!="" else "-"
                        self.data=self.data.set_index(["Επώνυμο","Όνομα"])
                    else:
                        self.data.loc[index,i]=data[i] if data[i]!="" else "-"
                if self.DueChange!=data["Εκρεμμότητες"]:
                    self.data.loc[index,"Τελευταία Πληρωμή"]=pd.Timestamp.today()
                    if int(data["Εκρεμμότητες"])<=0:
                        self.data.loc[index,"Κατάσταση"]=1
                    else:
                        self.data.loc[index,"Κατάσταση"]=2

            write_data(self.data)
        else:
            mb.showinfo("Σφάλμα","Τα πεδία Όνομα, Επώνυμο και Κατηγορία πρέπει να έχουν τιμή")
        self.disable()


    def disable(self):
        if mb.askyesno("Έξοδος","Θα θέλατε να αποχωρήσετε;"):
            self.endAction()
        else:
            self.nameEntry["state"]=tk.DISABLED
            self.surNameEntry["state"]=tk.DISABLED
            self.catEntry["state"]=tk.DISABLED
            for i in self.frames:
                self.frames[i]["state"]=tk.DISABLED
            self.doneButton["state"]=tk.DISABLED

class windowManager:
    def __init__(self):#Initializes the window manager
        self.back=[]
        self.forward=[]

    def getBack(self):#Returns the back list
        return self.back

    def getForward(self):#Returns the forward list
        return self.forward;

    def checkForward(self):#Returns True, if there is an element to forward to
        return len(self.forward)!=0

    def checkBack(self):#Return True, if there is an element to back to
        return len(self.back)!=0

    def addBack(self,toplevel,descr):#Adds a window in the back list as a the current back destination
        self.back.append((toplevel,descr))

    def addForward(self,toplevel,descr):#Adds a window in the forward list as the current forward destination
        self.forward.append((toplevel,descr))
    def checkExisting(self,name: str)->int:
        '''Checks if a window type already exists
        '''
        for i in self.back:
            if i[1]==name:
                return 1
        for i in self.forward:
            if i[1]==name:
                return -1
        return 0

    def openExisting(self,root:tk.Toplevel,descr:str,name:str,where:int)-> None:
        '''Moves to an already existing window
        '''
        if where>0:
            for i in self.back:
                if i[1]==name:
                    self.back.remove(i)
                    i[0].deiconify()
                    root.iconify()
                    self.addBack(root,descr)
        elif where<0:
            for i in self.forward:
                if i[1]==name:
                    self.forward.remove(i)
                    i[0].deiconify()
                    root.iconify()
                    self.addBack(root,descr)
            

    def moveBack(self,curr,descr):#Initiates a move to previous window action, while setting the current window as a forward destination with its string description
        if self.checkBack():
            self.back.pop()[0].deiconify()
            curr.iconify()
            self.addForward(curr,descr)
        else:
            return

    def moveForward(self,curr,descr):#Initiates a move to next window action, while setting the current window as a back destination with its string description.
        if self.checkForward():#Warning: checks if there is a window to forward to
            self.forward.pop()[0].deiconify()
            curr.iconify()
            self.addBack(curr,descr)
        else:
            return

    def peekType(self,direction=0):#Returns the string description of the desired destination in order to update old windows
        if not direction:
            return self.back[0][1] if self.checkBack() else ""
        else:
            return self.forward[0][1] if self.checkForward() else ""

    def clear(self):#Clears front and back lists
        self.back=[]
        self.forward=[]


class typedEntry(tk.Entry):
    def __init__(self,master,root,data,index,tv,cat,*args,**kwargs):
        self.master=master
        self.root=root
        self.data=data
        self.index=index
        self.textvar=tv
        self.category=cat
        super().__init__(master,textvariable=self.textvar,*args,**kwargs)
        super().bind("<FocusOut>",self.updateData)
    def updateData(self,value):
        self.data[self.category].loc[self.index]=self.textvar.get()
        write_data(self.data)
        self.data=run()
    def getCat(self):
        return self.category;

class ItemCreated(tk.Frame):
    def __init__(self,root:Athletes,window,state: str,data,**kwargs):
        self.father=root
        self.window=window
        self.state=state
        self.data=data
        self.attributes={}
        self.entries={}


        self.root=tk.Toplevel(self.window,bg="#1b2135")
        self.root.geometry("950x900")
        self.root.resizable(True,True)
        self.father.w_c["Create"]=self.root
        self.root.title("Δημιουργία: "+self.state)
        super().__init__(self.root,**kwargs)
        super().place(relheight=1,relwidth=1)

        for i in self.check().reset_index().columns:
            self.attributes[i]=""
        self.attributes["Ιδιότητα"]=self.state
        self.attributes["Τελευταία επεξεργασία"]=pd.Timestamp.today()
        self.attributes["Τελευταία Πληρωμή"]=pd.Timestamp.today()
        self.attributes["Κατάσταση"]=1 if self.state=="Αθλητής/τρια" else 0
        self.attributes["Ημερομηνία Δημιουργίας"]=pd.Timestamp.today()
        namevar=tk.StringVar()
        namevar.set("")
        self.nameFrame=tk.Frame(self,bg="#1b2135")
        self.nameFrame.place(relheight=0.1,relwidth=0.4,relx=0.05,rely=0.05)
        self.nameLabel=tk.Label(self.nameFrame,text="{:20s}".format("Όνομα:"),bg="#1b2135",fg="#fff")
        self.nameLabel.config(font=("Arial",18))
        self.nameLabel.pack(anchor=tk.NW,fill=tk.X)
        self.nameEntry=tk.Entry(self.nameFrame,textvariable=namevar,bg="#fff")
        self.nameEntry.config(font=("Arial",18))
        self.nameEntry.pack(anchor=tk.NW,fill=tk.X)
        self.entries["Όνομα"]=namevar

        surNamevar=tk.StringVar()
        surNamevar.set("")
        self.surNameFrame=tk.Frame(self,bg="#1b2135")
        self.surNameFrame.place(relheight=0.1,relwidth=0.4,relx=0.55,rely=0.05)
        self.surNameLabel=tk.Label(self.surNameFrame,text="{:20s}".format("Επώνυμο:"),bg="#1b2135",fg="#fff")
        self.surNameLabel.config(font=("Arial",18))
        self.surNameLabel.pack(anchor=tk.NW,fill=tk.X)
        self.surNameEntry=tk.Entry(self.surNameFrame,textvariable=surNamevar,bg="#fff")
        self.surNameEntry.config(font=("Arial",18))
        self.surNameEntry.pack(anchor=tk.NW,fill=tk.X)
        self.entries["Επώνυμο"]=surNamevar

        catvar=tk.StringVar()
        catvar.set("" if self.state=="Αθλητής/τρια" else self.state)
        self.catFrame=tk.Frame(self,bg="#1b2135")
        self.catFrame.place(relheight=0.1,relwidth=0.4,relx=0.3,rely=0.2)
        self.catLabel=tk.Label(self.catFrame,text="{:20s}".format("Κατηγορία:"),bg="#1b2135",fg="#fff")
        self.catLabel.config(font=("Arial",18))
        self.catLabel.pack(anchor=tk.NW,fill=tk.X)
        self.catEntry=tk.Entry(self.catFrame,textvariable=catvar,bg="#fff")
        self.catEntry.config(font=("Arial",18))
        self.catEntry.pack(anchor=tk.NW,fill=tk.X)
        self.entries["Κατηγορία"]=catvar

        restFrame=tk.Frame(self,bg="#1b2135")
        restFrame.place(relheight=0.5,relwidth=0.9,relx=0.05,rely=0.35)
        counter=0
        for cat in self.check().reset_index().columns:
            if cat!="Όνομα"and cat!="Επώνυμο" and cat!="Κατηγορία" and cat!="Ιδιότητα" and cat!="Τελευταία Πληρωμή" and cat!="Τελευταία επεξεργασία" and cat!="Ημερομηνία Δημιουργίας" and cat!="Κατάσταση":

                tempVariable=tk.StringVar()
                tempVariable.set("")
                tempFrame=tk.LabelFrame(restFrame,bg="#1b2135")
                tempFrame.place(relheight=0.1,relwidth=1,relx=0,rely=0+0.075*counter)
                tempLabel=tk.Label(tempFrame,text="{:25s}".format(cat.strip()),bg="#1b2135",fg="#fff",anchor="w")
                tempLabel.config(font=("Arial",18))
                tempLabel.place(relwidth=0.5,relheight=1)
                tempEntry=tk.Entry(tempFrame,textvariable=tempVariable,bg="#fff")
                tempEntry.config(font=("Arial",18))
                tempEntry.place(relwidth=0.5,relheight=1,relx=0.5)
                self.entries[cat]=tempVariable
                counter+=1

        self.doneButton=tk.Button(self,text="Ολοκλήρωση",command=self.complete,font=("Arial",16))
        self.doneButton.place(relheight=0.05,relwidth=0.35,relx=0.55,rely=0.9)


        tempLabel=None
        tempEntry=None
        tempFrame=None

        self.root.protocol("WM_DELETE_WINDOW",self.endAction)
        self.root.mainloop()
    def endAction(self):
        self.father.w_c["Create"]=""
        self.root.destroy()
        self.redraw()
    def redraw(self):
        tempWindow=self.father.getWindow()
        tempChanges=self.father.getChanges()
        self.father.root.destroy()
        init=Athletes(tempWindow,tempChanges)

    def complete(self):
        for i in self.entries:
            self.attributes[i]=self.entries[i].get()
        if not (self.attributes["Όνομα"]=="" or  self.attributes["Επώνυμο"]=="" or self.attributes["Κατηγορία"]==""):
            try:
                try:
                    if self.attributes["Εκρεμμότητες"]=="":
                        self.attributes["Εκρεμμότητες"]=0
                        self.attributes["Κατάσταση"]=1
                    else:
                        self.attributes["Εκρεμμότητες"]=int(self.attributes["Εκρεμμότητες"])
                        self.attributes["Κατάσταση"]=2
                    if self.attributes["Μπλούζες Δωρεάν"]=="":
                            self.attributes["Μπλούζες Δωρεάν"]=0
                    else:
                        self.attributes["Μπλούζες Δωρεάν"]=int(self.attributes["Μπλούζες Δωρεάν"])
                    if self.attributes["Μπλούζες Χρεωμένες"]=="":
                        self.attributes["Μπλούζες Χρεωμένες"]=0
                    else:
                        self.attributes["Μπλούζες Χρεωμένες"]=int(self.attributes["Μπλούζες Χρεωμένες"])
                    if self.attributes["Σύνολο για Μπλούζες"]=="":
                        self.attributes["Σύνολο για Μπλούζες"]=0
                    else:
                        self.attributes["Σύνολο για Μπλούζες"]=int(self.attributes["Σύνολο για Μπλούζες"])
                except KeyError:
                    pass
                temp=pd.Series(self.attributes)
                temp=temp.where(temp!="")
                self.data=self.data.reset_index().append(temp,ignore_index=True)
                self.data=self.data.set_index("Επώνυμο","Όνομα").fillna("-")
                write_data(self.data)
                self.data=run()
                if mb.askyesno("Τέρματισμός Δημιουργίας", "Θα θέλατε να τερματίσετε την δημιουργία;\nΗ σελίδα θα ανανεωθεί"):
                    self.father.w_c["Create"]=""
                    self.root.destroy()
                    self.redraw()
            except ValueError:
                 mb.showerror("Πρόβλημα στην εισαγωγή", "Κάποιο δεδομένο δεν είχε τον σωστό τύπο\n(πχ. κείμενο αντί για αριθμό);\nΠαρακαλώ, προσπαθήστε ξανά")

    def check(self):
        if len(self.data)==0:
            return pd.DataFrame()
        return self.data[["Έτος Γέννησης","Σταθερό","Κατηγορία","Ιδιότητα","Κινητό","Email","Επάγγελμα","Χόμπυ","Σχέση με τον Αθλητισμό"]] if self.state!="Αθλητής/τρια" else self.data.drop(columns=["Επάγγελμα","Χόμπυ","Σχέση με τον Αθλητισμό"])

class categoryEntry(tk.Entry):
    
    def __init__(self,master,cat,textv,root,**kwargs):
        self.root=root
        self.master=master
        self.textvar=textv
        self.category=cat
        super().__init__(master,textvariable=self.textvar,**kwargs)
        super().bind("<FocusOut>",func=self.update)
    def update(self,value):
        print(self.textvar.get())
        self.root.attributes[self.category]=self.textvar.get()
    def getCat(self):
        return self.category;

class ProjectList(tk.Toplevel):
    def __init__(self,master,data):
        self.master=master
        self.data=data
        self.imag={}
        self.top=super().__init__(master,bg="#1b2135")
        super().geometry("1400x800")
        super().resizable(True,True)
        self.master.w_c["Project"]=self
        self.topFrame=tk.Frame(self,bg="#1b2135")
        self.topFrame.pack(fill=tk.BOTH,expand=True)
        miniframe=tk.Frame(self.topFrame,bg="#1b2135")
        miniframe.pack(padx=25,pady=15,anchor=tk.E,fill=tk.X)
        label=tk.Label(miniframe,text="Λίστα Οφειλών Μελών",font=("Arial",24),fg="#fff",bg="#1b2135")
        label.pack(padx=25,pady=15,side=tk.LEFT,anchor=tk.W)
        self.projectVariable=tk.StringVar()
        self.projectVariable.set("Αναζήτηση")
        self.projectSearch=tk.Entry(miniframe,textvariable=self.projectVariable,bg="grey")
        self.projectSearch.bind("<FocusIn>",func=lambda x:self.projectVariable.set(""));
        self.projectSearch.bind("<Return>",func=self.refreshTreeview)
        self.projectSearch.bind("<FocusOut>",func=self.refreshTreeview)
        self.projectSearch.pack(padx=20,side="right",ipady=8)
        self.projectSearch.config(font=("Arial",16))

        self.emailButton=tk.Button(miniframe,text="Αποστολή Email",font=('Arial', 16),command=lambda : print(self.treeview.item(self.treeview.selection()[0],option="values")[5]))
        self.emailButton.pack(side="right")
        self.emailAllButton=tk.Button(miniframe,text="Αποστολή σε όλους",font=('Arial', 16),command=lambda : print(self.treeview.item(self.treeview.selection()[0],option="values")[5]))
        self.emailAllButton.pack(side="right",padx=10)
        self.treeframe=tk.Frame(self.topFrame)
        self.treeframe.pack(padx=10,pady=25)

        tree_scroll=ttk.Scrollbar(self.treeframe)
        tree_scroll.pack(side=tk.RIGHT,fill=tk.Y)

        style=ttk.Style()
        style.configure('Treeview', rowheight=60)
        style.configure("mystyle.Treeview",font=('Arial', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Arial', 14,'bold'),rowheight=120) # Modify the font of the headings
        self.treeview=ttk.Treeview(self.treeframe,style="mystyle.Treeview",select=tk.EXTENDED,columns=["Όνομα","Επώνυμο","Κατηγορία",'Σταθερό',"Κινητό","Email","Εκκρεμμότητες","Ημέρες από Εξόφληση"],yscrollcommand=tree_scroll.set)
        self.treeview.column("#0",width=120,stretch=tk.NO)
        self.treeview.column("Επώνυμο",anchor=tk.CENTER,width=120,minwidth=50)
        self.treeview.column("Όνομα",anchor=tk.W,width=120,minwidth=50)
        self.treeview.column("Κατηγορία",anchor=tk.W,width=120,minwidth=70)
        self.treeview.column("Σταθερό",anchor=tk.W,width=120,minwidth=70)
        self.treeview.column("Κινητό",anchor=tk.W,width=120,minwidth=70)
        self.treeview.column("Email",anchor=tk.W,width=180,minwidth=70)
        self.treeview.column("Εκκρεμμότητες",anchor=tk.W,width=160,minwidth=70)
        self.treeview.column("Ημέρες από Εξόφληση",anchor=tk.W,width=240,minwidth=70)
        self.treeview.heading("#0",text='Κατάσταση',anchor=tk.CENTER)
        self.treeview.heading("Επώνυμο",text="Επώνυμο",anchor=tk.W)
        self.treeview.heading("Όνομα",text="Όνομα",anchor=tk.W)
        self.treeview.heading("Κατηγορία",text="Κατηγορία",anchor=tk.W)
        self.treeview.heading("Σταθερό",text="Σταθερό",anchor=tk.W)
        self.treeview.heading("Κινητό",text="Κινητό",anchor=tk.W)
        self.treeview.heading("Email",text="Email",anchor=tk.W)
        self.treeview.heading("Εκκρεμμότητες",text="Εκκρεμμότητες",anchor=tk.W)
        self.treeview.heading("Ημέρες από Εξόφληση",text="Ημέρες από Εξόφληση",anchor=tk.W)
        self.treeview.pack(expand=True,fill=tk.BOTH)
        self.refreshTreeview(0)
        tree_scroll.config(command=self.treeview.yview)
        self.protocol("WM_DELETE_WINDOW",self.endAction)
        self.mainloop()

    def refreshTreeview(self,value):
        if len(self.treeview.get_children())!=0:
            for item in self.treeview.get_children():
                self.treeview.delete(item)
        count=0
        searchResults=self.projectVariable.get()
        if searchResults.strip()=="":
            self.projectVariable.set("Αναζήτηση")
        if searchResults!="Αναζήτηση":
            for group,frame in self.data.reset_index().groupby(level=0):
                if frame["Ιδιότητα"].iloc[0]=="Αθλητής/τρια":
                    if (searchResults in frame["Όνομα"].iloc[0]) or (searchResults in frame["Επώνυμο"].iloc[0]) or (searchResults in frame["Κατηγορία"].iloc[0]):
                        if frame["Κατάσταση"].iloc[0]>1:
                            self.imag[frame["Όνομα"].iloc[0]+" "+frame["Επώνυμο"].iloc[0]]=ImageTk.PhotoImage(file="assets//state"+str(frame["Κατάσταση"].iloc[0])+".png")
                            self.treeview.insert(parent='',text="",image=self.imag[frame["Όνομα"].iloc[0]+" "+frame["Επώνυμο"].iloc[0]],index=tk.END,iid=count,values=(frame["Επώνυμο"].iloc[0],frame["Όνομα"].iloc[0],frame["Κατηγορία"].iloc[0],frame["Σταθερό"].iloc[0],frame["Κινητό"].iloc[0],frame["Email"].iloc[0],frame["Εκρεμμότητες"].iloc[0],len(pd.date_range(start=frame["Τελευταία Πληρωμή"].iloc[0],end=pd.Timestamp.today(),freq="D"))-1))
                            count+=1
        else:
            for group,frame in self.data.reset_index().groupby(level=0):
                if frame["Ιδιότητα"].iloc[0]=="Αθλητής/τρια":
                    if frame["Κατάσταση"].iloc[0]>1:
                        self.imag[frame["Όνομα"].iloc[0]+" "+frame["Επώνυμο"].iloc[0]]=ImageTk.PhotoImage(file="assets//state"+str(frame["Κατάσταση"].iloc[0])+".png")
                        self.treeview.insert(parent='',text="",image=self.imag[frame["Όνομα"].iloc[0]+" "+frame["Επώνυμο"].iloc[0]],index=tk.END,iid=count,values=(frame["Επώνυμο"].iloc[0],frame["Όνομα"].iloc[0],frame["Κατηγορία"].iloc[0],frame["Σταθερό"].iloc[0],frame["Κινητό"].iloc[0],frame["Email"].iloc[0],frame["Εκρεμμότητες"].iloc[0],len(pd.date_range(start=frame["Τελευταία Πληρωμή"].iloc[0],end=pd.Timestamp.today(),freq="D"))-1))
                        count+=1
    def endAction(self):
        self.master.w_c["Project"]=""
        self.destroy()

    #def email(self):
    #    print(self.treeview.selection())
