class Dados:
    def __init__(self):
        from banco_de_dados import Banco
        self.banco=Banco()
    def salvar_aluno(self,nome,aniversario):
        if not nome or not aniversario:
            return False, "Preencha os campos!"
        self.banco.inserir_registro(
            "Alunos",
            "nome,aniversario",
            (nome,aniversario))
        return True,"Aluno salvo com sucesso!"
    
    def salvar_materia(self,nome,turno,professor,sala):
        if not nome or not turno or not professor or not sala:
            return False, "Preencha os campos!"
        try:
            sala_int=int(sala)
        except ValueError:
            return False, "Digite apenas números inteiros!"
        self.banco.inserir_registro(
            "Materias",
            "nome,turno,professor,sala",
            (nome,turno,professor,sala_int))
        return True, "Aluno salvo com sucesso!"
    def salvar_notas(self,matricula,id_materia,nota):
        if not matricula or not id_materia or not nota:
            return False, "Preencha os campos"
        self.banco.inserir_registro(
            "Notas",
            "id_materia,matricula,nota",
            (id_materia,matricula,nota)
        )
        return True, "Nota inserida com sucesso!"
    def atualizar_alunos(self,nome,aniversario,matricula_int):
        set_partes=[]
        valores=[]

        if nome:
            set_partes.append("nome=?")
            valores.append(nome)
        if aniversario:
            set_partes.append("aniversario=?")
            valores.append(aniversario)
        if not set_partes:
            return False, "Nenhum dado para atualizar!"
        set_colunas_valores=", ".join(set_partes)
        where_condicao="matricula=?"
        valores.append(matricula_int)
        self.banco.atualizar_registro(
            "Alunos",
            set_colunas_valores,
            where_condicao,
            tuple(valores))
        return True,"Aluno atualizado com sucesso!"
    
    def atualizar_materia(self,materia,turno,ID_int,sala_int,professor):
        set_partes=[]
        valores=[]

        if materia:
            set_partes.append("nome=?")
            valores.append(materia)
        if turno:
            set_partes.append("turno=?")
            valores.append(turno)
        if sala_int:
            set_partes.append("sala=?")
            valores.append(sala_int)
        if professor:
            set_partes.append("professor=?")
            valores.append(professor)
        if not set_partes:
            return False, "Nenhum dado para atualizar!"
        set_colunas_valores=", ".join(set_partes)
        where_condicao="Id_materia=?"
        valores.append(ID_int)
        self.banco.atualizar_registro(
            "Materias",
            set_colunas_valores,
            where_condicao,
            tuple(valores))
        return True,"Materia atualizada com sucesso!"
    def atualizar_nota(self,matricula,id_materia,nota,matricula_original,id_materia_original):
        if nota == None:
            return False, "Nota inválida!"
        try:
            nota=float(nota)
            if nota <0 or nota>10:
                return False, "Nota deve ser entre 0 e 10!"
        except ValueError:
            return False, "Nota inválida"
        
        matricula_original=int(matricula_original)
        id_materia_original=int(id_materia_original)

        set_colunas_valores="id_materia=?,matricula=?,nota=?"
        where_condicao="id_materia=? AND matricula=?"
        valores=(id_materia,matricula,nota,id_materia_original,matricula_original)
        print("DEBUG UPDATE:", valores)
        self.banco.atualizar_registro(
            "Notas",
            set_colunas_valores,
            where_condicao,
            valores)
        return True,"Nota atualizada com sucesso!"
    def deletar_aluno(self,matricula_int):
        self.banco.deletar_registro(
            "Alunos",
            "matricula=?",
            (matricula_int,))
        return True, "Aluno deletado com sucesso!"
    
    def deletar_materia(self,ID_int):
        self.banco.deletar_registro(
            "Materias",
            "Id_materia=?",
            (ID_int,))
        return True, "Materia deletada com sucesso!"
    
    def deletar_nota(self,id_materia,matricula):
        self.banco.deletar_registro(
            "Notas",
            "id_materia=? And matricula=?",
            (id_materia,matricula)
        )
        return True, "Nota deletada com sucesso!"
    
    def listar_materias(self):
        from banco_de_dados import Banco
        banco = Banco()
        return banco.selecionar("Materias")
    
    def listar_materias_formatado(self):
        materias = self.listar_materias()
        
        resultado = []
        for linha in materias:
            resultado.append({
                "id": linha[0],
                "nome": linha[1],
                "turno": linha[2],
                "sala": linha[3],
                "professor": linha[4]
            })
        
        return resultado

    def exportar(self,tabela,tipo="txt"):
        if tabela not in self.banco.tabelas_validas:
            return False, f"Tabela inválida!"
        if tipo=="txt":
            sucesso=self.banco.exportar_registro_txt(tabela)
        elif tipo=="csv":
            sucesso=self.banco.exportar_registros_csv(tabela)
        elif tipo=="json":
            json_data=self.banco.exportar_registros_json(tabela)
            if json_data:
                with open(f"{tabela}.json","w",encoding="utf-8") as f:
                    f.write(json_data)
                sucesso=True
            else:
                sucesso=False
        else:
            return False, f"Formato {tipo} não suportado!"
        if sucesso:
            return True, f"{tabela} exportada com sucesso!"
        else:
            return False, f"Falha ao exportar {tabela} em {tipo.upper()}."