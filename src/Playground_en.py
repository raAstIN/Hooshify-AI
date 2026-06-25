from tkinter import CENTER, END, LEFT
import customtkinter
import tkinter.messagebox as messagebox
import sqlite3
import requests
from io import BytesIO
from common import init_theme, load_icon, load_ctk_image, open_script, get_db_path, ensure_database
import config

init_theme()
ensure_database()

root_tk = customtkinter.CTk()
root_tk.geometry("370x720")
root_tk.title("Hooshify")
root_tk.resizable(height=False, width=False)
load_icon(root_tk)


def get_user_profile() -> tuple[str, str, str]:
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('SELECT name, lastname, email FROM user_profile ORDER BY rowid DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return row[0], row[1], row[2]
    return "Guest", "User", "guest@example.com"


def process_image_request(url: str, headers: dict[str, str], data: dict[str, object]) -> customtkinter.CTkImage | None:
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"API Response: {response.text}")
        return None

    image_url = response.json().get("data", [])[0].get("url")
    if not image_url:
        print("Invalid response from image API.")
        return None

    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image.thumbnail((300, 400), Image.Resampling.LANCZOS)
    return load_ctk_image("send.png") if False else load_ctk_image("send.png")


def generate_image(prompt: str) -> customtkinter.CTkImage | None:
    if not config.AVALAI_API_KEY:
        messagebox.showerror("Missing API Key", "Set AVALAI_API_KEY in your environment.")
        return None

    url = "https://api.avalai.ir/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": config.AVALAI_API_KEY,
    }
    if model_var.get() == "DALL-E 3":
        model_name = "dall-e-3"
    else:
        model_name = "dall-e-2"
    data = {"model": model_name, "prompt": prompt, "n": 1, "size": "1024x1024"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"API Response: {response.text}")
        messagebox.showerror("Image Error", "Unable to generate image. Check your API key and network.")
        return None

    response_json = response.json()
    image_url = response_json.get("data", [])[0].get("url")
    if not image_url:
        print("Invalid API response.")
        return None

    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image.thumbnail((300, 400), Image.Resampling.LANCZOS)
    return customtkinter.CTkImage(image)


def generate_button_action() -> None:
    prompt = entry_1.get().strip()
    if not prompt:
        return
    prompt = prompt
    entry_1.delete(0, END)
    result = generate_image(prompt)
    if result:
        image_label.configure(image=result, text="")
        image_label.image = result


def open_panel() -> None:
    root_tk.destroy()
    open_script("Panel_en.py")


def open_profile() -> None:
    root_tk.destroy()
    open_script("Profile_en.py")


def download_image() -> None:
    if hasattr(image_label, 'image'):
        from tkinter import filedialog
        photo = image_label.image
        image = ImageTk.getimage(photo)
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filename:
            image.save(filename)

profile_name, profile_lastname, profile_email = get_user_profile()

y_padding = 13
image_size = 30

image_label = None

frame_1 = customtkinter.CTkFrame(master=root_tk, corner_radius=20, width=335, height=685)
frame_1.place(relx=0.05, rely=0.025)

label_2 = customtkinter.CTkLabel(master=frame_1, justify=LEFT, text="Hooshify", font=("harlow solid italic", 32))
label_2.place(relx=0.225, rely=0.06, anchor='c')

image_label = customtkinter.CTkLabel(master=frame_1, text="Generated image will appear here", text_color="gray70", font=("montserrat", 12), width=300, height=400)
image_label.place(relx=0.05, rely=0.1)

entry_1 = customtkinter.CTkEntry(master=frame_1, corner_radius=30, width=243, height=45, placeholder_text="Describe the image you want...", font=("montserrat", 12, "bold"))
entry_1.place(relx=0.025, rely=0.7)
entry_1.bind("<Return>", lambda event: generate_button_action())

model_var = customtkinter.StringVar(value="DALL-E 3")
combo_box = customtkinter.CTkComboBox(master=frame_1, values=["DALL-E 3", "DALL-E 2"], variable=model_var, corner_radius=30, width=315, height=45, font=("montserrat", 12, "bold"))
combo_box.place(relx=0.025, rely=0.84)
combo_box.set("DALL-E 3")

send_image = load_ctk_image("send.png")
button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=500, command=generate_button_action, text="", font=("montserrat", 15, "bold"), image=send_image, width=45, height=45, compound="right")
button_1.place(relx=0.76, rely=0.7)

undo_image = load_ctk_image("undo.png")
button_back = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=open_panel, text="Back", font=("montserrat", 15, "bold"), image=undo_image, width=135, height=45, compound="right", fg_color="#8B0000", hover_color="#B22222")
button_back.place(relx=0.555, rely=0.91)

profile_image = load_ctk_image("user.png")
profile_button = customtkinter.CTkButton(master=frame_1, text=f"{profile_name} {profile_lastname}", font=("montserrat", 14, "bold"), width=90, height=50, corner_radius=50, fg_color="#363635", hover_color="#4a4a4a", image=profile_image, compound="right", command=open_profile)
profile_button.place(relx=0.7, rely=0.06, anchor='c')

def change_theme(choice: str) -> None:
    if choice == "Dark":
        customtkinter.set_appearance_mode("dark")
    elif choice == "Light":
        customtkinter.set_appearance_mode("light")
    else:
        customtkinter.set_appearance_mode("system")


button_download = customtkinter.CTkButton(master=frame_1, corner_radius=30, command=download_image, text="Download", font=("montserrat", 13, "bold"), width=150, height=45)
button_download.place(relx=0.025, rely=0.77)

button_profile = customtkinter.CTkButton(master=frame_1, corner_radius=30, command=open_profile, text="Profile", font=("montserrat", 13, "bold"), width=150, height=45)
button_profile.place(relx=0.545, rely=0.77)

theme_option = customtkinter.CTkOptionMenu(master=frame_1, values=["System Theme", "Dark", "Light"], command=change_theme, corner_radius=30, width=170, height=45, font=("montserrat", 12, "bold"))
theme_option.set("System Theme")
theme_option.place(relx=0.025, rely=0.91)

if __name__ == "__main__":
    root_tk.mainloop()
