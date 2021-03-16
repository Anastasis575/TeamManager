import tkinter as tk
import pandas as pd
from PIL import ImageTk,Image
import OperationFunctions as of
import tkinter.messagebox as mb
import ClubPage as pg

def main():
    change=of.windowManager()
    def Exit():
        Main.destroy()
    def initAthlete():
        for i in change.getBack()+change.getForward():
            i[0].destroy()
        change.clear()
        change.addBack(Main,"Main")
        of.write_data(data)
        AthleteFrame=of.Athletes(Main,change)      

    def initClub():
        for i in change.getBack()+change.getForward():
            i[0].destroy()
        change.clear()
        change.addBack(Main,"Main")
        init=pg.Club(Main,change)

    def goBack():
        change.moveBack(Main,"Main")
    def goForward():
        change.moveForward(Main,"Main")
    def configuring(event):
        headerFrame.update()
        h=headerFrame.winfo_height()*hE
        w=headerFrame.winfo_width()*wE
        imag=ImageTk.PhotoImage(Image.open("assets\\Esperos.png").resize((int(h),int(w))))
        logo.config(imag=imag)
        logo.imag=imag


    Main=tk.Tk()
    Main.title("TeamManager.exe")
    mainCanvas=tk.Canvas(Main,height=1200,width=1400)
    mainCanvas.pack()
    Main.state("zoomed")
    Main.iconphoto(True,ImageTk.PhotoImage(Image.open("assets\\Esperos.png")))

    mainFrame=tk.Frame(Main,bg="#4e73c2")
    mainFrame.place(relheight=1,relwidth=1)

    headerFrame=headerFrame=tk.Frame(mainFrame,bg="light grey")
    headerFrame.place(relheight=0.35,relwidth=0.8,relx=0.1,rely=0)


    subHeaderFrame=tk.Frame(mainFrame,bg="grey")
    subHeaderFrame.place(relheight=0.65,relwidth=0.8,relx=0.1,rely=0.35)


    titleFrame=tk.Frame(headerFrame,bg="white")
    titleFrame.place(relwidth=0.7,relheight=0.4,relx=0.3,rely=0)


    menuFrame=tk.Frame(subHeaderFrame,bg="#494949")
    menuFrame.place(relwidth=0.3,relheight=1,relx=0,rely=0)


    menuLabel=tk.Label(menuFrame,text="Menu",fg="#fff",bg=menuFrame["bg"])
    menuLabel.place(relwidth=1,relheight=0.3,relx=0,rely=0)
    menuLabel.config(font=("Arial Black",42))


    athleteFrame=tk.Frame(menuFrame,bg="#3a3a3a")
    athleteFrame.place(relwidth=0.8,relx=0.1,relheight=0.2,rely=0.25)

    athleteButton=tk.Button(athleteFrame,text="Δεδομένα\nΜελών",command=initAthlete,bg="#494949",fg="#fff")
    athleteFrame.update()
    athleteE=38/athleteFrame.winfo_height()
    athleteButton.config(font=("Arial",38))
    athleteButton.place(relwidth=0.9,relheight=0.9,relx=0.05,rely=0.05)

    teamFrame=tk.Frame(menuFrame,bg="#3a3a3a")
    teamFrame.place(relwidth=0.8,relx=0.1,relheight=0.2,rely=0.55)

    teamButton=tk.Button(teamFrame,text="Δεδομένα\nΣυλόγου",command=initClub,bg="#494949",fg="#fff")
    teamButton.config(font=("Arial",38))
    teamButton.place(relwidth=0.9,relheight=0.9,relx=0.05,rely=0.05)

    
    imag=ImageTk.PhotoImage(Image.open("assets\\esperos.png").resize((350,350)))#BE CAREFUL
    logo=tk.Label(headerFrame,image=imag,bg="light grey")
    logo.place(relheight=1,relwidth=0.3,relx=0,rely=0)

    title=tk.Label(titleFrame,text="Team Manager:\nΈσπερος",bg="white")
    title.config(font=("Arial",28))
    title.place(relheight=1,relwidth=1,relx=0,rely=0)

    imaging=ImageTk.PhotoImage(Image.open("assets\\Welcome.png").resize((1075,662)))#BE CAREFUL
    welcomePic=tk.Label(subHeaderFrame,image=imaging)
    welcomePic.place(relwidth=0.7,relheight=1,rely=0,relx=0.3)

    backphoto=ImageTk.PhotoImage(Image.open("assets\\back.png").resize((75,75)))
    backButton=tk.Button(headerFrame,image=backphoto,command=goBack,bg="light grey",borderwidth=0)
    backButton.place(relheight=0.225,relwidth=0.05,relx=0.9,rely=0.7)
    
    forphoto=ImageTk.PhotoImage(Image.open("assets\\next.png").resize((75,75)))
    forwardButton=tk.Button(headerFrame,image=forphoto,command=goForward,bg="light grey",borderwidth=0)
    forwardButton.place(relheight=0.225,relwidth=0.05,relx=0.95,rely=0.7)

    Main.protocol("WM_DELETE_WINDOW",Exit)
    Main.mainloop()


if __name__=="__main__":
    data=of.run(True)
    main()