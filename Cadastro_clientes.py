from tkinter import* 
from tkinter import ttk
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
from reportlab.platypus import SimpleDocTemplate
import webbrowser
import os


root = Tk()

class Funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.telefone_entry.delete(0, END)


    def conecta_bd(self):
        self.conn = sqlite3.connect("cliente.db") ; print("Conectando ao banco de dados")
        self.cursor = self.conn.cursor()


    def desconecta_bd(self):
        self.conn.close() ; print("Banco de Dados Desconectado")


    def montaTablelas(selfD):
        selfD.conecta_bd()
        selfD.cursor.execute("""
           CREATE TABLE IF NOT EXISTS clientes (
              cod INTEGER PRIMARY KEY,
              nome_cliente CHAR(40) NOT NULL,
              telefone INTERGER(20),
              cidade CHAR(40)
            )
        """
        )
        selfD.conn.commit(); print("Banco de Dados criado")


    def add_clientes(self):
        self.codigo =  self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
                            VALUES (?, ? , ?)""" , (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()


    def select_lista(self):
        self.listcli.delete(*self.listcli.get_children())
        self.conecta_bd()

        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
                                    ORDER BY nome_cliente ASC""")
        
        for i in lista:
            self.listcli.insert("", END, values=i)
        self.desconecta_bd()


    def OnDoubleclick(self,event): 
        self.limpa_tela()
        self.listcli.selection()

        for n in self.listcli.selection():
            col1, col2, col3, col4 = self.listcli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)


    def delete_cliente(self):
        self.codigo =  self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()


    def altera(self):
        self.codigo =  self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ? , cidade = ? WHERE cod = ?""",(self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
        
    def busca_cliente(self):
        self.conecta_bd()
        self.listcli.delete(*self.listcli.get_children())
        self.nome_entry.insert(END, '')
        nome = self.nome_entry.get() + '%'
        self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomecli = self.cursor.fetchall()
        for i in buscanomecli:
            self.listcli.insert("", END, value=i)
            self.limpa_tela
        self.desconecta_bd()
    

class application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_de_tela()
        self.widget_frame_1()
        self.lista_frame_2()
        self.montaTablelas()
        self.select_lista()
        root.mainloop()


    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background="#DDD8C4")
        self.root.geometry("700x600") 
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=800) 
        self.root.minsize(width=500, height=400)


    def frames_de_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg="#ADD8E6", highlightbackground="#84B59F", highlightthickness=3 )
        self.frame_1.place(relx=0.02 ,rely=0.02 ,relwidth=0.96 ,relheight=0.46,) 
        
        self.frame_2 = Frame(self.root, bd=4, bg="#ADD8E6", highlightbackground="#84B59F", highlightthickness=3 )
        self.frame_2.place(relx=0.02 ,rely=0.5 ,relwidth=0.96 ,relheight=0.46,) 


    def widget_frame_1(self):
        button_style = {
            'bd': 2,
            'bg': '#4CAF50',  
            'fg': 'Black',  
            'font': ('verdana', 10, 'bold')  
        }

        self.bt_limpar = Button(self.frame_1, text="LIMPAR", command=self.limpa_tela, **button_style)
        self.bt_limpar.place(relx=0.22, rely=0.05, relwidth=0.10, relheight=0.10)

        self.bt_buscar = Button(self.frame_1, text="BUSCAR", command=self.busca_cliente, **button_style)
        self.bt_buscar.place(relx=0.32, rely=0.05, relwidth=0.10, relheight=0.10)

        self.bt_alterar = Button(self.frame_1, text="ALTERAR", command=self.altera, **button_style)
        self.bt_alterar.place(relx=0.58, rely=0.05, relwidth=0.10, relheight=0.10)

        self.bt_novo = Button(self.frame_1, text="INSERIR", command=self.add_clientes, **button_style)
        self.bt_novo.place(relx=0.68, rely=0.05, relwidth=0.10, relheight=0.10)

        self.bt_apagar = Button(self.frame_1, text="APAGAR", command=self.delete_cliente, **button_style)
        self.bt_apagar.place(relx=0.78, rely=0.05, relwidth=0.10, relheight=0.10)

        label_style = {
            'bd': 2,
            'bg': '#ADD8E6',  
            'fg': '#13495A',  
            'font': ("verdana", 10, 'bold', 'italic')
        }

        self.lb_codigo = Label(self.frame_1, text="Código", **label_style)
        self.lb_codigo.place(relx=0.05, rely=0.01)
        self.codigo_entry = Entry(self.frame_1, bd=2)
        self.codigo_entry.place(relx=0.05, rely=0.08, relwidth=0.1, relheight=0.07)

        self.lb_nome = Label(self.frame_1, text="Nome", **label_style)
        self.lb_nome.place(relx=0.05, rely=0.25)
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.32, relwidth=0.80, relheight=0.07)

        self.lb_telefone = Label(self.frame_1, text="Telefone", **label_style)
        self.lb_telefone.place(relx=0.05, rely=0.50)
        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.58, relwidth=0.38, relheight=0.07)

        self.lb_cidade = Label(self.frame_1, text="Cidade", **label_style)
        self.lb_cidade.place(relx=0.50, rely=0.50)
        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.50, rely=0.58, relwidth=0.38, relheight=0.07)

    def lista_frame_2(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('verdana', 10, 'bold'), background='#4CAF50', foreground='white')  # Estilo dos cabeçalhos
        style.configure("Treeview", font=('verdana', 9))  

        self.listcli = ttk.Treeview(self.frame_2, height=2, columns=("col1", "col2", "col3", "col4"))
        self.listcli.place(relx=0.01, rely=0.01, relwidth=0.97, relheight=0.98)

        self.scroollista = Scrollbar(self.frame_2, orient='vertical')
        self.scroollista.configure(command=self.listcli.yview)
        self.scroollista.place(relx=0.98, rely=0.01, relwidth=0.03, relheight=0.98)

        self.listcli.heading("#0", text="")
        self.listcli.heading("#1", text="Código")
        self.listcli.heading("#2", text="Nome")
        self.listcli.heading("#3", text="Telefone")
        self.listcli.heading("#4", text="Cidade")

        self.listcli.column("#0", width=1)
        self.listcli.column("#1", width=50)
        self.listcli.column("#2", width=200)
        self.listcli.column("#3", width=125)
        self.listcli.column("#4", width=125)

        self.listcli.bind("<Double-1>", self.OnDoubleclick)


application()