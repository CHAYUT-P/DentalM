import customtkinter as ctk

class HomeView:
    def __init__(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(frame, text="Welcome to Dental Management System", font=("Arial", 22)).pack(pady=20)
        ctk.CTkLabel(frame, text="Use the left menu to navigate.", font=("Arial", 14)).pack(pady=10)