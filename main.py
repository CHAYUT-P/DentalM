import customtkinter as ctk
from ui.app import DentalManagementSystem

def main():
    root = ctk.CTk()
    app = DentalManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()