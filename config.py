import sqlite3

db_file="escola.db"

def criar_banco():
    try:
        conexao=sqlite3.connect(db_file)
        cursor=conexao.cursor()
        cursor.execute("PRAGMA foreign_keys= ON")

        cursor.execute("CREATE TABLE IF NOT EXISTS Alunos(matricula integer NOT NULL AUTO_INCREMENT primary key, nome text)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Materias(id integer primary key, nome text, grade integer)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Notas(matricula integer,id integer,nota float,FOREIGN KEY(matricula) REFERENCES Aluno(matricula),FOREIGN KEY(id) REFERENCES Materia(id))")
        conexao.commit()
        print("Tabelas criadas!")
        cursor.close()
        conexao.close()
    except sqlite3.Error:
        print("conexão falhou!")
def get_conexao():
    return sqlite3.connect(db_file)