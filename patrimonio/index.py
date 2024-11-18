import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('patrimonio.db')
cursor = conn.cursor()

# Criação das tabelas se não existirem
cursor.execute('''CREATE TABLE IF NOT EXISTS locais (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nome TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS patrimonios (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nome TEXT,
                  local_id INTEGER,
                  FOREIGN KEY(local_id) REFERENCES locais(id))''')

conn.commit()

# Função para adicionar um novo patrimônio
def adicionar_patrimonio():
    patrimonio_nome = simpledialog.askstring("Adicionar Patrimônio", "Nome do patrimônio:")
    if patrimonio_nome:
        locais = listar_locais()
        if locais:
            local_nome = simpledialog.askstring("Escolha o Local", f"Selecione um dos locais: {', '.join(locais)}")
            if local_nome in locais:
                local_id = buscar_local_id(local_nome)
                cursor.execute("INSERT INTO patrimonios (nome, local_id) VALUES (?, ?)", (patrimonio_nome, local_id))
                conn.commit()
                messagebox.showinfo("Sucesso", "Patrimônio adicionado com sucesso!")
                atualizar_listas()
            else:
                messagebox.showerror("Erro", "Local não encontrado.")
        else:
            messagebox.showerror("Erro", "Nenhum local cadastrado. Adicione um local primeiro.")
    else:
        messagebox.showerror("Erro", "Nome do patrimônio não pode ser vazio.")

# Função para adicionar um novo local
def adicionar_local():
    local_nome = simpledialog.askstring("Adicionar Local", "Nome do local:")
    if local_nome:
        cursor.execute("INSERT INTO locais (nome) VALUES (?)", (local_nome,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Local adicionado com sucesso!")
        atualizar_listas()
    else:
        messagebox.showerror("Erro", "Nome do local não pode ser vazio.")

# Função para buscar o ID do local pelo nome
def buscar_local_id(local_nome):
    cursor.execute("SELECT id FROM locais WHERE nome = ?", (local_nome,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

# Função para listar os locais cadastrados
def listar_locais():
    cursor.execute("SELECT nome FROM locais")
    locais = [row[0] for row in cursor.fetchall()]
    return locais

# Função para listar os patrimônios por local
def listar_patrimonios_por_local(local_id):
    cursor.execute("SELECT nome FROM patrimonios WHERE local_id = ?", (local_id,))
    return [row[0] for row in cursor.fetchall()]

# Função para atualizar as listas de patrimônio e locais
def atualizar_listas():
    list_locais.delete(0, tk.END)
    locais = listar_locais()
    for local in locais:
        list_locais.insert(tk.END, local)

    list_patrimonios.delete(0, tk.END)

# Função para mover patrimônio de um local para outro
def mover_patrimonio():
    patrimonio_selecionado = list_patrimonios.get(tk.ACTIVE)
    local_selecionado = list_locais.get(tk.ACTIVE)

    if patrimonio_selecionado and local_selecionado:
        novo_local = simpledialog.askstring("Mover Patrimônio", f"Para qual local deseja mover '{patrimonio_selecionado}'?")

        if novo_local in listar_locais():
            novo_local_id = buscar_local_id(novo_local)
            cursor.execute("UPDATE patrimonios SET local_id = ? WHERE nome = ?", (novo_local_id, patrimonio_selecionado))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Patrimônio '{patrimonio_selecionado}' movido para '{novo_local}'.")
            atualizar_listas()
        else:
            messagebox.showerror("Erro", "Local não encontrado.")
    else:
        messagebox.showerror("Erro", "Selecione um patrimônio e um local.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Sistema de Controle de Patrimônio")

frame = tk.Frame(root)
frame.pack(pady=20)

# Lista de locais
list_locais_label = tk.Label(frame, text="Locais")
list_locais_label.grid(row=0, column=0)

list_locais = tk.Listbox(frame)
list_locais.grid(row=1, column=0)

# Lista de patrimônios
list_patrimonios_label = tk.Label(frame, text="Patrimônios")
list_patrimonios_label.grid(row=0, column=1)

list_patrimonios = tk.Listbox(frame)
list_patrimonios.grid(row=1, column=1)

# Botões
btn_adicionar_local = tk.Button(frame, text="Adicionar Local", command=adicionar_local)
btn_adicionar_local.grid(row=2, column=0, pady=10)

btn_adicionar_patrimonio = tk.Button(frame, text="Adicionar Patrimônio", command=adicionar_patrimonio)
btn_adicionar_patrimonio.grid(row=2, column=1, pady=10)

btn_mover_patrimonio = tk.Button(frame, text="Mover Patrimônio", command=mover_patrimonio)
btn_mover_patrimonio.grid(row=3, column=1, pady=10)

# Inicia a interface com as listas atualizadas
atualizar_listas()

root.mainloop()

# Fecha a conexão com o banco de dados ao fechar o programa
conn.close()