import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dados import Dados
from config import criar_banco

class DashboardEscola(tk.Tk):
    def __init__(self):
        self.dados=Dados()
        super().__init__()

        style = ttk.Style(self)

        style.theme_use("default")  # evita bugs de tema

        style.configure("Treeview",
            background="#2d2d2d",
            foreground="white",
            rowheight=30,
            fieldbackground="#2d2d2d",
            font=("Arial", 11)
        )

        style.map("Treeview",
            background=[("selected", "#FF0101")],
            foreground=[("selected", "white")]
        )

        style.configure("Treeview.Heading",
            background="#1f1f1f",
            foreground="white",
            font=("Arial", 12, "bold")
        )
        self.title("Gerenciador de Escola")
        self.geometry("900x600")

        self.configure(bg="#fffefe")
        
        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_lateral=tk.Frame(self, width=200, bg="#2d2d2d")
        self.menu_lateral.grid(row=0,column=0,sticky="nsew")
        self.menu_lateral.grid_rowconfigure(False)

        tk.Label(self.menu_lateral,text="Admin",fg="white",bg="#2d2d2d",font=("Arial", 16 , "bold")).pack(pady=30)
        tk.Button(self.menu_lateral,text="Alunos",command=self.show_alunos,bg="#3d3d3d",fg="white",relief="flat",padx=20).pack(fill="x",pady=5)
        tk.Button(self.menu_lateral,text="Matérias",command=self.show_materias,bg="#3d3d3d",fg="white",relief="flat",padx=20).pack(fill="x",pady=5)
        tk.Button(self.menu_lateral,text="Notas",command=self.show_notas,bg="#3d3d3d",fg="white",relief="flat",padx=20).pack(fill="x",pady=5)

        self.container=tk.Frame(self, width=200, bg="#0000B1")
        self.container.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")

        self.show_alunos()

    def show_alunos(self):
        self.limpar_container()

        label=tk.Label(self.container,text="Cadastro de Aluno",fg="white",bg="#0000B1",font=("Arial",18))
        label.pack(pady=20)

        tk.Label(self.container, text="Nome do Aluno:", fg="white", bg="#0000B1").pack(pady=(10,0))
        self.ent_nome = tk.Entry(self.container, width=40, font=("Arial", 12))
        self.ent_nome.pack(pady=5)

        tk.Label(self.container, text="Data de aniversário:", fg="white", bg="#0000B1").pack(pady=(10,0))
        self.ent_data = tk.Entry(self.container, width=40, font=("Arial", 12))
        self.ent_data.pack(pady=5)


        frame_botoes = tk.Frame(self.container, bg="#0000B1")
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Salvar", command=self.salvar_aluno).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self.atualizar_aluno).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Deletar", command=self.deletar_aluno).pack(side="left", padx=5)

        tk.Label(self.container, text="", bg="#0000B1").pack()

        botao_exportar = tk.Menubutton(self.container, text="Exportar ▼", bg="#3d3d3d", fg="white", relief="flat")

        menu_exportar = tk.Menu(botao_exportar, tearoff=0)

        menu_exportar.add_command(label="Exportar como TXT", command=lambda: self.exportar_aluno("txt"))
        menu_exportar.add_command(label="Exportar como CSV", command=lambda: self.exportar_aluno("csv"))
        menu_exportar.add_command(label="Exportar como JSON", command=lambda: self.exportar_aluno("json"))

        botao_exportar.config(menu=menu_exportar)
        botao_exportar.pack(pady=5)

        self.tree=ttk.Treeview(self.container,columns=("matricula","nome","aniversario"),show="headings")
        
        self.tree.heading("matricula",text="Matrícula")
        self.tree.heading("nome",text="Nome")
        self.tree.heading("aniversario",text="Aniversário")

        self.tree.pack(fill="both",expand=True)

        self.tree.column("matricula", anchor="center", width=100)
        self.tree.column("nome", anchor="center", width=200)
        self.tree.column("aniversario", anchor="center", width=150)

        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item_aluno)

        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        self.refresh_tabela_alunos()
    
    def show_materias(self):
        self.limpar_container()

        label=tk.Label(self.container,text="Cadastro de Matérias",fg="white",bg="#0000B1",font=("Arial",18))
        label.pack(pady=20)

        tk.Label(self.container, text="Nome da Matéria:", fg="white", bg="#0000B1").pack(pady=(10,0))
        self.ent_materia = tk.Entry(self.container, width=40, font=("Arial", 12))
        self.ent_materia.pack(pady=5)

        tk.Label(self.container, text="Turno:", fg="white", bg="#0000B1").pack(pady=(10,0))
        self.ent_turno = tk.Entry(self.container, width=40, font=("Arial", 12))
        self.ent_turno.pack(pady=5)

        tk.Label(self.container, text="Sala:", fg="white", bg="#0000B1").pack(pady=(10,0))
        self.ent_sala = tk.Entry(self.container, width=40, font=("Arial", 12))
        self.ent_sala.pack(pady=5)

        tk.Label(self.container, text="Nome do professor:", fg="white", bg="#0000B1").pack(pady=(10,0))
        self.ent_professor = tk.Entry(self.container, width=40, font=("Arial", 12))
        self.ent_professor.pack(pady=5)

        frame_botoes = tk.Frame(self.container, bg="#0000B1")
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Salvar", command=self.salvar_materia).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self.atualizar_materia).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Deletar", command=self.deletar_materia).pack(side="left", padx=5)

        tk.Label(self.container, text="", bg="#0000B1").pack()

        botao_exportar = tk.Menubutton(self.container, text="Exportar ▼", bg="#3d3d3d", fg="white", relief="flat")

        menu_exportar = tk.Menu(botao_exportar, tearoff=0)

        menu_exportar.add_command(label="Exportar como TXT", command=lambda: self.exportar_materia("txt"))
        menu_exportar.add_command(label="Exportar como CSV", command=lambda: self.exportar_materia("csv"))
        menu_exportar.add_command(label="Exportar como JSON", command=lambda: self.exportar_materia("json"))

        botao_exportar.config(menu=menu_exportar)
        botao_exportar.pack(pady=5)

        self.tree=ttk.Treeview(self.container,columns=("id_materia","materia","turno","sala","professor"),show="headings")
        
        self.tree.heading("id_materia",text="ID")
        self.tree.heading("materia",text="Matéria")
        self.tree.heading("turno",text="Turno")
        self.tree.heading("sala",text="Sala")
        self.tree.heading("professor",text="Professor")

        self.tree.pack(fill="both",expand=True)

        self.tree.column("id_materia", anchor="center", width=100)
        self.tree.column("materia", anchor="center", width=200)
        self.tree.column("turno", anchor="center", width=200)
        self.tree.column("sala", anchor="center", width=100)
        self.tree.column("professor", anchor="center", width=150)

        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item_materia)

        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        self.refresh_tabela_materias()

    def show_notas(self):
        self.limpar_container()

        label=tk.Label(self.container,text="Cadastro de Notas",fg="white",bg="#0000B1",font=("Arial",18))
        label.pack(pady=20)

        tk.Label(self.container, text="Matrícula do Aluno:", fg="white", bg="#0000B1").pack(pady=(10,0))
        self.ent_matricula = tk.Entry(self.container, width=40, font=("Arial", 12))
        self.ent_matricula.pack(pady=5)

        tk.Label(self.container, text="Matéria:",fg="white", bg="#0000B1").pack(pady=(10, 0))

        self.combo_materias = ttk.Combobox(self.container, state="readonly", width=37)
        self.combo_materias.pack(pady=5)

        dados=self.dados.listar_materias_formatado()

        self.materias_dict={}
        lista_materias=[]

        for materia in dados:
            texto=f"{materia["nome"]} (Sala{materia["sala"]})"

            lista_materias.append(texto)
            self.materias_dict[texto]=materia["id"]
        
        self.combo_materias['values']=lista_materias

        tk.Label(self.container, text="Nota do aluno:", fg="white", bg="#0000B1").pack(pady=(10,0))
        self.ent_nota = tk.Entry(self.container, width=40, font=("Arial", 12))
        self.ent_nota.pack(pady=5)

        frame_botoes = tk.Frame(self.container, bg="#0000B1")
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes,text="Salvar",command=self.salvar_notas).pack(side="left", padx=5)

        tk.Button(frame_botoes,text="atualizar",command=self.atualizar_notas).pack(side="left", padx=5)

        tk.Button(frame_botoes,text="Deletar",command=self.deletar_notas).pack(side="left", padx=5)

        tk.Label(self.container, text="", bg="#0000B1").pack()

        botao_exportar = tk.Menubutton(self.container, text="Exportar ▼", bg="#3d3d3d", fg="white", relief="flat")

        menu_exportar = tk.Menu(botao_exportar, tearoff=0)

        menu_exportar.add_command(label="Exportar como TXT", command=lambda: self.exportar_nota("txt"))
        menu_exportar.add_command(label="Exportar como CSV", command=lambda: self.exportar_nota("csv"))
        menu_exportar.add_command(label="Exportar como JSON", command=lambda: self.exportar_nota("json"))

        botao_exportar.config(menu=menu_exportar)
        botao_exportar.pack(pady=5)
        
        self.tree=ttk.Treeview(self.container,columns=("id_materia","matricula","nota"),show="headings")
        
        self.tree.heading("id_materia",text="ID")
        self.tree.heading("matricula",text="Matricula")
        self.tree.heading("nota",text="Nota")

        self.tree.pack(fill="both",expand=True)

        self.tree.column("id_materia", anchor="center", width=200)
        self.tree.column("matricula", anchor="center", width=200)
        self.tree.column("nota", anchor="center", width=200)

        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item_nota)

        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.refresh_tabela_notas()

    def selecionar_item_aluno(self, event):
        print("clique detectado")
        item=self.tree.selection()

        if item:
            valores=self.tree.item(item[0],"values")

            self.matricula_selecionada=valores[0]

            self.ent_nome.delete(0,tk.END)
            self.ent_nome.insert(0,valores[1])

            self.ent_data.delete(0,tk.END)
            self.ent_data.insert(0,valores[2])

    def selecionar_item_materia(self, event):
        print("clique detectado")
        item=self.tree.selection()

        if item:
            valores=self.tree.item(item[0],"values")

            self.ID_selecionada=valores[0]

            self.ent_materia.delete(0,tk.END)
            self.ent_materia.insert(0,valores[1])

            self.ent_turno.delete(0,tk.END)
            self.ent_turno.insert(0,valores[2])

            self.ent_sala.delete(0,tk.END)
            self.ent_sala.insert(0,valores[3])

            self.ent_professor.delete(0,tk.END)
            self.ent_professor.insert(0,valores[4])

    def selecionar_item_nota(self,event):
        item=self.tree.selection()
        if item:
            valores=self.tree.item(item[0],"values")

            self.ID_selecionada=int(valores[0])
            self.matricula_selecionada=int(valores[1])

            self.id_materia_original = valores[0]
            self.matricula_original = valores[1]

            self.ent_nota.delete(0,tk.END)
            self.ent_nota.insert(0,valores[2])

            for texto, id_materia in self.materias_dict.items():
                if id_materia == int(valores[0]):
                    self.combo_materias.set(texto)
                    break
    def limpar_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()    
    
    def salvar_aluno(self):
        nome=self.ent_nome.get()
        aniversario=self.ent_data.get()

        sucesso,msg=self.dados.salvar_aluno(nome,aniversario)
        self.mostrar_feedback(msg,sucesso)

        self.refresh_tabela_alunos()
        self.novo_aluno()

    def salvar_materia(self):
        nome_materia=self.ent_materia.get()
        turno=self.ent_turno.get()
        professor=self.ent_professor.get()
        sala=self.ent_sala.get()

        sucesso,msg=self.dados.salvar_materia(nome_materia,turno,professor,sala)
        self.mostrar_feedback(msg,sucesso)

        self.refresh_tabela_materias()
        self.nova_materia()
    
    def salvar_notas(self):
        matricula = self.ent_matricula.get()
        materia_selecionada=self.combo_materias.get()
        nota = self.ent_nota.get().replace(",",".")

        try:
            matricula = int(matricula)
        except ValueError:
            self.mostrar_feedback("Matrícula inválida!", False)
            return

        if materia_selecionada not in self.materias_dict:
            self.mostrar_feedback("Selecione uma matéria válida!", False)
            return

        id_materia = self.materias_dict[materia_selecionada]

        try:
            nota=float(nota)
        except ValueError:
            self.mostrar_feedback("Insira valores entre 0 a 10!", False)
            return
        
        print("MATRICULA:", matricula)
        print("ID_MATERIA:", id_materia)
        print("NOTA:", nota)

        sucesso, msg = self.dados.salvar_notas(matricula, id_materia, nota)
        self.mostrar_feedback(msg, sucesso)
        self.refresh_tabela_notas()
        self.nova_nota()

    def atualizar_aluno(self):
        if not hasattr(self, "matricula_selecionada"):
            print("Selecione um aluno na tabela!")
            return False
        nome=self.ent_nome.get()
        aniversario=self.ent_data.get()
        matricula_int = int(self.matricula_selecionada)

        sucesso,msg=self.dados.atualizar_alunos(nome,aniversario,matricula_int)
        self.mostrar_feedback(msg,sucesso)
        
        self.refresh_tabela_alunos()
        self.novo_aluno()

    def atualizar_materia(self):
        if not hasattr(self, "ID_selecionada"):
            print("Selecione uma matéria na tabela!")
            return False
        materia=self.ent_materia.get()
        turno=self.ent_turno.get()
        ID_int = int(self.ID_selecionada)
        sala=self.ent_sala.get()
        sala_int=int(sala)
        professor=self.ent_professor.get()

        sucesso,msg=self.dados.atualizar_materia(materia,turno,ID_int,sala_int,professor)
        self.mostrar_feedback(msg,sucesso)
        
        self.refresh_tabela_materias()
        self.nova_materia()
    
    def atualizar_notas(self):
        if not hasattr(self, "ID_selecionada") or not hasattr(self,"matricula_selecionada"):
            return False,"Selecione uma ID de matéria ou matricula na tabela!"
        matricula=int(self.matricula_selecionada)
        
        materia_selecionada=self.combo_materias.get()
        if materia_selecionada not in self.materias_dict:
            return False,"Selecione uma matéria válida!"
        id_materia=self.materias_dict[materia_selecionada]

        try:
            nota=float(self.ent_nota.get().replace(",","."))
        except ValueError:
            return False,"Nota inválida!"
        sucesso,msg=self.dados.atualizar_nota(matricula,id_materia,nota,self.matricula_original,self.id_materia_original)
        self.mostrar_feedback(msg,sucesso)
        
        self.refresh_tabela_notas()
        self.nova_nota()  
        
    def refresh_tabela_alunos(self):
        from banco_de_dados import Banco
        banco = Banco()
        dados = banco.selecionar("Alunos")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, linha in enumerate(dados):
            if i % 2 == 0:
                self.tree.insert("", "end", values=linha, tags=("par",))
            else:
                self.tree.insert("", "end", values=linha, tags=("impar",))

        self.tree.tag_configure("par", background="#3a3a3a")
        self.tree.tag_configure("impar", background="#2d2d2d")

    def refresh_tabela_materias(self):
        from banco_de_dados import Banco
        banco = Banco()
        dados = banco.selecionar("Materias")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, linha in enumerate(dados):
            if i % 2 == 0:
                self.tree.insert("", "end", values=linha, tags=("par",))
            else:
                self.tree.insert("", "end", values=linha, tags=("impar",))

        self.tree.tag_configure("par", background="#3a3a3a")
        self.tree.tag_configure("impar", background="#2d2d2d")
    
    def refresh_tabela_notas(self):
        from banco_de_dados import Banco
        banco = Banco()
        dados = banco.selecionar("Notas")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, linha in enumerate(dados):
            if i % 2 == 0:
                self.tree.insert("", "end", values=linha, tags=("par",))
            else:
                self.tree.insert("", "end", values=linha, tags=("impar",))

        self.tree.tag_configure("par", background="#3a3a3a")
        self.tree.tag_configure("impar", background="#2d2d2d")
        
    def deletar_aluno(self):
        if not hasattr(self,"matricula_selecionada"):
            return False,"selecione uma matrícula da tabela!"
        
        matricula_int=int(self.matricula_selecionada)

        resposta=messagebox.askyesno("Confirmação",f"Tem certeza quem quer deletar o aluno da matrícula {matricula_int}?")
        if not resposta:
            return False
        sucesso,msg=self.dados.deletar_aluno(matricula_int)
        self.mostrar_feedback(msg,sucesso)
        self.refresh_tabela_alunos()

        del self.matricula_selecionada
    
    def deletar_materia(self):
        if not hasattr(self,"ID_selecionada"):
            return False,"selecione uma ID da tabela!"
        
        ID_int=int(self.ID_selecionada)

        resposta=messagebox.askyesno("Confirmação",f"Tem certeza quem quer deletar o aluno da matrícula {ID_int}?")
        if not resposta:
            return False
        sucesso,msg=self.dados.deletar_materia(ID_int)
        self.mostrar_feedback(msg,sucesso)
        self.refresh_tabela_alunos()

        del self.ID_selecionada

    def deletar_notas(self):
        if not hasattr(self, "ID_selecionada") or not hasattr(self,"matricula_selecionada"):
            return False,"Selecione uma ID de matéria ou matricula na tabela!"
        matricula=int(self.matricula_selecionada)
        id_materia=int(self.ID_selecionada)
        resposta=messagebox.askyesno("Confirmação",f"Tem certeza quem quer deletar o aluno da matrícula {matricula}?")
        if not resposta:
            return False
        sucesso,msg=self.dados.deletar_nota(matricula,id_materia)
        self.mostrar_feedback(msg,sucesso)
        self.refresh_tabela_alunos()

        del self.ID_selecionada
        del self.matricula_selecionada

    def novo_aluno(self):
        self.ent_nome.delete(0, tk.END)
        self.ent_data.delete(0, tk.END)

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        if hasattr(self, "matricula_selecionada"):
            del self.matricula_selecionada

        print("Modo novo aluno ativado")

    def nova_materia(self):
        self.ent_materia.delete(0, tk.END)
        self.ent_turno.delete(0, tk.END)
        self.ent_sala.delete(0, tk.END)
        self.ent_professor.delete(0, tk.END)

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        if hasattr(self, "ID_selecionada"):
            del self.ID_selecionada

        print("Modo nova matéria ativado")
    
    def nova_nota(self):

        if hasattr(self, "ID_selecionada"):
            del self.ID_selecionada
        if hasattr(self, "matricula_selecionada"):
            del self.matricula_selecionada

        print("Modo nova Nota ativado")

    def exportar_aluno(self,formato):
        sucesso,msg=self.dados.exportar("Alunos",formato)
        self.mostrar_feedback(msg,sucesso)

    def exportar_materia(self,formato):
        sucesso,msg=self.dados.exportar("Materias",formato)
        self.mostrar_feedback(msg,sucesso)
    
    def exportar_nota(self,formato):
        sucesso,msg=self.dados.exportar("Notas",formato)
        self.mostrar_feedback(msg,sucesso)

    def mostrar_feedback(self, msg, sucesso=True):

        if hasattr(self, "lbl_feedback") and self.lbl_feedback.winfo_exists():
            self.lbl_feedback.destroy()

        cor = "#4CAF50" if sucesso else "#FF5252"

        self.lbl_feedback = tk.Label(
            self.container,
            text=msg,
            fg="white",
            bg=cor,
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5
        )
        
        self.lbl_feedback.pack(pady=5)

        
        self.lbl_feedback.after(3000, self.lbl_feedback.destroy)
if __name__=="__main__":
    criar=criar_banco()
    app=DashboardEscola()
    app.mainloop()