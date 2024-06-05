from tkinter import *
from tkinter import ttk
import sqlite3
import addBook, addMember,givebook
from tkinter import messagebox

con = sqlite3.connect('library.db')
cur = con.cursor()

class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__ (self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False,False)

        query="SELECT * FROM books WHERE book_status=0 "
        books =cur.execute(query).fetchall()
        book_list=[]
        for book in books:
            book_list.append(str(book[0])+"_"+book[1])

        query2="SELECT * FROM members"
        members =cur.execute(query2).fetchall()
        memeber_list=[]
        for member in members:
            memeber_list.append(str(member[0])+"_"+member[1])

        ########################## Frame ###############################
        # top Frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)
        # bottam Frame
        self.bottomFrame = Frame(self, height=600, bg='#345B63')
        self.bottomFrame.pack(fill=X)
        # heading,image
        self.top_image = PhotoImage(file='icon/user.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white', )
        top_image_lbl.place(x=250, y=55)
        heading = Label(self.topFrame, text='Land a Book', font='arial', fg='white', bg='#345B63')
        heading.place(x=290, y=60)

        ################################## Entries and Labels##############################

        # membername
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text=' Book :', font='arial', fg='white', bg='#345B63')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame,textvariable=self.book_name)
        self.combo_name['values']=book_list
        self.combo_name.place(x=150,y=45)




        # phone
        self.member_name = StringVar()
        self.lbl_phone = Label(self.bottomFrame, text='Member :', font='arial', fg='white', bg='#345B63')
        self.lbl_phone.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member['values']=memeber_list
        self.combo_member.place(x=150, y=85)


        # button
        button = Button(self.bottomFrame, text='Lend Book',command=self.lendbook)
        button.place(x=270, y=120)

    def lendbook(self):
        book_name=self.book_name.get()
        self.book_id=book_name.split('-')[0]
        member_name=self.member_name.get()

        if(book_name and member_name !=""):
            try:
                query="INSERT INTO 'borrows'(bbook_id,bmember_id) VALUES(?,?)"
                cur.execute(query,(book_name,member_name))
                con.commit()
                messagebox.showinfo("success","Successfuly added to database",icon='info')
                cur.execute("UPDATE book SET bool_status =? WHERE book_id=?",(1,self.book_id))
                con.commit()

            except:
                messagebox.showerror("Error", "cant add to data base", icon='warning')
        else:
            messagebox.showerror("Error","Fields cant be empty",icon='warning')
