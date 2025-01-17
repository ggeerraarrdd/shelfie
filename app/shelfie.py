# Python Standard Library
from tkinter import *
from tkinter import messagebox, ttk, font
import logging
import sqlite3

# Third-Party Libraries
from PIL import ImageTk, Image

# Local
from config import DATABASE_CONFIG
from config import LOGGING_CONFIG










class Shelfie:

    def __init__(self, root):
        self.window = root
        self.window.title('Shelfie v0.3 ~ A Library Management System')
        self.window.geometry("1280x720")
        self.window.resizable(False, False)

        # ===============================================
        # MAIN FRAME OF START PAGE
        # ===============================================
        frame_1 = Frame(self.window, bg='white')
        frame_1.place(x=0, y=0, width=1000, relheight=1)

        # Content in Main Frame
        self.image = ImageTk.PhotoImage(Image.open('assets/images/library.png'))
        splash = Label(image=self.image)
        splash.place(x=-5, y=-5)


        # ===============================================
        # SIDE FRAME OF START PAGE
        # ===============================================

        # Frame 2
        frame_2 = Frame(self.window, bg='cyan')
        frame_2.place(x=1000, y=0, relwidth=1, relheight=1)

        garamond50bold = font.Font(family='Garamond', size=50, weight='bold')
        title = Label(frame_2, text='Shelfie!', bg='cyan', font=garamond50bold, borderwidth=0)
        title.place(x=0, y=28, width=280)

        close_button = Button(frame_2, text='Close', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.window.quit)
        close_button.place(x=90, y=625, width=100)

        # noinspection PyUnusedLocal
        def click_login(event):
            login.configure(state=NORMAL)
            login.delete(0, END)
            login.unbind('<Button-1>', clicked_login)

        # noinspection PyUnusedLocal
        def click_password(event):
            password.configure(state=NORMAL)
            password.delete(0, END)
            password.unbind('<Button-1>', clicked_password)
            password.config(show='*')

        def click_signin():
            validation = login.get() == LOGGING_CONFIG['username'] and password.get() == LOGGING_CONFIG['password']
            if validation:
                print(validation)
                self.Library_Page()
            else:
                print(validation)
                incorrect = Label(frame_4, text='Incorrect login or password.', bg='cyan', fg='#F34C50', font='Helvetica 14', borderwidth=0, anchor=CENTER)
                incorrect.place(x=0, y=150, width=200)
            return

        # Frame 4
        frame_4 = Frame(self.window, bg='cyan', borderwidth=0, pady=30)
        frame_4.place(x=1040, y=210, height=250, width=200)

        login = Entry(frame_4, bd=2, highlightbackground='cyan', highlightthickness=0)
        login.place(x=5, y=0, width=190)
        login.insert(0, 'borges')
        clicked_login = login.bind('<Button-1>', click_login)

        password = Entry(frame_4, bd=2, highlightbackground='cyan', highlightthickness=0)
        password.place(x=5, y=50, width=190)
        password.insert(0, 'babel410')
        clicked_password = password.bind('<Button-1>', click_password)

        update_button = Button(frame_4, text='Sign in', bd=2, highlightbackground='cyan', highlightthickness=0, width=10, command=click_signin)
        update_button.place(x=48, y=100, width=100)


    def Library_Page(self):

        # ===============================================
        # MAIN FRAME OF LIBRARY PAGE
        # ===============================================
        frame_1 = Frame(self.window, bg="white")
        frame_1.place(x=0, y=0, width=1000, relheight=1)

        # Page Header
        title = Label(frame_1, text='My Library', bg="white", font='Garamond 25 bold', borderwidth=0, anchor="w")
        title.place(x=100, y=50, width=280)
        title_separator = ttk.Separator(orient="horizontal")
        title_separator.place(x=100, y=80, height=2, width=800)

        # Add style to Treeview
        style = ttk.Style()
        style.theme_use('aqua')
        style.configure('Treeview', background='gainsboro', foreground='black', rowheight=25, fieldbackground='gainsboro')
        style.map('Treeview', background=[('selected', 'cyan')])

        # Create Treeview Frame inside frame_1
        tree_frame = Frame(self.window)
        tree_frame.place(x=100, y=115, height=475, width=800)

        # Create Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        my_tree = ttk.Treeview(tree_frame, height=18, yscrollcommand=tree_scroll.set)

        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ('Record', 'Title', 'Author', 'Date')

        # Format Our Columns
        my_tree.column('#0', width=0, stretch=NO)
        my_tree.column('Record', anchor=W, width=75)
        my_tree.column('Title', anchor=W, width=435)
        my_tree.column('Author', anchor=W, width=175)
        my_tree.column('Date', anchor=W, width=100)

        # Create Headings
        my_tree.heading('#0', text='', anchor=W)
        my_tree.heading('Record', text='Record ID', anchor=W)
        my_tree.heading('Title', text='Title', anchor=W)
        my_tree.heading('Author', text='Author', anchor=W)
        my_tree.heading('Date', text='Date Added', anchor=W)

        connection = sqlite3.connect(DATABASE_CONFIG['path'])
        curs = connection.cursor()

        curs.execute("SELECT rowid, title, name_first || ' ' || name_last, date(date_created) FROM shelfie ORDER BY rowid ASC;")
        data = curs.fetchall()
        curs.execute("SELECT count(*) FROM shelfie;")
        data_count = curs.fetchone()
        curs.close()
        connection.close()

        count = 0

        for record in data:
            my_tree.insert(parent='', index='end', iid=str(count), text='',
                           values=(record[0], record[1], record[2], record[3]))
            count += 1

        # Pack the treeview to the screen
        my_tree.place(x=0, y=0)


        def click_read_button():
            try:
                selected_item = my_tree.focus()
                selected_item_values = my_tree.item(selected_item)
                record_number = selected_item_values.get('values')[0]
                print(record_number)
                self.Read_Page(record_number)
            except Exception as e:
                please_select = Label(frame_4, text='Please select a record.', bg='cyan', font='Helvetica 14', borderwidth=0, anchor=CENTER)
                please_select.place(x=2, y=220, width=196)
                logging.exception(e)


        def click_update_button():
            try:
                selected_item = my_tree.focus()
                selected_item_values = my_tree.item(selected_item)
                update_record_number = selected_item_values.get('values')[0]
                print(update_record_number)
                update_message = ''
                self.Update_Page(update_record_number, update_message)
            except Exception as e:
                please_select = Label(frame_4, text='Please select a record.', bg='cyan', font='Helvetica 14', borderwidth=0, anchor=CENTER)
                please_select.place(x=2, y=220, width=196)
                logging.exception(e)


        def click_delete_button():
            try:
                selected_item = my_tree.focus()
                selected_item_values = my_tree.item(selected_item)
                delete_record_number = selected_item_values.get('values')[0]
                print(delete_record_number)
                self.Delete_Page(delete_record_number)
            except Exception as e:
                please_select = Label(frame_4, text='Please select a record.', bg='cyan', font='Helvetica 14', borderwidth=0, anchor=CENTER)
                please_select.place(x=2, y=220, width=196)
                logging.exception(e)


        # Data count
        data_count_text = f'Total: %s records' % data_count
        count = Label(frame_1, text=data_count_text, bg="white", font='Helvetica 15', borderwidth=0, relief="solid", anchor='e')
        count.place(x=600, y=58, width=300)

        # Navigation Buttons
        nav_separator = ttk.Separator(orient="horizontal")
        nav_separator.place(x=100, y=615, height=2, width=800)


        # ===============================================
        # SIDE FRAME OF LIBRARY PAGE
        # ===============================================

        # Frame 2
        frame_2 = Frame(self.window, bg='cyan')
        frame_2.place(x=1000, y=0, relwidth=1, relheight=1)

        title = Label(frame_2, text='Shelfie!', bg='cyan', font='Garamond 50 bold', borderwidth=0, relief='solid')
        title.place(x=0, y=28, width=280)
        # shelfie_separator = ttk.Separator(frame_2, orient='horizontal')
        # shelfie_separator.place(x=40, y=80, height=2, width=200)

        about_button = Button(frame_2, text='About', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.About_Page)
        about_button.place(x=90, y=485, width=100)

        close_button = Button(frame_2, text='Close', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.window.quit)
        close_button.place(x=90, y=625, width=100)


        # Frame 3
        frame_3 = Frame(self.window, bg='cyan', borderwidth=0, relief='ridge')
        frame_3.place(x=1040, y=110, height=100, width=200)

        lib = LabelFrame(frame_3, text='Browse', bg='cyan', pady=10)
        lib.place(height=75, width=200)

        library_button = Button(lib, text='My Library', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.Library_Page)
        library_button.place(x=48, y=0, width=100)
        library_button.config(state='disabled')


        # Frame 4
        frame_4 = Frame(self.window, borderwidth=0, relief='ridge')
        frame_4.place(x=1040, y=210, height=250, width=200)

        crud = LabelFrame(frame_4, text='Record', bg='cyan', pady=10)
        crud.place(height=250, width=200)

        add_button = Button(crud, text='Add', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.Create_Page)
        add_button.place(x=48, y=0, width=100)

        view_button = Button(crud, text='View', bd=2, highlightbackground='cyan', highlightthickness=0, width=10, command=click_read_button)
        view_button.place(x=48, y=50, width=100)

        update_button = Button(crud, text='Update', bd=2, highlightbackground='cyan', highlightthickness=0, width=10, command=click_update_button)
        update_button.place(x=48, y=100, width=100)

        delete_button = Button(crud, text='Delete', bd=2, highlightbackground='cyan', highlightthickness=0, width=10, command=click_delete_button)
        delete_button.place(x=48, y=150, width=100)


    def Create_Page(self):

        # ===============================================
        # MAIN FRAME OF ADD PAGE
        # ===============================================
        frame_1 = Frame(self.window, bg='white')
        frame_1.place(x=0, y=0, width=1000, relheight=1)

        # Content in Main Frame

        # Title of Page
        title = Label(frame_1, text='Add Record', bg='white', font='Garamond 25 bold', borderwidth=0, anchor='w')
        title.place(x=100, y=50, width=280)
        title_separator = ttk.Separator(orient='horizontal')
        title_separator.place(x=100, y=80, height=2, width=800)

        # Main Content of Page

        isbn_label = Label(frame_1, text='ISBN', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        isbn_label.place(x=100, y=115, width=100)
        isbn_entry = Entry(frame_1, width=200)
        isbn_entry.place(x=100, y=140, width=150)

        title_label = Label(frame_1, text='Title', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        title_label.place(x=100, y=200, width=100)
        title_entry = Entry(frame_1, width=50)
        title_entry.place(x=100, y=225, width=800)

        first_label = Label(frame_1, text='Author - First Name', bg="white", font='Helvetica 15 bold', anchor="w",  padx=10)
        first_label.place(x=100, y=275, width=300)
        first_entry = Entry(frame_1, width=50)
        first_entry.place(x=100, y=300, width=300)

        last_label = Label(frame_1, text='Author - Last Name', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        last_label.place(x=425, y=275, width=300)
        last_entry = Entry(frame_1, width=50)
        last_entry.place(x=425, y=300, width=300)

        binding_label = Label(frame_1, text='Binding', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        binding_label.place(x=750, y=275, width=150)
        binding = StringVar()
        binding_options = OptionMenu(frame_1, binding, 'Hardcover', 'Softcover')
        binding.set(' ')
        binding_options.place(x=750, y=300, width=150)

        publisher_label = Label(frame_1, text='Publisher', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        publisher_label.place(x=100, y=350, width=300)
        publisher_entry = Entry(frame_1, width=50)
        publisher_entry.place(x=100, y=375, width=300)

        published_label = Label(frame_1, text='Published Date', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        published_label.place(x=425, y=350, width=300)
        published_entry = Entry(frame_1, width=50)
        published_entry.place(x=425, y=375, width=300)

        notes_label = Label(frame_1, text='Notes', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        notes_label.place(x=100, y=425, width=300)
        notes_entry = Text(frame_1, height=8, width=50, wrap=WORD)
        notes_entry.place(x=100, y=450, width=300)

        def clear_fields():
            isbn_entry.delete(0, END)
            title_entry.delete(0, END)
            first_entry.delete(0, END)
            last_entry.delete(0, END)
            publisher_entry.delete(0, END)
            published_entry.delete(0, END)
            binding.set(' ')
            notes_entry.delete('1.0', 'end-1c')

        def click_save():
            if title_entry.get() == '':
                messagebox.showerror("Error!", "The title field is required!")
            elif isbn_entry.get() is not None and len(isbn_entry.get()) != 13:
                messagebox.showerror("Error!", "ISBN must be 13 digits!")
            else:
                try:
                    connection = sqlite3.connect(DATABASE_CONFIG['path'])
                    curs = connection.cursor()
                    curs.execute(
                        "INSERT INTO shelfie (isbn, title, name_first, name_last, publisher, date_publication, binding, notes) values( ?, ?, ?, ?, ?, ?, ?, ?);",
                        (
                            isbn_entry.get(),
                            title_entry.get(),
                            first_entry.get(),
                            last_entry.get(),
                            publisher_entry.get(),
                            published_entry.get(),
                            binding.get(),
                            notes_entry.get('1.0', 'end-1c'))
                    )
                    connection.commit()
                    connection.close()
                    please_select = Label(frame_4, text='Record has been saved!', bg='cyan', font='Helvetica 14', borderwidth=0, anchor=CENTER)
                    please_select.place(x=2, y=220, width=196)
                    clear_fields()

                except Exception as e:
                    messagebox.showerror("Error!", f"Error due to {str(e)}")


        # Navigation Buttons
        nav_separator = ttk.Separator(orient="horizontal")
        nav_separator.place(x=100, y=615, height=2, width=800)

        button_prev = Button(frame_1, text='<< Back to Library', highlightbackground='white', highlightthickness=0, command=self.Library_Page)
        button_prev.place(x=100, y=625, width=150)

        button_save = Button(frame_1, text='Save New Record', highlightbackground='white', highlightthickness=0, command=click_save)
        button_save.place(x=750, y=625, width=150)


        # ===============================================
        # SIDE FRAME OF ADD PAGE
        # ===============================================

        # Frame 2
        frame_2 = Frame(self.window, bg='cyan')
        frame_2.place(x=1000, y=0, relwidth=1, relheight=1)

        title = Label(frame_2, text='Shelfie!', bg='cyan', font='Garamond 50 bold', borderwidth=0, relief='solid')
        title.place(x=0, y=28, width=280)
        # shelfie_separator = ttk.Separator(frame_2, orient='horizontal')
        # shelfie_separator.place(x=40, y=80, height=2, width=200)

        about_button = Button(frame_2, text='About', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.About_Page)
        about_button.place(x=90, y=485, width=100)

        close_button = Button(frame_2, text='Close', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.window.quit)
        close_button.place(x=90, y=625, width=100)


        # Frame 3
        frame_3 = Frame(self.window, bg='cyan', borderwidth=0, relief='ridge')
        frame_3.place(x=1040, y=110, height=100, width=200)

        lib = LabelFrame(frame_3, text='Browse', bg='cyan', pady=10)
        lib.place(height=75, width=200)

        library_button = Button(lib, text='My Library', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.Library_Page)
        library_button.place(x=48, y=0, width=100)


        # Frame 4
        frame_4 = Frame(self.window, borderwidth=0, relief='ridge')
        frame_4.place(x=1040, y=210, height=250, width=200)

        crud = LabelFrame(frame_4, text='Record', bg='cyan', pady=10)
        crud.place(height=250, width=200)

        add_button = Button(crud, text='Add', bd=2, highlightbackground='cyan', highlightthickness=0)
        add_button.place(x=48, y=0, width=100)
        add_button.config(state='disabled')

        view_button = Button(crud, text='View', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        view_button.place(x=48, y=50, width=100)
        view_button.config(state='disabled')

        update_button = Button(crud, text='Update', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        update_button.place(x=48, y=100, width=100)
        update_button.config(state='disabled')

        delete_button = Button(crud, text='Delete', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        delete_button.place(x=48, y=150, width=100)
        delete_button.config(state='disabled')


    def Read_Page(self, record_number):

        # ===============================================
        # MAIN FRAME OF READ PAGE
        # ===============================================
        frame_1 = Frame(self.window, bg="white")
        frame_1.place(x=0, y=0, width=1000, relheight=1)

        # PAGE HEADER
        title = Label(frame_1, text='View Record', bg="white", font='Garamond 25 bold', borderwidth=0, anchor="w")
        title.place(x=100, y=50, width=280)
        title_separator = ttk.Separator(orient="horizontal")
        title_separator.place(x=100, y=80, height=2, width=800)

        # Establish a connection to the database by creating a cursor object
        connection = sqlite3.connect(DATABASE_CONFIG['path'])
        curs = connection.cursor()
        curs.execute("SELECT rowid, * FROM shelfie WHERE rowid = ?;", [record_number])
        single_record = curs.fetchone()
        curs.close()
        connection.close()

        # This replaces empty values or None with an empty string.
        # Apparently Tkinter widgets cannot represent the value None.
        single_record_view = []
        for i in single_record:
            if i is None:
                single_record_view.append('')
            else:
                single_record_view.append(i)

        print(single_record_view)

        # Main Content of Page

        isbn_label = Label(frame_1, text='ISBN', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        isbn_label.place(x=100, y=115, width=100)
        isbn_entry = Entry(frame_1, width=200)
        isbn_entry.place(x=100, y=140, width=150)
        isbn_entry.insert(0, single_record_view[1])
        isbn_entry.config(state='disabled', disabledforeground='black')

        record_label = Label(frame_1, text='Record #', bg="white", font='Helvetica 15', anchor="w", padx=10)
        record_label.place(x=400, y=115, width=100)
        record_entry = Entry(frame_1, width=200)
        record_entry.place(x=400, y=140, width=150)
        record_entry.insert(0, single_record_view[0])
        record_entry.config(state='disabled', disabledforeground='black')

        added_label = Label(frame_1, text='Date Added', bg="white", font='Helvetica 15', anchor="w", padx=10)
        added_label.place(x=575, y=115, width=100)
        added_entry = Entry(frame_1, width=200)
        added_entry.place(x=575, y=140, width=150)
        added_entry.insert(0, single_record_view[9])
        added_entry.config(state='disabled', disabledforeground='black')

        update_label = Label(frame_1, text='Last Update', bg="white", font='Helvetica 15', anchor="w", padx=10)
        update_label.place(x=750, y=115, width=150)
        update_entry = Entry(frame_1, width=150)
        update_entry.place(x=750, y=140, width=150)
        update_entry.insert(0, single_record_view[10])
        update_entry.config(state='disabled', disabledforeground='black')

        title_label = Label(frame_1, text='Title', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        title_label.place(x=100, y=200, width=100)
        title_entry = Entry(frame_1, width=50)
        title_entry.place(x=100, y=225, width=800)
        title_entry.insert(0, single_record_view[2])
        title_entry.config(state='disabled', disabledforeground='black')

        first_label = Label(frame_1, text='Author - First Name', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        first_label.place(x=100, y=275, width=300)
        first_entry = Entry(frame_1, width=50)
        first_entry.place(x=100, y=300, width=300)
        first_entry.insert(0, single_record_view[3])
        first_entry.config(state='disabled', disabledforeground='black')

        last_label = Label(frame_1, text='Author - Last Name', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        last_label.place(x=425, y=275, width=300)
        last_entry = Entry(frame_1, width=50)
        last_entry.place(x=425, y=300, width=300)
        last_entry.insert(0, single_record_view[4])
        last_entry.config(state='disabled', disabledforeground='black')

        binding_label = Label(frame_1, text='Binding', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        binding_label.place(x=750, y=275, width=150)
        clicked = StringVar(value=single_record_view[7])
        binding_options = OptionMenu(frame_1, clicked, 'Hardcover', 'Softcover')
        binding_options.place(x=750, y=300, width=150)
        binding_options.config(state='disabled', disabledforeground='black')

        publisher_label = Label(frame_1, text='Publisher', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        publisher_label.place(x=100, y=350, width=300)
        publisher_entry = Entry(frame_1, width=50)
        publisher_entry.place(x=100, y=375, width=300)
        publisher_entry.insert(0, single_record_view[5])
        publisher_entry.config(state='disabled', disabledforeground='black')

        published_label = Label(frame_1, text='Published Date', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        published_label.place(x=425, y=350, width=300)
        published_entry = Entry(frame_1, width=50)
        published_entry.place(x=425, y=375, width=300)
        published_entry.insert(0, single_record_view[6])
        published_entry.config(state='disabled', disabledforeground='black')

        notes_label = Label(frame_1, text='Notes', bg="white", font='Helvetica 15 bold', anchor='w', padx=10)
        notes_label.place(x=100, y=425, width=300)
        notes_entry = Text(frame_1, height=7, width=50, font='Helvetica 13', wrap=WORD)
        notes_entry.place(x=100, y=450, width=300)
        notes_entry.insert('1.0', single_record_view[8])
        notes_entry.config(state='disabled')

        # Navigation Buttons
        nav_separator = ttk.Separator(orient="horizontal")
        nav_separator.place(x=100, y=615, height=2, width=800)

        button_prev = Button(frame_1, text='<< Back to Library', highlightbackground='white', highlightthickness=0, command=self.Library_Page)
        button_prev.place(x=100, y=625, width=150)


        # ===============================================
        # SIDE FRAME OF READ PAGE
        # ===============================================

        # Frame 2
        frame_2 = Frame(self.window, bg='cyan')
        frame_2.place(x=1000, y=0, relwidth=1, relheight=1)

        title = Label(frame_2, text='Shelfie!', bg='cyan', font='Garamond 50 bold', borderwidth=0, relief='solid')
        title.place(x=0, y=28, width=280)
        # shelfie_separator = ttk.Separator(frame_2, orient='horizontal')
        # shelfie_separator.place(x=40, y=80, height=2, width=200)

        about_button = Button(frame_2, text='About', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.About_Page)
        about_button.place(x=90, y=485, width=100)

        close_button = Button(frame_2, text='Close', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.window.quit)
        close_button.place(x=90, y=625, width=100)


        # Frame 3
        frame_3 = Frame(self.window, bg='cyan', borderwidth=0, relief='ridge')
        frame_3.place(x=1040, y=110, height=100, width=200)

        lib = LabelFrame(frame_3, text='Browse', bg='cyan', pady=10)
        lib.place(height=75, width=200)

        library_button = Button(lib, text='My Library', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.Library_Page)
        library_button.place(x=48, y=0, width=100)


        # Frame 4
        frame_4 = Frame(self.window, borderwidth=0, relief='ridge')
        frame_4.place(x=1040, y=210, height=250, width=200)

        crud = LabelFrame(frame_4, text='Record', bg='cyan', pady=10)
        crud.place(height=250, width=200)

        add_button = Button(crud, text='Add', bd=2, highlightbackground='cyan', highlightthickness=0)
        add_button.place(x=48, y=0, width=100)
        add_button.config(state='disabled')

        view_button = Button(crud, text='View', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        view_button.place(x=48, y=50, width=100)
        view_button.config(state='disabled')

        update_button = Button(crud, text='Update', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        update_button.place(x=48, y=100, width=100)
        update_button.config(state='disabled')

        delete_button = Button(crud, text='Delete', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        delete_button.place(x=48, y=150, width=100)
        delete_button.config(state='disabled')


    def Update_Page(self, record_number, update_message):

        # ===============================================
        # MAIN FRAME OF UPDATE RECORD PAGE
        # ===============================================
        frame_1 = Frame(self.window, bg="white")
        frame_1.place(x=0, y=0, width=1000, relheight=1)

        # Content in Main Frame

        # Establish a connection to the database by creating a cursor object
        connection = sqlite3.connect(DATABASE_CONFIG['path'])
        curs = connection.cursor()
        curs.execute("SELECT rowid, * FROM shelfie WHERE rowid = ?;", [record_number])
        single_record = curs.fetchone()
        curs.close()
        connection.close()

        # This replaces empty values or None with an empty string.
        # Apparently Tkinter widgets cannot represent the value None.
        single_record_view = []
        for i in single_record:
            if i is None:
                single_record_view.append('')
            else:
                single_record_view.append(i)

        print(single_record_view)

        # Title of Page
        title = Label(frame_1, text='Update Record', bg="white", font='Garamond 25 bold', borderwidth=0, anchor="w")
        title.place(x=100, y=50, width=280)
        title_separator = ttk.Separator(orient="horizontal")
        title_separator.place(x=100, y=80, height=2, width=800)

        # Main Content of Page
        isbn_label = Label(frame_1, text='ISBN', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        isbn_label.place(x=100, y=115, width=100)
        isbn_entry = Entry(frame_1, width=200)
        isbn_entry.place(x=100, y=140, width=150)
        isbn_entry.insert(0, single_record_view[1])

        record_label = Label(frame_1, text='Record #', bg="white", font='Helvetica 15', anchor="w", padx=10)
        record_label.place(x=400, y=115, width=100)
        record_entry = Entry(frame_1, width=200)
        record_entry.place(x=400, y=140, width=150)
        record_entry.insert(0, single_record_view[0])
        record_entry.config(state='disabled', disabledforeground='black')

        added_label = Label(frame_1, text='Date Added', bg="white", font='Helvetica 15', anchor="w", padx=10)
        added_label.place(x=575, y=115, width=100)
        added_entry = Entry(frame_1, width=200)
        added_entry.place(x=575, y=140, width=150)
        added_entry.insert(0, single_record_view[9])
        added_entry.config(state='disabled', disabledforeground='black')

        update_label = Label(frame_1, text='Last Update', bg="white", font='Helvetica 15', anchor="w", padx=10)
        update_label.place(x=750, y=115, width=150)
        update_entry = Entry(frame_1, width=150)
        update_entry.place(x=750, y=140, width=150)
        update_entry.insert(0, single_record_view[10])
        update_entry.config(state='disabled', disabledforeground='black')

        title_label = Label(frame_1, text='Title', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        title_label.place(x=100, y=200, width=100)
        title_entry = Entry(frame_1, width=50)
        title_entry.place(x=100, y=225, width=800)
        title_entry.insert(0, single_record_view[2])

        first_label = Label(frame_1, text='Author - First Name', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        first_label.place(x=100, y=275, width=300)
        first_entry = Entry(frame_1, width=50)
        first_entry.place(x=100, y=300, width=300)
        first_entry.insert(0, single_record_view[3])

        last_label = Label(frame_1, text='Author - Last Name', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        last_label.place(x=425, y=275, width=300)
        last_entry = Entry(frame_1, width=50)
        last_entry.place(x=425, y=300, width=300)
        last_entry.insert(0, single_record_view[4])

        binding_label = Label(frame_1, text='Binding', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        binding_label.place(x=750, y=275, width=150)
        clicked = StringVar(value=single_record_view[7])
        binding_options = OptionMenu(frame_1, clicked, 'Hardcover', 'Softcover')
        binding_options.place(x=750, y=300, width=150)

        publisher_label = Label(frame_1, text='Publisher', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        publisher_label.place(x=100, y=350, width=300)
        publisher_entry = Entry(frame_1, width=50)
        publisher_entry.place(x=100, y=375, width=300)
        publisher_entry.insert(0, single_record_view[5])

        published_label = Label(frame_1, text='Published Date', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        published_label.place(x=425, y=350, width=300)
        published_entry = Entry(frame_1, width=50)
        published_entry.place(x=425, y=375, width=300)
        published_entry.insert(0, single_record_view[6])

        notes_label = Label(frame_1, text='Notes', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        notes_label.place(x=100, y=425, width=300)
        notes_entry = Text(frame_1, height=7, width=50, font='Helvetica 13', wrap=WORD)
        notes_entry.place(x=100, y=450, width=300)
        notes_entry.insert('1.0', single_record_view[8])


        def click_update():
            new_update = single_record_view[1] == int(isbn_entry.get()) and \
                         single_record_view[2] == title_entry.get() and \
                         single_record_view[3] == first_entry.get() and \
                         single_record_view[4] == last_entry.get() and \
                         single_record_view[7] == clicked.get() and \
                         single_record_view[5] == publisher_entry.get() and \
                         str(single_record_view[6]) == str(published_entry.get()) and \
                         single_record_view[8] == notes_entry.get('1.0', 'end-1c')

            if title_entry.get() == '':
                messagebox.showerror("Error!", "The title field is required!")
            elif new_update:
                message_no_update = 'Nothing to update!'
                update_none = Label(frame_4, text=message_no_update, bg='cyan', font='Helvetica 14', borderwidth=0, anchor=CENTER)
                update_none.place(x=2, y=220, width=196)
            else:
                try:
                    connection = sqlite3.connect(DATABASE_CONFIG['path'])
                    c = connection.cursor()
                    c.execute(
                        """UPDATE shelfie SET 
                                    isbn = %s,
                                    title = %s,
                                    name_first = %s,
                                    name_last = %s,
                                    publisher = %s,
                                    date_publication = %s,
                                    binding = %s,
                                    notes = %s,
                                    date_updated = current_timestamp
                        WHERE rowid = %s;""",
                        (
                            isbn_entry.get(),
                            title_entry.get(),
                            first_entry.get(),
                            last_entry.get(),
                            publisher_entry.get(),
                            published_entry.get(),
                            clicked.get(),
                            notes_entry.get('1.0', 'end-1c'),
                            record_entry.get())
                    )
                    connection.commit()
                    connection.close()

                    update_done = 'Record #' + record_entry.get() + ' is updated!'
                    self.Update_Page(record_number, update_done)

                except Exception as e:
                    messagebox.showerror("Error!", f"Error due to {str(e)}")


        # Navigation Buttons
        nav_separator = ttk.Separator(orient="horizontal")
        nav_separator.place(x=100, y=615, height=2, width=800)

        button_prev = Button(frame_1, text='<< Back to Library', highlightbackground='white', highlightthickness=0, command=self.Library_Page)
        button_prev.place(x=100, y=625, width=150)

        button_back = Button(frame_1, text='Confirm Update', highlightbackground='white', highlightthickness=0, command=click_update)
        button_back.place(x=750, y=625, width=150)


        # ===============================================
        # SIDE FRAME OF UPDATE PAGE
        # ===============================================

        # Frame 2
        frame_2 = Frame(self.window, bg='cyan')
        frame_2.place(x=1000, y=0, relwidth=1, relheight=1)

        title = Label(frame_2, text='Shelfie!', bg='cyan', font='Garamond 50 bold', borderwidth=0, relief='solid')
        title.place(x=0, y=28, width=280)
        # shelfie_separator = ttk.Separator(frame_2, orient='horizontal')
        # shelfie_separator.place(x=40, y=80, height=2, width=200)

        about_button = Button(frame_2, text='About', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.About_Page)
        about_button.place(x=90, y=485, width=100)

        close_button = Button(frame_2, text='Close', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.window.quit)
        close_button.place(x=90, y=625, width=100)


        # Frame 3
        frame_3 = Frame(self.window, bg='cyan', borderwidth=0, relief='ridge')
        frame_3.place(x=1040, y=110, height=100, width=200)

        lib = LabelFrame(frame_3, text='Browse', bg='cyan', pady=10)
        lib.place(height=75, width=200)

        library_button = Button(lib, text='My Library', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.Library_Page)
        library_button.place(x=48, y=0, width=100)


        # Frame 4
        frame_4 = Frame(self.window, borderwidth=0, relief='ridge')
        frame_4.place(x=1040, y=210, height=250, width=200)

        crud = LabelFrame(frame_4, text='Record', bg='cyan', pady=10)
        crud.place(height=250, width=200)

        add_button = Button(crud, text='Add', bd=2, highlightbackground='cyan', highlightthickness=0)
        add_button.place(x=48, y=0, width=100)
        add_button.config(state='disabled')

        view_button = Button(crud, text='View', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        view_button.place(x=48, y=50, width=100)
        view_button.config(state='disabled')

        update_button = Button(crud, text='Update', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        update_button.place(x=48, y=100, width=100)
        update_button.config(state='disabled')

        delete_button = Button(crud, text='Delete', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        delete_button.place(x=48, y=150, width=100)
        delete_button.config(state='disabled')

        message_update = update_message
        update_saved = Label(frame_4, text=message_update, bg='cyan', font='Helvetica 14', borderwidth=0, anchor=CENTER)
        update_saved.place(x=2, y=220, width=196)


    def Delete_Page(self, record_number):

        # ===============================================
        # MAIN FRAME OF DELETE RECORD PAGE
        # ===============================================
        frame_1 = Frame(self.window, bg="white")
        frame_1.place(x=0, y=0, width=1000, relheight=1)

        # Content in Main Frame

        # Establish a connection to the database by creating a cursor object
        connection = sqlite3.connect(DATABASE_CONFIG['path'])
        curs = connection.cursor()
        curs.execute("SELECT rowid, * FROM shelfie WHERE rowid = ?;", [record_number])
        single_record = curs.fetchone()
        curs.close()
        connection.close()

        # This replaces empty values or None with an empty string.
        # Apparently Tkinter widgets cannot represent the value None.
        single_record_view = []
        for i in single_record:
            if i is None:
                single_record_view.append('')
            else:
                single_record_view.append(i)

        print(single_record_view)

        # Title of Page
        title = Label(frame_1, text='Delete Record', bg="white", font='Garamond 25 bold', borderwidth=0, anchor="w")
        title.place(x=100, y=50, width=280)
        title_separator = ttk.Separator(orient="horizontal")
        title_separator.place(x=100, y=80, height=2, width=800)

        # Main Content of Page

        isbn_label = Label(frame_1, text='ISBN', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        isbn_label.place(x=100, y=115, width=100)
        isbn_entry = Entry(frame_1, width=200)
        isbn_entry.place(x=100, y=140, width=150)
        isbn_entry.insert(0, single_record_view[1])
        isbn_entry.config(state='disabled', disabledforeground='black')

        record_label = Label(frame_1, text='Record #', bg="white", font='Helvetica 15', anchor="w", padx=10)
        record_label.place(x=400, y=115, width=100)
        record_entry = Entry(frame_1, width=200)
        record_entry.place(x=400, y=140, width=150)
        record_entry.insert(0, single_record_view[0])
        record_entry.config(state='disabled', disabledforeground='black')

        added_label = Label(frame_1, text='Date Added', bg="white", font='Helvetica 15', anchor="w", padx=10)
        added_label.place(x=575, y=115, width=100)
        added_entry = Entry(frame_1, width=200)
        added_entry.place(x=575, y=140, width=150)
        added_entry.insert(0, single_record_view[9])
        added_entry.config(state='disabled', disabledforeground='black')

        update_label = Label(frame_1, text='Last Update', bg="white", font='Helvetica 15', anchor="w", padx=10)
        update_label.place(x=750, y=115, width=150)
        update_entry = Entry(frame_1, width=150)
        update_entry.place(x=750, y=140, width=150)
        update_entry.insert(0, single_record_view[10])
        update_entry.config(state='disabled', disabledforeground='black')

        title_label = Label(frame_1, text='Title', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        title_label.place(x=100, y=200, width=100)
        title_entry = Entry(frame_1, width=50)
        title_entry.place(x=100, y=225, width=800)
        title_entry.insert(0, single_record_view[2])
        title_entry.config(state='disabled', disabledforeground='black')

        first_label = Label(frame_1, text='Author - First Name', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        first_label.place(x=100, y=275, width=300)
        first_entry = Entry(frame_1, width=50)
        first_entry.place(x=100, y=300, width=300)
        first_entry.insert(0, single_record_view[3])
        first_entry.config(state='disabled', disabledforeground='black')

        last_label = Label(frame_1, text='Author - Last Name', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        last_label.place(x=425, y=275, width=300)
        last_entry = Entry(frame_1, width=50)
        last_entry.place(x=425, y=300, width=300)
        last_entry.insert(0, single_record_view[4])
        last_entry.config(state='disabled', disabledforeground='black')

        binding_label = Label(frame_1, text='Binding', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        binding_label.place(x=750, y=275, width=150)
        binding = StringVar(value=single_record_view[7])
        binding_options = OptionMenu(frame_1, binding, 'Hardcover', 'Softcover')
        binding_options.place(x=750, y=300, width=150)
        binding_options.config(state='disabled', disabledforeground='black')

        publisher_label = Label(frame_1, text='Publisher', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        publisher_label.place(x=100, y=350, width=300)
        publisher_entry = Entry(frame_1, width=50)
        publisher_entry.place(x=100, y=375, width=300)
        publisher_entry.insert(0, single_record_view[5])
        publisher_entry.config(state='disabled', disabledforeground='black')

        published_label = Label(frame_1, text='Published Date', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        published_label.place(x=425, y=350, width=300)
        published_entry = Entry(frame_1, width=50)
        published_entry.place(x=425, y=375, width=300)
        published_entry.insert(0, single_record_view[6])
        published_entry.config(state='disabled', disabledforeground='black')

        notes_label = Label(frame_1, text='Notes', bg="white", font='Helvetica 15 bold', anchor="w", padx=10)
        notes_label.place(x=100, y=425, width=300)
        notes_entry = Text(frame_1, height=7, width=50, font='Helvetica 13', wrap=WORD)
        notes_entry.place(x=100, y=450, width=300)
        notes_entry.insert('1.0', single_record_view[8])
        notes_entry.config(state='disabled')


        def clear_fields():
            isbn_entry.config(state='normal')
            title_entry.config(state='normal')
            record_entry.config(state='normal')
            added_entry.config(state='normal')
            update_entry.config(state='normal')
            first_entry.config(state='normal')
            last_entry.config(state='normal')
            publisher_entry.config(state='normal')
            published_entry.config(state='normal')
            binding_options.config(state='normal')
            notes_entry.config(state='normal')

            isbn_entry.delete(0, END)
            title_entry.delete(0, END)
            record_entry.delete(0, END)
            added_entry.delete(0, END)
            update_entry.delete(0, END)
            first_entry.delete(0, END)
            last_entry.delete(0, END)
            publisher_entry.delete(0, END)
            published_entry.delete(0, END)
            binding.set(' ')
            notes_entry.delete('1.0', 'end-1c')

            isbn_entry.config(state='disabled')
            title_entry.config(state='disabled')
            record_entry.config(state='disabled')
            added_entry.config(state='disabled')
            update_entry.config(state='disabled')
            first_entry.config(state='disabled')
            last_entry.config(state='disabled')
            publisher_entry.config(state='disabled')
            published_entry.config(state='disabled')
            binding_options.config(state='disabled')
            notes_entry.config(state='disabled')

        def click_delete():
            # Asks user to confirm deletion of record
            delete_record_number = record_entry.get()
            delete_record_title = title_entry.get()
            delete_confirm = 'Are you sure you want to delete Record #{0}: \'{1}\''.format(delete_record_number, delete_record_title)
            delete_answer = messagebox.askyesno("Confirm", delete_confirm)

            if delete_answer:
                # Prints selected record number, title and answer in console
                print(delete_record_number, delete_record_title, delete_answer)

                # Connects to db to delete record using id
                connection = sqlite3.connect(DATABASE_CONFIG['path'])
                c = connection.cursor()
                c.execute("""DELETE FROM shelfie WHERE rowid = {0};""".format(delete_record_number))
                connection.commit()
                connection.close()

                # Clears all entry widgets and disables delete button
                clear_fields()
                button_confirm_delete.config(state='disabled')

                delete_yes = 'Record #{0} was deleted.'.format(delete_record_number)
                please_select = Label(frame_4, text=delete_yes, bg='cyan', font='Helvetica 14', borderwidth=0, anchor=CENTER)
                please_select.place(x=2, y=220, width=196)

            else:
                # Prints selected record number, title and answer in console
                print(delete_record_number, delete_record_title, delete_answer)

                delete_no = 'Record #{0} was not deleted.'.format(delete_record_number)
                please_select = Label(frame_4, text=delete_no, bg='cyan', font='Helvetica 14', borderwidth=0, anchor=CENTER)
                please_select.place(x=2, y=220, width=196)


        # Navigation Buttons
        nav_separator = ttk.Separator(orient="horizontal")
        nav_separator.place(x=100, y=615, height=2, width=800)

        button_prev = Button(frame_1, text='<< Back to Library', highlightbackground='white', highlightthickness=0, command=self.Library_Page)
        button_prev.place(x=100, y=625, width=150)

        button_confirm_delete = Button(frame_1, text='Confirm Delete', highlightbackground='white', highlightthickness=0, command=click_delete)
        button_confirm_delete.place(x=750, y=625, width=150)


        # ===============================================
        # SIDE FRAME OF DELETE PAGE
        # ===============================================

        # Frame 2
        frame_2 = Frame(self.window, bg='cyan')
        frame_2.place(x=1000, y=0, relwidth=1, relheight=1)

        title = Label(frame_2, text='Shelfie!', bg='cyan', font='Garamond 50 bold', borderwidth=0, relief='solid')
        title.place(x=0, y=28, width=280)
        # shelfie_separator = ttk.Separator(frame_2, orient='horizontal')
        # shelfie_separator.place(x=40, y=80, height=2, width=200)

        about_button = Button(frame_2, text='About', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.About_Page)
        about_button.place(x=90, y=485, width=100)

        close_button = Button(frame_2, text='Close', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.window.quit)
        close_button.place(x=90, y=625, width=100)


        # Frame 3
        frame_3 = Frame(self.window, bg='cyan', borderwidth=0, relief='ridge')
        frame_3.place(x=1040, y=110, height=100, width=200)

        lib = LabelFrame(frame_3, text='Browse', bg='cyan', pady=10)
        lib.place(height=75, width=200)

        library_button = Button(lib, text='My Library', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.Library_Page)
        library_button.place(x=48, y=0, width=100)


        # Frame 4
        frame_4 = Frame(self.window, borderwidth=0, relief='ridge')
        frame_4.place(x=1040, y=210, height=250, width=200)

        crud = LabelFrame(frame_4, text='Record', bg='cyan', pady=10)
        crud.place(height=250, width=200)

        add_button = Button(crud, text='Add', bd=2, highlightbackground='cyan', highlightthickness=0)
        add_button.place(x=48, y=0, width=100)
        add_button.config(state='disabled')

        view_button = Button(crud, text='View', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        view_button.place(x=48, y=50, width=100)
        view_button.config(state='disabled')

        update_button = Button(crud, text='Update', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        update_button.place(x=48, y=100, width=100)
        update_button.config(state='disabled')

        delete_button = Button(crud, text='Delete', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        delete_button.place(x=48, y=150, width=100)
        delete_button.config(state='disabled')


    def About_Page(self):

        # ======================
        # MAIN FRAME FOR ABOUT PAGE
        # ======================
        frame_1 = Frame(self.window, bg="white")
        frame_1.place(x=0, y=0, width=1000, relheight=1)

        # Content in Main Frame

        # Page Banner
        title = Label(frame_1, text='About', bg="white", font='Garamond 25 bold', borderwidth=0, anchor="w")
        title.place(x=100, y=50, width=280)
        title_separator = ttk.Separator(orient="horizontal")
        title_separator.place(x=100, y=80, height=2, width=800)

        # About
        file = open('assets/copy/about.txt', 'r')
        about_content = file.read()
        about = Text(frame_1, height=20, width=50, font='Helvetica 15', wrap=WORD, highlightbackground='white', highlightthickness=0)
        about.place(x=100, y=115, width=800)
        about.insert('1.0', about_content)
        about.config(state=DISABLED)

        # Navigation Buttons
        nav_separator = ttk.Separator(orient="horizontal")
        nav_separator.place(x=100, y=590, height=2, width=800)


        # ===============================================
        # SIDE FRAME OF ABOUT PAGE
        # ===============================================

        # Frame 2
        frame_2 = Frame(self.window, bg='cyan')
        frame_2.place(x=1000, y=0, relwidth=1, relheight=1)

        title = Label(frame_2, text='Shelfie!', bg='cyan', font='Garamond 50 bold', borderwidth=0)
        title.place(x=0, y=28, width=280)
        # shelfie_separator = ttk.Separator(frame_2, orient='horizontal')
        # shelfie_separator.place(x=40, y=80, height=2, width=200)

        about_button = Button(frame_2, text='About', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.About_Page)
        about_button.place(x=90, y=485, width=100)
        about_button.config(state='disabled')

        close_button = Button(frame_2, text='Close', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.window.quit)
        close_button.place(x=90, y=625, width=100)


        # Frame 3
        frame_3 = Frame(self.window, bg='cyan', borderwidth=0, relief='ridge')
        frame_3.place(x=1040, y=110, height=100, width=200)

        lib = LabelFrame(frame_3, text='Browse', bg='cyan', pady=10)
        lib.place(height=75, width=200)

        library_button = Button(lib, text='My Library', bd=2, highlightbackground='cyan', highlightthickness=0, command=self.Library_Page)
        library_button.place(x=48, y=0, width=100)


        # Frame 4
        frame_4 = Frame(self.window, borderwidth=0, relief='ridge')
        frame_4.place(x=1040, y=210, height=250, width=200)

        crud = LabelFrame(frame_4, text='Record', bg='cyan', pady=10)
        crud.place(height=250, width=200)

        add_button = Button(crud, text='Add', bd=2, highlightbackground='cyan', highlightthickness=0)
        add_button.place(x=48, y=0, width=100)
        add_button.config(state='disabled')

        view_button = Button(crud, text='View', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        view_button.place(x=48, y=50, width=100)
        view_button.config(state='disabled')

        update_button = Button(crud, text='Update', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        update_button.place(x=48, y=100, width=100)
        update_button.config(state='disabled')

        delete_button = Button(crud, text='Delete', bd=2, highlightbackground='cyan', highlightthickness=0, width=10)
        delete_button.place(x=48, y=150, width=100)
        delete_button.config(state='disabled')


# The main function
if __name__ == "__main__":
    window = Tk()
    obj = Shelfie(window)
    window.mainloop()
