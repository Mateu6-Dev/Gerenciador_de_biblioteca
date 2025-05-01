import psycopg2 as conector
from faker import Faker
import tkinter as tk
from tkinter import ttk

class bancodados:
    def __init__(self):
        self.conexao = conector.connect(
            dbname="lojadb",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conexao.cursor()

    def criar_tabela(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS livros ( 
                id SERIAL PRIMARY KEY, 
                titulo VARCHAR(255), 
                autor VARCHAR(255), 
                ano_publicacao INTEGER, 
                genero VARCHAR(100) 
            ) 
        """)
        self.conexao.commit()

    def inserir_dados(self, titulo, autor, ano_publicacao, genero):
        self.cursor.execute("""
            INSERT INTO livros (titulo, autor, ano_publicacao, genero)
            VALUES (%s, %s, %s, %s)""", (titulo, autor, ano_publicacao, genero))
        self.conexao.commit()

    def selecionar_dados(self):
        self.cursor.execute("SELECT * FROM livros")
        return self.cursor.fetchall()


fake = Faker('pt_BR')
bd = bancodados()
bd.criar_tabela()
for _ in range(100):
    bd.inserir_dados(fake.text(max_nb_chars=20), fake.name(), fake.year(), fake.word())


class bibliotecagui:
    def __init__(self, root, bd):
        self.bd = bd
        self.root = root
        self.root.title('Gerenciador de biblioteca')

        self.tree = ttk.Treeview(root, columns=("ID", "Título", "Autor", "Ano", "Gênero"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Autor", text="Autor")
        self.tree.heading("Ano", text="Ano de publicação")
        self.tree.heading("Gênero", text="Gênero")
        self.tree.pack()

        self.carregar_dados()

    def carregar_dados(self):
        registros = self.bd.selecionar_dados()
        for registro in registros:
            self.tree.insert("", "end", values=registro)


root = tk.Tk()
app_bd = bancodados()
app_gui = bibliotecagui(root, app_bd)
root.mainloop()