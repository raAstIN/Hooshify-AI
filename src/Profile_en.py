from tkinter import CENTER
import customtkinter
import sqlite3
from common import init_theme, load_icon, load_ctk_image, open_script, get_db_path, ensure_database

init_theme()
ensure_database()

root_tk = customtkinter.CTk()
root_tk.geometry("400x550")
root_tk.title("Hooshify")
root_tk.resizable(height=False, width=False)
load_icon(root_tk)


def get_current_profile() -> tuple[str, str, str]:
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('SELECT name, lastname, email FROM user_profile ORDER BY rowid DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return row[0], row[1], row[2]
    return "Guest", "User", "guest@example.com"


def go_back() -> None:
    root_tk.destroy()
    open_script("Panel_en.py")


def logout() -> None:
    root_tk.destroy()
    open_script("Main_en.py")


def toggle_theme() -> None:
    if switch_1.get() == 1:
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")

profile_name, profile_lastname, profile_email = get_current_profile()

y_padding = 13
image_size = 30

user_image = load_ctk_image("user.png", size=(image_size, image_size))
undo_image = load_ctk_image("undo.png", size=(image_size, image_size))
cross_image = load_ctk_image("cross.png", size=(image_size-10, image_size-10))

frame_1 = customtkinter.CTkFrame(master=root_tk, corner_radius=20)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text="Hooshify", font=("harlow solid italic", 40))
label_1.pack(pady=y_padding, padx=10)

label_name = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text=f"Name: {profile_name}", font=("montserrat", 15, "bold"))
label_name.pack(pady=y_padding, padx=10)

label_last = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text=f"LastName: {profile_lastname}", font=("montserrat", 15, "bold"))
label_last.pack(pady=y_padding, padx=10)

label_email = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text=f"Email: {profile_email}", font=("montserrat", 15, "bold"))
label_email.pack(pady=y_padding, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=go_back, text="Back", font=("montserrat", 15, "bold"), image=undo_image, width=200, height=45, compound="right")
button_1.pack(pady=y_padding, padx=10)
button_2 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=logout, text="Log Out", font=("montserrat", 15, "bold"), image=cross_image, width=200, height=45, compound="right", fg_color="#8B0000", hover_color="#B22222")
button_2.pack(pady=y_padding, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1, text="Dark Mode", command=toggle_theme, font=("montserrat", 10, "bold"))
switch_1.pack(pady=y_padding, padx=10)

if __name__ == "__main__":
    root_tk.mainloop()
