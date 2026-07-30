from CTkMessagebox import CTkMessagebox
from check_security import *
from database import *
import customtkinter as ctk
from tkinter import ttk

class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        Base.metadata.create_all(engine)
        self.title("Password Manager")
        self.geometry("400x350")

        self.visibility=False  # visibility of text in password entry

        self.registration()

    def registration(self):

        # Getting unique_key for app's registration.
        # APP_UNIQUE_KEY will show if the app was activated before
        # first activation will end to registration with unique column of 'where_used'

        load_dotenv()
        self.APP_UNIQUE_KEY=os.getenv("UNIQUE_KEY_APP").encode()

        registration=ctk.CTkLabel(self, text="Registration", font=("Times", 40, "bold"))

        self.username=ctk.CTkEntry(self, placeholder_text="Entry your username", font=("Times", 30), width=380)
        self.password=ctk.CTkEntry(self, placeholder_text="Entry your password", font=("Times", 30), width=380, show="*")

        self.check_new=ctk.CTkLabel(self, text="", font=("Times", 15))

        open_app=ctk.CTkButton(self, text="Open Manager", font=("Times", 40, "bold"), command=self.pre_open_manager)
        self.show_button=ctk.CTkButton(self, text="🔒", font=("Times", 30), command=self.show, width=1)

        registration.pack(pady=40)
        self.username.pack()

        self.password.pack(pady=(20, 0))

        self.check_new.pack(side="left")
        self.show_button.pack(side="left")

        # following will tell if password is secure enough
        self.password.bind("<KeyRelease>", command=lambda e: self.check_weakness(event=e, start=True))

        open_app.pack(side="bottom", pady=(20, 0))

    def show(self):  # shows or hides password entry's text
        if self.visibility:
            self.password.configure(show="*")
            self.show_button.configure(text="🔒")
            self.visibility=False
        elif not self.visibility:
            self.password.configure(show="")
            self.show_button.configure(text="🔓")
            self.visibility=True

    def check_weakness(self, event, start: bool):
        """
        Function for search of weaknesses in password
        """

        session=Session()

        if start:  # if it's from func 'registration'

            # checking if user was logged in before
            user=session.query(UserPasswords).filter_by(where_used=self.APP_UNIQUE_KEY).first()

            if not user:  # was not logged before
                self.result=Password.analise(self.password.get())

                if self.result=="Weak password":
                    self.check_new.configure(text=self.result, text_color="red")
                elif self.result=="Medium password":
                    self.check_new.configure(text=self.result, text_color="yellow")
                elif self.result=="Strong password":
                    self.check_new.configure(text=self.result, text_color="green2")
                session.close()

            else:  # ignore function and returns nothing
                session.close()
                return
        else:  # if func is from add_pass[word]
            self.result = Password.analise(self.password.get())

            if self.result == "Weak password":
                self.check_new.configure(text=self.result, text_color="red")
            elif self.result == "Medium password":
                self.check_new.configure(text=self.result, text_color="yellow")
            elif self.result == "Strong password":
                self.check_new.configure(text=self.result, text_color="green2")
            session.close()



    def pre_open_manager(self):
        """
        Function check if user was logged in. If not, adds him to database and let him in
        """

        self.unbind_all("<KeyRelease>")

        session=Session()

        # search for user with unique 'where_used'
        user=session.query(UserPasswords).filter_by(where_used=self.APP_UNIQUE_KEY, username=self.username.get()).first()


        if not user:  # if user with following username was not found

            new_user=session.query(UserPasswords).filter_by(where_used=self.APP_UNIQUE_KEY).first()

            if not new_user: # create everything if there is no such data
                new_user2=UserPasswords(where_used=self.APP_UNIQUE_KEY,
                                       username=self.username.get())

                if self.result in ["Weak password", "Medium password"]:
                    # security of the given password
                    CTkMessagebox(title="Warning", message="Make your password stronger!",
                                  font=("Times", 20), width=200, height=100, icon="warning")
                    return

                new_user2.set_password(self.password.get())

                session.add(new_user2)
                session.commit()
                session.close()
                self.pre_open_manager()
                return

        try:
            password = user.get_password()
        except AttributeError:
            CTkMessagebox(title="Error!", message="Check the spelling of the password/username!",
                          font=("Times", 20), width=200, height=100, icon="warning")
            return
        finally:
            session.commit()
            session.close()

        if password!=self.password.get():  # Is password correct?
            CTkMessagebox(title="Error!", message="Check the spelling of the password/username!",
                              font=("Times", 20), width=200, height=100, icon="warning")
            return

        self.manager()

    def manager(self):
        """
        Main manager function with table and adding/deleting abilities
        """

        for widget in self.winfo_children():
            widget.destroy()  # clean window

        self.state("zoomed")  # full-screen window

        style=ttk.Style()

        style.configure("Treeview", font=("Times", 20), rowheight=40)

        style.configure("Treeview.Heading", font=("Times", 25))

        self.passwords = ttk.Treeview(self, columns=("where_used", "username", "password"),
                                       show="headings", height=40,)

        self.passwords.heading("where_used", text="Service")
        self.passwords.column("where_used", width=400)

        self.passwords.heading("username", text="Username")
        self.passwords.column("username", width=400)

        self.passwords.heading("password", text="Password")
        self.passwords.column("password", width=400)

        self.passwords.pack(side="right")

        add=ctk.CTkButton(self, text="Add", font=("Times", 40), command=self.add_pass)
        delete=ctk.CTkButton(self, text="Delete", font=("Times", 40), command=self.delete_pass)

        add.pack(pady=30)
        delete.pack()

        self.update_table()

    def update_table(self):
        """
        Updating data in table called self.passwords
        """

        connect = engine.connect()

        get = connect.execute(text("SELECT where_used, username, password FROM user_passwords"))
        result = get.fetchall()

        for item in self.passwords.get_children():
            self.passwords.delete(item)  # clean table

        for info in result:
            new_info = [0, 1, 2]
            if info[0] == self.APP_UNIQUE_KEY:  # ignore main app data
                continue
            if info[0]:
                new_info.insert(0, info[0])
            if info[1]:
                new_info.insert(1, info[1])
            if info[2]:
                decrypted = cipher.decrypt(info[2].encode("utf-8"))

                new_info.insert(2, decrypted.decode("utf-8"))

            if new_info != [0, 1, 2]:
                self.passwords.insert("", ctk.END, values=new_info)  # inserting data with encrypted passwords

    def add_pass(self):
        """
        Function for adding password window
        """

        self.add_new_word = ctk.CTkToplevel(self)

        self.add_new_word.geometry("700x500")
        self.add_new_word.title("Neu Wort")
        self.add_new_word.attributes("-topmost", True)

        self.where_used=ctk.CTkEntry(self.add_new_word, font=("Times", 25), placeholder_text="Entry service", width=500)
        self.username=ctk.CTkEntry(self.add_new_word, font=("Times", 25), placeholder_text="Entry username", width=500)
        self.password=ctk.CTkEntry(self.add_new_word, font=("Times", 25), placeholder_text="Entry password", show="*", width=500)

        self.password.bind("<KeyRelease>", command=lambda e: self.check_weakness(event=e, start=False))

        add=ctk.CTkButton(self.add_new_word, text="Add", font=("Times", 40), command=self.add_pass_process)
        recommend_one=ctk.CTkButton(self.add_new_word, text="Recommend", font=("Times", 25), command=lambda:
        [self.password.delete(0, ctk.END),self.password.insert(0, Password.recommend_new_password())])
        # lambda: clean entry and then insert strong password

        self.check_new = ctk.CTkLabel(self.add_new_word, text="", font=("Times", 15))
        self.show_button = ctk.CTkButton(self.add_new_word, text="🔒", font=("Times", 30), command=self.show, width=1)

        self.where_used.pack(pady=20)
        self.username.pack()
        self.password.pack(pady=(20, 0))

        self.check_new.pack(side="left")
        self.show_button.pack(side="left")

        add.pack(side="right")
        recommend_one.pack(side="right")

    def add_pass_process(self):
        # process of adding new data

        try:
            session=Session()

            new_pass=UserPasswords(where_used=self.where_used.get(), username=self.username.get())
            new_pass.set_password(self.password.get())
            self.result = Password.analise(self.password.get())
            if self.result in ["Weak password", "Medium password"]:
                # security of the given password
                CTkMessagebox(title="Warning", message="Make your password stronger!",
                              font=("Times", 20), width=200, height=100, icon="warning")
                return

            session.add(new_pass)
            session.commit()
            session.close()
            self.add_new_word.destroy()  # close TopLevel to show that process is ended
        except IntegrityError:
            CTkMessagebox(title="Error", message="Service and username already used!", icon="warning")
        finally:
            self.update_table()


    def delete_pass(self):
        # data deletion

        session=Session()

        try:
            delete_find=self.passwords.selection()  # get selected data

            for item_id in delete_find:
                value=self.passwords.item(item_id, "values")

            delete_find=session.query(UserPasswords).filter_by(where_used=value[0], username=value[1]).first()
            # search it in window

            session.delete(delete_find)  # delete it
        except:
            CTkMessagebox(title="Error", message="Error")
        finally:
            session.commit()
            session.close()
            self.update_table()

if __name__=="__main__":
    app=Window()
    app.mainloop()
