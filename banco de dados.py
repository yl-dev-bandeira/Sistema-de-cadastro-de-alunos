from config import get_conexao
import sqlite3
import json

db_file="escola.db"

tabelas_validas=["Aluno","Materia","Notas"]

def validar_dados(tabelas,valores):
    if tabelas=="Alunos":
        nome=valores[0]
        if not nome or not isinstance(nome,str):
            print("Erro: nome ou tipo está errado!")
            return False
    elif tabelas=="Materias":
        nome,grade=valores
        if not nome or not isinstance(nome,str):
            print("Erro: nome ou tipo está errado!")
            return False
        if not isinstance(grade,int) or grade<0:
            print("Erro: tipo ou horas insuficientes!")
            return False
    elif tabelas=="notas":
        matricula,id_materia,nota=valores
        if not isinstance(nota,(int,float)) or nota<0 or nota>10:
            print("Erro: nota inválida!")
            return False
    return True
def inserir_registro(tabela,colunas,valores):
    if tabela not in tabelas_validas:
        print("Tabela inválida")
        return False
    if not validar_dados(tabela,valores):
        return False
    placeholders=",".join(["?"]*len(valores))
    try:
        with get_conexao as conn:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO {tabela}({colunas}) VALUES({placeholders})",valores)
            conn.commit()
            print(f"Registros inseridos com sucesso!")
    except sqlite3.IntegrityError as e:
            print("Erro de integridade: ",e)
    except sqlite3.Error as e:
            print("Erro ao acessar o banco de dados: ",e)
def selecionar(tabela,colunas="*"):
    if tabela not in tabelas_validas:
        print("Tabela inválida")
        return False
    try:
        with get_conexao as conn:
            cursor=conn.cursor()
            cursor.execute(f"SELECT {colunas} FROM {tabela}")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error ao acessar o banco de dados: ",e)
        return []
def selecionar_registros_json(tabela, colunas="*"):
    if tabela not in tabelas_validas:
        print("Tabela inválida!")
        return json.dumps([])
    try:
        with get_conexao as conn:
            cursor=conn.cursor()
            cursor.execute(f"SELECT {colunas} FROM {tabela}")
            linhas=cursor.fetchall()
            nomes_colunas=[desc[0]for desc in cursor.description]
            lista_dict=[dict(zip(nomes_colunas,linha))for linha in linhas]
            return json.dumps(lista_dict,indent=4,ensure_ascii=False)
    except sqlite3.Error as e:
        print("Error ao acessar o banco de dados: ",e)
        return json.dumps([])
def atualizar_registro(tabela,set_colunas_valores,where_condicao,where_valores):
    if tabela not in tabelas_validas:
        print("Tabela inválida")
        return False
    try:
        with get_conexao as conn:
            cursor=conn.cursor()
            cursor.execute(f"UPDATE {tabela} SET {set_colunas_valores} WHERE {where_condicao}",where_valores)
            conn.commit()
            print(f"Atualizado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar: ",e)
def deletar_registro(tabela,where_condicao,where_valores):
    if tabela not in tabelas_validas:
        print("Tabela inválida")
        return False
    try:
        with get_conexao as conn:
            cursor=conn.cursor()
            cursor.execute(f"Delete FROM {tabela} WHERE {where_condicao}",where_valores)
            conn.commit()
            print(f"Deletado com sucesso!")
    except sqlite3.Error as e:
        print("Erro ao deletar registros: ",e)