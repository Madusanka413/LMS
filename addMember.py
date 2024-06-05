from tkinter import *
from tkinter import messagebox
import sqlite3
con =sqlite3.connect('library.db')
cur=con.cursor()

class AddMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+250")
        self.title("Add Member")
        self.resizable(False,False)

        ########################## Frame ###############################
        #top Frame
        self.topFrame=Frame(self,height=150,bg='white')
        self.topFrame.pack(fill=X)
        #bottam Frame
        self.bottomFrame= Frame(self,height=600,bg='#345B63')
        self.bottomFrame.pack(fill=X)
        #heading,image
        self.top_image= PhotoImage(file='icon/user.png')
        top_image_lbl=Label(self.topFrame,image=self.top_image,bg='white',)
        top_image_lbl.place(x=250,y=55)
        heading=Label(self.topFrame,text='Add Member',font='arial',fg='white',bg='#345B63')
        heading.place(x=290,y=60)

        ################################## Entries and Labels##############################

        #membername
        self.lbl_name=Label(self.bottomFrame,text='Name :',font='arial',fg='white',bg='#345B63')
        self.lbl_name.place(x=40,y=40)
        self.ent_name=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_name.insert(0,'Please enter a book name')
        self.ent_name.place(x=150,y=45)

        #phone
        self.lbl_phone = Label(self.bottomFrame, text='Phone :', font='arial', fg='white', bg='#345B63')
        self.lbl_phone.place(x=40, y=80)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_phone.insert(0, 'Please enter a phone number')
        self.ent_phone.place(x=150, y=85)


        #button
        button=Button(self.bottomFrame,text='Add Member',command=self.addMember)
        button.place(x=270,y=120)

    def addMember(self):
        name = self.ent_name.get()
        phone = self.ent_phone.get()


        if (name and phone  !=""):
            try:
                query="INSERT INTO 'members'(member_name,member_phone)VALUES(?,?)"
                cur.execute(query,(name,phone))
                con.commit()
                messagebox.showinfo("Success","successfully added to database",icon='info')
            except:
                messagebox.showerror("Error","Cant add to database",icon='warning')
        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')



