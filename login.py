import customtkinter as ctk
from tkinter import messagebox
from database import Database

db = Database()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LoginApp:

    def __init__(self):

        self.window = ctk.CTk()
        self.window.title("Gym Tracker - Login")
        self.window.geometry("500x500")
        self.window.resizable(False, False)

        title = ctk.CTkLabel(
            self.window,
            text="🏋 Gym Tracker",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=30)

        self.username = ctk.CTkEntry(
            self.window,
            placeholder_text="Username",
            width=300
        )
        self.username.pack(pady=15)

        self.password = ctk.CTkEntry(
            self.window,
            placeholder_text="Password",
            show="*",
            width=300
        )
        self.password.pack(pady=15)

        self.show_password = ctk.CTkCheckBox(
            self.window,
            text="Show Password",
            command=self.toggle_password
        )
        self.show_password.pack()

        login_btn = ctk.CTkButton(
            self.window,
            text="Login",
            width=250,
            command=self.login
        )
        login_btn.pack(pady=20)

        register_btn = ctk.CTkButton(
            self.window,
            text="Register",
            width=250,
            fg_color="green",
            command=self.register
        )
        register_btn.pack()

        self.window.mainloop()

    def toggle_password(self):

        if self.show_password.get():
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

    def login(self):

        username = self.username.get()
        password = self.password.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Please fill all fields.")
            return

        user = db.login_user(username, password)

        if user:
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.window.destroy()

            from dashboard import Dashboard
            Dashboard(username)

        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password.")

    def register(self):

        register_window = ctk.CTkToplevel(self.window)
        register_window.title("Register")
        register_window.geometry("400x550")

        fullname = ctk.CTkEntry(register_window, placeholder_text="Full Name")
        fullname.pack(pady=10)

        username = ctk.CTkEntry(register_window, placeholder_text="Username")
        username.pack(pady=10)

        password = ctk.CTkEntry(register_window, placeholder_text="Password", show="*")
        password.pack(pady=10)

        age = ctk.CTkEntry(register_window, placeholder_text="Age")
        age.pack(pady=10)

        gender = ctk.CTkEntry(register_window, placeholder_text="Gender")
        gender.pack(pady=10)

        height = ctk.CTkEntry(register_window, placeholder_text="Height (cm)")
        height.pack(pady=10)

        weight = ctk.CTkEntry(register_window, placeholder_text="Weight (kg)")
        weight.pack(pady=10)

        def save():

            success = db.register_user(
                fullname.get(),
                username.get(),
                password.get(),
                age.get(),
                gender.get(),
                height.get(),
                weight.get()
            )

            if success:
                messagebox.showinfo("Success", "Registration Successful!")
                register_window.destroy()
            else:
                messagebox.showerror("Error", "Username already exists.")

        ctk.CTkButton(
            register_window,
            text="Create Account",
            command=save
        ).pack(pady=20)


if __name__ == "__main__":
    LoginApp()
