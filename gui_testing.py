import customtkinter as ctk
from tkinter import scrolledtext
import testing  # Import the testing module

def main_gui():
    app = ctk.CTk()
    app.title("Input and Output Windows")
    app.geometry("800x400")

    # Create a frame for input
    input_frame = ctk.CTkFrame(master=app, width=390, height=400)
    input_frame.place(x=0, y=0)

    # Create a frame for output
    output_frame = ctk.CTkFrame(master=app, width=390, height=400)
    output_frame.place(x=410, y=0)

    # Textbox for output
    output_text = scrolledtext.ScrolledText(output_frame, width=45, height=20)
    output_text.pack(pady=20, padx=20)

    # Function to handle input and update output
    def handle_input():
        user_input = entry.get()
        result = testing.process_input(user_input)  # Use the function from testing.py
        output_text.insert("end", f"{result}\n")

    # Entry for input
    entry = ctk.CTkEntry(input_frame)
    entry.pack(pady=20, padx=20)

    # Button to submit input
    submit_button = ctk.CTkButton(input_frame, text="Submit", command=handle_input)
    submit_button.pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    main_gui()
