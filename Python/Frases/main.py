# main.py

import tkinter as tk
from app_gui import AplicacaoLembretesFrases # Importa a classe da sua GUI

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoLembretesFrases(root)
    root.mainloop()