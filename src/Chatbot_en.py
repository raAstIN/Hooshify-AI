import threading
from tkinter import CENTER, END, LEFT
import customtkinter
import persian
import sqlite3
from openai import OpenAI
try:
    from groq import Groq
except Exception:
    Groq = None
from common import init_theme, load_icon, load_ctk_image, open_script, get_db_path, ensure_database
import config

init_theme()
ensure_database()

root_tk = customtkinter.CTk()
root_tk.geometry("400x760")
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


def get_llm7_client() -> OpenAI:
    if not config.LLM7_API_KEY:
        raise RuntimeError("LLM7 API key is not configured. Set LLM7_API_KEY in the environment.")
    return OpenAI(base_url=config.LLM7_BASE_URL, api_key=config.LLM7_API_KEY)


def get_groq_client():
    if Groq is None:
        raise RuntimeError("groq package not installed. Install with `pip install groq`")
    if getattr(config, "GROQ_API_KEY", None):
        return Groq(api_key=config.GROQ_API_KEY)
    return Groq()


def ask_llm7_model(message: str, friendly_name: str) -> str:
    api_model = config.MODEL_MAPPING.get(friendly_name)
    if not api_model:
        return "Model not supported."
    # Use Groq provider for models that map to openai/gpt-oss-*
    if isinstance(api_model, str) and api_model.startswith("openai/gpt-oss"):
        client = get_groq_client()
        completion = client.chat.completions.create(
            model=api_model,
            messages=[{"role": "user", "content": message}],
            temperature=1,
            max_completion_tokens=getattr(config, "GROQ_MAX_TOKENS", 1024),
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None,
        )
        text = ""
        for chunk in completion:
            try:
                delta = chunk.choices[0].delta.content or ""
            except Exception:
                delta = ""
            text += delta
        return text.strip()

    client = get_llm7_client()
    resp = client.chat.completions.create(
        model=api_model,
        messages=[{"role": "user", "content": message}],
    )
    if hasattr(resp, "choices") and len(resp.choices) > 0:
        try:
            return resp.choices[0].message.content.strip()
        except Exception:
            response_dict = resp
            return response_dict["choices"][0]["message"]["content"].strip()
    if isinstance(resp, dict):
        if "choices" in resp and len(resp["choices"]) > 0:
            c = resp["choices"][0]
            if isinstance(c.get("message"), dict):
                return c["message"].get("content", "").strip()
            if "text" in c:
                return c["text"].strip()
    return ""


def send_message() -> None:
    user_prompt = entry_1.get().strip()
    if not user_prompt:
        return
    user_prompt = persian.arToPersianChar(user_prompt)
    entry_1.delete(0, END)

    def run_model_call() -> None:
        try:
            answer = ask_llm7_model(user_prompt, current_model)
        except Exception as exc:
            answer = f"Error: {exc}"
        root_tk.after(0, lambda: answer_to_user(user_prompt, answer))

    threading.Thread(target=run_model_call, daemon=True).start()


def answer_to_user(user_prompt: str, ai_answer: str) -> None:
    model_name = current_model.capitalize()
    textbox.insert(END, f"{profile_name}: {user_prompt}\n")
    textbox.see(END)
    textbox.insert(END, "________________________________________\n\n")
    textbox.insert(END, f"{model_name}: ")
    textbox.see(END)

    words = ai_answer.split()

    def stream_words(index: int) -> None:
        if index < len(words):
            textbox.insert(END, words[index] + " ")
            textbox.see(END)
            root_tk.after(80, stream_words, index + 1)
        else:
            textbox.insert(END, "\n________________________________________\n\n\n")
            textbox.see(END)

    stream_words(0)


def open_panel() -> None:
    root_tk.destroy()
    open_script("Panel_en.py")


def change_theme() -> None:
    if theme_option.get() == "Dark":
        customtkinter.set_appearance_mode("dark")
        textbox.configure(fg_color="#363635")
    elif theme_option.get() == "Light":
        customtkinter.set_appearance_mode("light")
        textbox.configure(fg_color="#f0f0f0")
    else:
        customtkinter.set_appearance_mode("system")
        textbox.configure(fg_color="#363635")


def set_model(choice: str) -> None:
    global current_model
    current_model = choice


def clear_chat() -> None:
    textbox.delete("1.0", END)


def select_file() -> None:
    from tkinter import filedialog
    file_path = filedialog.askopenfilename()
    if file_path:
        textbox.insert(END, f"File selected: {file_path}\n")
        textbox.see(END)


def open_profile_screen() -> None:
    root_tk.destroy()
    open_script("Profile_en.py")

profile_name, profile_lastname, profile_email = get_user_profile()

y_padding = 13

send_image = load_ctk_image("send.png")
attach_image = load_ctk_image("attach.png")
plus_image = load_ctk_image("plus.png")
undo_image = load_ctk_image("undo.png")
user_image = load_ctk_image("user.png")

frame_1 = customtkinter.CTkFrame(master=root_tk, corner_radius=20, width=365, height=725)
frame_1.place(relx=0.05, rely=0.025)

textbox_container = customtkinter.CTkFrame(master=frame_1, corner_radius=15, width=335, height=410)
textbox_container.place(relx=0.05, rely=0.12)

textbox = customtkinter.CTkTextbox(master=textbox_container, width=335, height=410, font=("Vazir", 15, "bold"), wrap="word", corner_radius=15, fg_color="#363635")
textbox.pack(fill="both", expand=True)

textbox.configure(yscrollcommand=customtkinter.CTkScrollbar(master=textbox_container, orientation="vertical", command=textbox.yview).set)

textbox.insert(END, f"Hi {profile_name}\nHow can i help you?\n\n")

entry_1 = customtkinter.CTkEntry(master=frame_1, corner_radius=50, width=265, height=45, placeholder_text="Write A Message...", font=("Vazir", 12, "bold"))
entry_1.place(relx=0.03, rely=0.71)
entry_1.bind("<Return>", lambda event: send_message())

combo_box = customtkinter.CTkComboBox(
    master=frame_1,
    values=list(config.MODEL_MAPPING.keys()),
    command=set_model,
    corner_radius=25,
    width=340,
    height=45,
    font=("Vazir", 15, "bold"),
)
combo_box.set("gpt-oss-20b")
combo_box.place(relx=0.03, rely=0.85)

button_send = customtkinter.CTkButton(master=frame_1, corner_radius=500, command=send_message, text="", font=("Vazir", 15, "bold"), image=send_image, width=45, height=45, compound="right")
button_send.place(relx=0.77, rely=0.71)

button_back = customtkinter.CTkButton(master=frame_1, corner_radius=50, command=open_panel, text="Back", font=("Vazir", 15, "bold"), image=undo_image, width=140, height=45, compound="right", fg_color="#8B0000", hover_color="#B22222")
button_back.place(relx=0.58, rely=0.92)

segmented_btn = customtkinter.CTkSegmentedButton(master=frame_1, values=["      New Chat      ", "      Send Files      "], command=lambda choice: clear_chat() if choice == "New Chat" else select_file(), corner_radius=50, width=340, height=45, font=("montserrat", 14, "bold"), fg_color="#363635")
segmented_btn.place(relx=0.03, rely=0.78)

label_2 = customtkinter.CTkLabel(master=frame_1, justify=LEFT, text="Hooshify", font=("harlow solid italic", 35))
label_2.place(relx=0.25, rely=0.06, anchor='c')

profile_button = customtkinter.CTkButton(master=frame_1, text=f"{profile_name} {profile_lastname}", font=("montserrat", 15, "bold"), width=100, height=50, corner_radius=50, fg_color="#363635", hover_color="#4a4a4a", image=user_image, compound="right", command=open_profile_screen)
profile_button.place(relx=0.72, rely=0.06, anchor='c')

theme_option = customtkinter.CTkOptionMenu(master=frame_1, values=["System Theme", "Dark", "Light"], command=change_theme, corner_radius=30, width=190, height=45, font=("montserrat", 14, "bold"))
theme_option.set("System Theme")
theme_option.place(relx=0.03, rely=0.92)

current_model = "gpt-oss-20b"

if __name__ == "__main__":
    root_tk.mainloop()
