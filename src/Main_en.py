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


def open_menu() -> None:
    root_tk.destroy()
    open_script("Menu_en.py")


def disabled_action() -> None:
    pass


def toggle_theme() -> None:
    if switch_1.get() == 1:
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")


y_padding = 13
image_size = 30

play_image = load_ctk_image("play.png", size=(image_size, image_size))
internet_image = load_ctk_image("internet.png", size=(image_size, image_size))
team_image = load_ctk_image("team.png", size=(image_size, image_size))
question_image = load_ctk_image("question.png", size=(image_size, image_size))

frame_1 = customtkinter.CTkFrame(master=root_tk, corner_radius=20)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text="Hooshify", font=("harlow solid italic", 40))
label_1.pack(pady=y_padding, padx=10)

label_2 = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text="A Chatbot With A Lot of Tools And Fun.", font=("montserrat", 10, "bold"))
label_2.pack(pady=y_padding, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=open_menu, text="Get Started", font=("montserrat", 15, "bold"), image=play_image, width=190, height=45, compound="right")
button_1.pack(pady=y_padding, padx=10)
button_2 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=disabled_action, text="Language", font=("montserrat", 15, "bold"), image=internet_image, width=190, height=45, compound="right")
button_2.pack(pady=y_padding, padx=10)
button_2.configure(state="disabled")
button_3 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=disabled_action, text="About Us", font=("montserrat", 15, "bold"), image=team_image, width=190, height=45, compound="right")
button_3.pack(pady=y_padding, padx=10)
button_3.configure(state="disabled")
button_4 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=disabled_action, text="Notice", font=("montserrat", 15, "bold"), image=question_image, width=190, height=45, compound="right")
button_4.pack(pady=y_padding, padx=10)
button_4.configure(state="disabled")

switch_1 = customtkinter.CTkSwitch(master=frame_1, text="Dark Mode", command=toggle_theme, font=("montserrat", 10, "bold"))
switch_1.pack(pady=y_padding, padx=10)

if __name__ == "__main__":
    root_tk.mainloop()
