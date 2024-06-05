from tkinter import *
from tkinter import ttk
import sqlite3
import addBook, addMember,givebook
from tkinter import messagebox

con = sqlite3.connect('library.db')
cur = con.cursor()


class Main(object):
    def __init__(self, master):
        self.master = master

        def displayStatistic(evt):
            count_books=cur.execute("SELECT count(book_id) FROM books").fetchall()
            count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
            taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status=1").fetchall()
            print(count_books)
            self.lbl_book_count.config(text='Total :'+str(count_books[0][0])+' books in library')
            self.lbl_member_count.config(text='Total member :' + str(count_members[0][0]))
            self.lbl_taken_count.config(text='Taken books :' + str(taken_books[0][0]))
            displayBooks(self)



        def displayBooks(self):
            books = cur.execute("SELECT * FROM books").fetchall()
            count = 0
            self.list_books.delete(0,END)
            for book in books:
                print(book)
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1

            def bookInfo(evt):

                value = str(self.list_books.get(self.list_books.curselection()))
                id = value.split('-')[0]
                book = cur.execute("SELECT * FROM books WHERE book_id=?", (id,))
                book_info = book.fetchall()
                print(book_info)
                self.list_details.delete(0, END)

                self.list_details.insert(0, "Book Name: " + book_info[0][1])
                self.list_details.insert(1, "Author: " + book_info[0][2])
                self.list_details.insert(2, "Page: " + book_info[0][3])
                self.list_details.insert(3, "Language: " + book_info[0][4])
                if book_info[0][5] == 0:
                    self.list_details.insert(4, "status : Available")
                else:
                    self.list_details.insert(4, "status : Not Available")

            def doubleClick(evt):
                global given_id
                value=str(self.list_books.get(self.list_books.curselection()))
                given_id=value.split('-')[0]
                give_book=GiveBook()



            self.list_books.bind('<<ListboxSelect>>', bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>',displayStatistic)
            #self.tabs.bind('<ButtonRelease-1>',displayBooks)
            self.list_books.bind('<Double-Button-1>',doubleClick)



        # Main frame
        mainFrame = Frame(self.master)
        mainFrame.pack()

        # Top frame
        topFrame = Frame(mainFrame, width=1350, height=70, bg='#112031', padx=20, relief=SUNKEN, borderwidth=2)
        topFrame.pack(side=TOP, fill=X)
        # centerFrame
        centerFrame = Frame(mainFrame, width=1350, relief=RIDGE, bg='#112031', height=680)
        centerFrame.pack(side=TOP)
        # center left Frame
        centerLeftFrame = Frame(centerFrame, width=900, height=700, bg='#112031', borderwidth=2, relief=SUNKEN)
        centerLeftFrame.pack(side=LEFT)
        # center Right Frame
        centerRightFrame = Frame(centerFrame, width=450, height=700, bg='#112031', borderwidth=2, relief=SUNKEN)
        centerRightFrame.pack()

        # search bar
        search_bar = LabelFrame(centerRightFrame, width=440, height=175, text='search', bg='#345B63', fg='white')
        search_bar.pack(fill=BOTH)
        self.lbl_search = Label(search_bar, text='Search :', font='arial', bg='#345B63', fg='white')
        self.lbl_search.grid(row=0, column=0, padx=20, pady=10)
        self.ent_search = Entry(search_bar, width=30, bd=10)
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
        self.btn_search = Button(search_bar, text='Search', font='arial', bg='#345B63', fg='white',command=self.searchBooks)
        self.btn_search.grid(row=0, column=4, padx=20, pady=10)

        # list_bar
        list_bar = LabelFrame(centerRightFrame, width=440, height=175, text='List', bg='#345B63', fg='white')
        list_bar.pack(fill=BOTH)
        lbl_list = Label(list_bar, text='Sort By', font='arial', fg='white', bg='#345B63')
        lbl_list.grid(row=0, column=2)
        self.listChoice = IntVar()
        rb1 = Radiobutton(list_bar, text='All Books',variable=self.listChoice, value=1, bg='#345B63', fg='black')
        rb2 = Radiobutton(list_bar, text='In Library',variable=self.listChoice, value=2, bg='#345B63', fg='black')
        rb3 = Radiobutton(list_bar, text='Borrowed Books',variable=self.listChoice, value=3, bg='#345B63', fg='black')
        rb1.grid(row=1, column=0)
        rb2.grid(row=1, column=1)
        rb3.grid(row=1, column=2)
        btn_list = Button(list_bar, text='List Books', bg='#345B63', fg='white', font='arial',command=self.listBook)
        btn_list.grid(row=1, column=3, padx=40, pady=10)

        # title and image
        image_bar = Frame(centerRightFrame, width=440, height=350, padx=120, pady=30, bg='#345B63')
        image_bar.pack(fill=BOTH)
        self.title_right = Label(image_bar, text='Welcome to our Library', font='arial 16 bold', fg='black')
        self.title_right.grid(row=0)
        self.img_library = PhotoImage(file='icon/library.png')
        self.lblImg = Label(image_bar, image=self.img_library)
        self.lblImg.grid(row=1)

        owner_bar = Frame(centerRightFrame, width=20, height=20, padx=180, pady=100, bg='#345B63')
        owner_bar.pack(fill=BOTH)
        self.owner_right = Label(owner_bar, text='©solution by madusanka', font=('arial 16 bold', 8), fg='black')
        self.owner_right.grid(row=2)

        ################################################################## TOOL BAR ############################################
        # add_book
        self.iconbook = PhotoImage(file='icon/addbook.png', height=70)
        self.btnbook = Button(topFrame, text='ADD BOOK', image=self.iconbook, padx=10, compound=LEFT, font='arial',
                              command=self.addBook)
        self.btnbook.pack(side=LEFT)

        # add member button
        self.iconmember = PhotoImage(file='icon/user.png', height=70)
        self.btnmember = Button(topFrame, text='ADD MEMBER', font='arial', padx=10, image=self.iconmember,
                                compound=LEFT, command=self.addMember)
        self.btnmember.pack(side=LEFT)

        # give book
        self.icongive = PhotoImage(file='icon/givebook.png', height=70)
        self.btngive = Button(topFrame, text='GIVE BOOK', font='arial', padx=10, image=self.icongive, compound=LEFT,command=self.giveBook)
        self.btngive.pack(side=LEFT)
        ###################################################################### TABS ############################################
        #################################### TAB 1 ##################################
        self.tabs = ttk.Notebook(centerLeftFrame, width=900, height=660)
        self.tabs.pack()
        self.tab1_icon = PhotoImage(file='icon/books.png')
        self.tab2_icon = PhotoImage(file='icon/members.png')
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text='Libarary Management', image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text='Statistics', image=self.tab2_icon, compound=LEFT)

        # list books
        self.list_books = Listbox(self.tab1, width=40, height=30, bd=5, font='arial')
        self.sb = Scrollbar(self.tab1, orient=VERTICAL)
        self.list_books.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
        self.sb.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=0, sticky=N + S + E)
        # list details
        self.list_details = Listbox(self.tab1, width=80, height=30, bd=5, font='arial')
        self.list_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)
        ######################### TAB 2 ######################################
        # statistic
        self.lbl_book_count = Label(self.tab2, text="", pady=20, font='arial', )
        self.lbl_book_count.grid(row=0)
        self.lbl_member_count = Label(self.tab2, text="", pady=20, font='arial')
        self.lbl_member_count.grid(row=1, sticky=W)
        self.lbl_taken_count = Label(self.tab2, text="", pady=20, font='arial')
        self.lbl_taken_count.grid(row=2, sticky=W)

        # funtion
        displayBooks(self)
        displayStatistic(self)

    def addBook(self):
        add = addBook.AddBook()

    def addMember(self):
        member = addMember.AddMember()

    def searchBooks(self):
        value = self.ent_search.get()
        search=cur.execute("SELECT * FROM books WHERE book_name LIKE ?",('%'+value+'%',)).fetchall()
        print(search)
        self.list_books.delete(0,END)
        count=0
        for book in search:
            self.list_books.insert(count,str(book[0])+"_"+book[1])
            count +=1

    def listBook(self):
        value = self.listChoice.get()
        if value == 1:
            allbooks =cur.execute("SELECT * FROM books").fetchall()
            self.list_books.delete(0,END)

            count=0
            for book in allbooks:
                self.list_books.insert(count,str(book[0])+"_"+book[1])
                count +=1
        elif value == 2:
            book_in_library = cur.execute("SELECT * FROM books WHERE book_status =?",(0,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in book_in_library :
                self.list_books.insert(count, str(book[0]) + "_" + book[1])
                count += 1
        else:
            taken_books = cur.execute("SELECT * FROM books WHERE book_status =?",(1,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in taken_books:
                self.list_books.insert(count, str(book[0]) + "_" + book[1])
                count += 1

    def giveBook(self):
        give_book =givebook.GiveBook()


class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__ (self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False,False)
        global given_id
        self.book_id=int(given_id)
        query="SELECT * FROM books"
        books =cur.execute(query).fetchall()
        book_list=[]
        for book in books:
            book_list.append(str(book[0])+"-"+book[1])

        query2="SELECT * FROM members"
        members =cur.execute(query2).fetchall()
        memeber_list=[]
        for member in members:
            memeber_list.append(str(member[0])+"-"+member[1])

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
        heading = Label(self.topFrame, text='Add Member', font='arial', fg='white', bg='#345B63')
        heading.place(x=290, y=60)

        ################################## Entries and Labels##############################

        # membername
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text=' Book :', font='arial', fg='white', bg='#345B63')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame,textvariable=self.book_name)
        self.combo_name['values']=book_list
        self.combo_name.current(self.book_id-1)
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
                messagebox.showerror("Error", "cant add to data base uhg", icon='warning')
        else:
            messagebox.showerror("Error","Fields cant be empty",icon='warning')


def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1350x750+350+250")  # Corrected format
    root.iconbitmap('icon/icon.ico')
    root.mainloop()


if __name__ == '__main__':
    main()
