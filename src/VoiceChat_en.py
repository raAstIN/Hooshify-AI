from tkinter import CENTER
import customtkinter
from common import init_theme, load_icon, load_ctk_image, open_script, ensure_database

init_theme()
ensure_database()

root_tk = customtkinter.CTk()
root_tk.geometry("400x520")
root_tk.title("Hooshify")
root_tk.resizable(height=False, width=False)
load_icon(root_tk)


def go_back() -> None:
    root_tk.destroy()
    open_script("Panel_en.py")


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

label_1 = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text="Voice Chat", font=("harlow solid italic", 40))
label_1.pack(pady=y_padding, padx=10)

label_2 = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text="This feature is coming soon.", font=("montserrat", 12, "bold"))
label_2.pack(pady=y_padding, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=go_back, text="Back", font=("montserrat", 15, "bold"), image=undo_image, width=190, height=45, compound="right")
button_1.pack(pady=y_padding, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1, text="Dark Mode", command=toggle_theme, font=("montserrat", 10, "bold"))
switch_1.pack(pady=y_padding, padx=10)

if __name__ == "__main__":
    root_tk.mainloop()
