from tkinter import *
from tkinter import messagebox
import sqlite3
con =sqlite3.connect('library.db')
cur=con.cursor()

class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+250")
        self.title("Add Book")
        self.resizable(False,False)

        ########################## Frame ###############################
        #top Frame
        self.topFrame=Frame(self,height=150,bg='white')
        self.topFrame.pack(fill=X)
        #bottam Frame
        self.bottomFrame= Frame(self,height=600,bg='#345B63')
        self.bottomFrame.pack(fill=X)
        #heading,image
        self.top_image= PhotoImage(file='icon/addbook.png')
        top_image_lbl=Label(self.topFrame,image=self.top_image,bg='white',)
        top_image_lbl.place(x=260,y=60)
        heading=Label(self.topFrame,text='Add Book',font='arial',fg='white',bg='#345B63')
        heading.place(x=290,y=60)

        ################################## Entries and Labels##############################

        #name
        self.lbl_name=Label(self.bottomFrame,text='Name :',font='arial',fg='white',bg='#345B63')
        self.lbl_name.place(x=40,y=40)
        self.ent_name=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_name.insert(0,'Please enter a book name')
        self.ent_name.place(x=150,y=45)

        #author
        self.lbl_author = Label(self.bottomFrame, text='Author :', font='arial', fg='white', bg='#345B63')
        self.lbl_author.place(x=40, y=80)
        self.ent_author = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_author.insert(0, 'Please enter a author name')
        self.ent_author.place(x=150, y=85)

        # page
        self.lbl_page = Label(self.bottomFrame, text='page :', font='arial', fg='white', bg='#345B63')
        self.lbl_page.place(x=40, y=120)
        self.ent_page = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_page.insert(0, 'Please enter a page size ')
        self.ent_page.place(x=150, y=125)

        # language
        self.lbl_language = Label(self.bottomFrame, text='language :', font='arial', fg='white', bg='#345B63')
        self.lbl_language.place(x=40, y=160)
        self.ent_language = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_language.insert(0, 'Please enter the language ')
        self.ent_language.place(x=150, y=165)

        #button
        button=Button(self.bottomFrame,text='Add Book',command=self.addBook)
        button.place(x=270,y=200)

    def addBook(self):
        name = self.ent_name.get()
        author = self.ent_author.get()
        page = self.ent_page.get()
        language=self.ent_language.get()

        if (name and author and page and language !=""):
            try:
                query="INSERT INTO 'books'(book_name,book_author,book_page,book_language)VALUES(?,?,?,?)"
                cur.execute(query,(name,author,page,language))
                con.commit()
                messagebox.showinfo("Success","successfully added to database",icon='info')
            except:
                messagebox.showerror("Error","Cant add to database",icon='warning')
        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')



