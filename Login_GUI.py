import customtkinter as ctk
from tkinter import filedialog, simpledialog, messagebox


def start_login_gui():
    app = ctk.CTk()
    app.geometry("800x400")
    app.title("ASU Job Application Tool")

    user_details = {
        "asu_username": "",
        "asu_password": "",
        "resume_path": "",
        "start_date": ""
    }

    frame = ctk.CTkFrame(master=app)
    frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    asu_username_entry = ctk.CTkEntry(master=frame, placeholder_text="ASU Username")
    asu_username_entry.pack(pady=12, padx=10, fill='x', expand=True)
    asu_password_entry = ctk.CTkEntry(master=frame, placeholder_text="ASU Password", show="*")
    asu_password_entry.pack(pady=12, padx=10, fill='x', expand=True)

    def choose_file():
        filename = filedialog.askopenfilename(initialdir="/", title="Select Resume File",
                                              filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        if filename:
            user_details["resume_path"] = filename
            file_label.configure(text=f"Selected File: {filename}")

    file_button = ctk.CTkButton(master=frame, text="Select Resume File", command=choose_file)
    file_button.pack(pady=12)
    file_label = ctk.CTkLabel(master=frame, text="No file selected")
    file_label.pack(pady=12)

    def get_date():
        date = simpledialog.askstring("Input", "Enter start date (MM/DD/YYYY):", parent=app)
        if date:
            user_details["start_date"] = date
            date_label.configure(text="Start Date: " + date)

    date_button = ctk.CTkButton(master=frame, text="Select Start Date", command=get_date)
    date_button.pack(pady=12)
    date_label = ctk.CTkLabel(master=frame, text="No date selected")
    date_label.pack(pady=12)

    def save_and_close():
        user_details["asu_username"] = asu_username_entry.get()
        user_details["asu_password"] = asu_password_entry.get()
        app.destroy()

    continue_button = ctk.CTkButton(master=frame, text="Continue", command=save_and_close)
    continue_button.pack(pady=20)

    app.mainloop()
    return user_details



