from tkinter import CENTER
import customtkinter
from common import init_theme, load_icon, load_ctk_image, open_script, ensure_database

init_theme()
ensure_database()

root_tk = customtkinter.CTk()
root_tk.geometry("400x590")
root_tk.title("Hooshify")
root_tk.resizable(height=False, width=False)
load_icon(root_tk)


def open_chatbot() -> None:
    root_tk.destroy()
    open_script("Chatbot_en.py")


def open_playground() -> None:
    root_tk.destroy()
    open_script("Playground_en.py")


def disabled_action() -> None:
    pass


def open_profile() -> None:
    root_tk.destroy()
    open_script("Profile_en.py")


def logout() -> None:
    root_tk.destroy()
    open_script("Main_en.py")


def toggle_theme() -> None:
    if switch_1.get() == 1:
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")


y_padding = 13
image_size = 30

chat_image = load_ctk_image("chat.png", size=(image_size, image_size))
microphone_image = load_ctk_image("microphone.png", size=(image_size, image_size))
image_image = load_ctk_image("image.png", size=(image_size, image_size))
cross_image = load_ctk_image("cross.png", size=(image_size-10, image_size-10))
user_image = load_ctk_image("user.png", size=(image_size, image_size))

frame_1 = customtkinter.CTkFrame(master=root_tk, corner_radius=20)
frame_1.pack(pady=20, padx=50, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text="Hooshify", font=("harlow solid italic", 40))
label_1.pack(pady=y_padding, padx=10)

label_2 = customtkinter.CTkLabel(master=frame_1, justify=CENTER, text="A Chatbot With A Lot of Tools And Fun.", font=("montserrat", 10, "bold"))
label_2.pack(pady=y_padding, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=open_chatbot, text="ChatBot", font=("montserrat", 15, "bold"), image=chat_image, width=220, height=45, compound="right")
button_1.pack(pady=y_padding, padx=10)
button_2 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=open_playground, text="Image Playground", font=("montserrat", 15, "bold"), image=image_image, width=220, height=45, compound="right")
button_2.pack(pady=y_padding, padx=10)
button_3 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=disabled_action, text="Voice Chat", font=("montserrat", 15, "bold"), image=microphone_image, width=220, height=45, compound="right")
button_3.pack(pady=y_padding, padx=10)
button_3.configure(state="disabled")
button_4 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=open_profile, text="Profile", font=("montserrat", 15, "bold"), image=user_image, width=220, height=45, compound="right")
button_4.pack(pady=y_padding, padx=10)
button_5 = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=logout, text="Log Out", font=("montserrat", 15, "bold"), image=cross_image, width=220, height=45, compound="right", fg_color="#8B0000", hover_color="#B22222")
button_5.pack(pady=y_padding, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1, text="Dark Mode", command=toggle_theme, font=("montserrat", 10, "bold"))
switch_1.pack(pady=y_padding, padx=10)

if __name__ == "__main__":
    root_tk.mainloop()
