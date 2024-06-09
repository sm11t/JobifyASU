import customtkinter as ctk
import subprocess
import platform

def main_gui():
    app = ctk.CTk()
    app.title("Input and Output Windows")
    app.geometry("800x400")

    # Create a frame for output
    output_frame = ctk.CTkFrame(master=app)
    output_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    file_path = "/Users/shiro/Desktop/Resume March24.pdf"

    # Function to open the resume file
    def open_resume(event=None):  # Added event parameter for binding
        if platform.system() == "Windows":
            subprocess.run(["start", file_path], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux
            subprocess.run(["xdg-open", file_path])

    # Label styled like a hyperlink
    hyperlink_label = ctk.CTkLabel(master=output_frame, text=file_path, text_color="green", cursor="hand2", font=("Arial", 14, "underline"))
    hyperlink_label.pack(pady=20)
    hyperlink_label.bind("<Button-1>", open_resume)  # Bind left mouse click to the open_resume function

    app.mainloop()

if __name__ == "__main__":
    main_gui()
