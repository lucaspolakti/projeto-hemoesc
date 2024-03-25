import tkinter as tk
from tkinter import messagebox

def exibir_mensagem():
    messagebox.showinfo("Mensagem", "Olá! Você clicou no botão.")

# Criando a janela principal
root = tk.Tk()
root.title("Exemplo de Frontend em Python")

# Criando um botão na janela
botao = tk.Button(root, text="Clique Aqui", command=exibir_mensagem)
botao.pack(pady=20)

# Executando o loop principal da aplicação
root.mainloop()