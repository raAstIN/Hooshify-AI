from tkinter import CENTER, END
import customtkinter
import tkinter.messagebox as messagebox
import sqlite3
from common import init_theme, load_icon, load_ctk_image, open_script, get_db_path, ensure_database

init_theme()
ensure_database()

root_tk = customtkinter.CTk()
root_tk.geometry("400x510")
root_tk.title("Hooshify")
root_tk.resizable(height=False, width=False)
load_icon(root_tk)


def login_user() -> None:
    email_login = entry_1.get().strip()
    pass_login = entry_2.get().strip()
    if not email_login or not pass_login:
        messagebox.showinfo("Login", "Please enter email and password.")
        return

    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('SELECT name, lastname, email FROM user_info WHERE email = ? AND password = ?', (email_login, pass_login))
    result = c.fetchone()
    if result:
        user_name, user_lastname, user_email = result
        c.execute('DELETE FROM user_profile WHERE email = ?', (user_email,))
        c.execute(
            'INSERT INTO user_profile (name, lastname, email) VALUES (?, ?, ?)',
            (user_name, user_lastname, user_email),
        )
        conn.commit()
        conn.close()
        root_tk.destroy()
        open_script("Panel_en.py")
    else:
        conn.close()
        messagebox.showinfo("Login", "Email or password is wrong.")


def go_back() -> None:
    root_tk.destroy()
    open_script("Menu_en.py")


def toggle_theme() -> None:
    if switch_1.get() == 1:
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")


y_padding = 13
image_size = 30

user_image = load_ctk_image("user.png", size=(image_size, image_size))
undo_image = load_ctk_image("undo.png", size=(image_size, image_size))

frame_1 = customtkinter.CTkFrame(master=root_tk, corner_radius=20)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text="Hooshify", font=("harlow solid italic", 40))
label_1.pack(pady=y_padding, padx=10)

label_2 = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text="A ChatBot With A Lot of Tools And Fun.", font=("montserrat", 10, "bold"))
label_2.pack(pady=y_padding, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame_1, corner_radius=20, width=200, placeholder_text="Email", height=40)
entry_1.pack(pady=y_padding, padx=10)
entry_2 = customtkinter.CTkEntry(master=frame_1, corner_radius=20, width=200, show="●", placeholder_text="Password", height=40)
entry_2.pack(pady=y_padding, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=login_user, text="Login", font=("montserrat", 15, "bold"), image=user_image, width=190, height=45, compound="right")
button_1.pack(pady=y_padding, padx=10)
button_2 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=go_back, text="Back", font=("montserrat", 15, "bold"), image=undo_image, width=190, height=45, compound="right")
button_2.pack(pady=y_padding, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1, text="Dark Mode", command=toggle_theme, font=("montserrat", 10, "bold"))
switch_1.pack(pady=y_padding, padx=10)

if __name__ == "__main__":
    root_tk.mainloop()
