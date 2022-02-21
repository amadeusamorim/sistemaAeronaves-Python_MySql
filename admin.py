import pymysql.cursors
import main
from time import sleep

linha = '-' * 50

class admin():
    def __init__(self):
        pass

    def conexao(self): # conexão para se conectar ao banco | será acionado em quase todo método
        try:
            self.banco = pymysql.connect(
                host='localhost',
                user='root',
                password='spfc2006',
                db='projetoaeronave',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('\033[0;31mErro ao conectar com o Banco de Dados.\033[m')

    def login(self):
        global autenticado
        self.conexao()
        email = input('Digite seu e-mail: ')
        senha = input('Senha: ')
        try:
            with self.banco.cursor() as cursos:
                cursos.execute('SELECT * from adm') # Executa esse comando no BD
                resultados = cursos.fetchall()
        except:
            print('Erro ao fazer a consulta com o Banco de Dados adm')
        for i in resultados:
            if email == i['email'] and senha == i['senha']: # Compara se as credenciais inseridas são as mesmas do BD
                autenticado = True
                break
            else:
                autenticado = False
                pass
        if autenticado:
            self.menuAdm() # Avança o Menu
        else:
            print('\033[0;31mDados errados! Tente novamente.\033[m')
            self.login() # Volta ao menu principal

    def VerificaEmail(self, email): # Função que verifica se o e-mail já existe para evitar duplicidade
        self.conexao()
        try:
            with self.banco.cursor() as cursos:
                cursos.execute('SELECT * from adm') # Acessa ao BD
                resultados = cursos.fetchall()
        except:
            print('Erro ao fazer a consulta com o Banco de Dados adm')
        for i in resultados:
            if email == i['email']:
                return 1
            else:
                pass
        return 0

    def cadastro(self): # Cadastrar novo usuário
        cod = '123'
        codigo = input('Digite o código verificador: ')
        if codigo == cod:
            nome = str(input('Nome: '))
            email = str(input('E-mail: '))
            senha = str(input('Senha: '))
            dados = [nome, email, senha, 1]
            self.conexao()
            n = self.VerificaEmail(email)
            if n == 1: # Caso já tenha e-mail no BD, não cadastra.
                print('E-mail existente. Tente realizar o login.')
                self.login()
            else: # Insere novos dados no BD.
                with self.banco.cursor() as cursos:
                    sql = 'INSERT INTO adm (nome, email, senha, status) VALUES (%s, %s, %s, %s)'
                    cursos.execute(sql, dados)
                    self.banco.commit()
                    print('Cadasrando informações...')
                    sleep(1)
                    print('\033[0;32mCadastrado!\033[m')
                    self.login()

    def menuAdm(self):
        print(linha)
        print(
            '1. Cadastrar nova aeronave.\n2. Alterar dados da aeronave.\n3. Deletar aeronave.\n4. Listar aeronaves.\n0. Sair.')
        print(linha)
        op = int(input('Digite a opção desejada: '))
        print(linha)
        if op == 0:
            return 0
        elif op == 1:
            modelo = str(input('Modelo: '))
            ano = int(input('Ano: '))
            cor = str(input('Cor: '))
            tipo = int(input('Tipo 1 -> Avião | 2 -> Helicoptério | 3 -> Drone: '))
            dadosAeronaves = [modelo, ano, cor, tipo]
            aeronaves().cadastrarAeronave(dadosAeronaves)
        elif op == 2:
            aeronaves().alterarAeronave()
        elif op == 3:
            aeronaves().deletarAeronave()
        elif op == 4:
            aeronaves().listarAeronave()


class aeronaves(admin):
    def __init__(self):
        pass

    def cadastrarAeronave(self, dadosAeronave):
        self.conexao()
        with self.banco.cursor() as cursos:
            sql = 'INSERT INTO aeronaves (modelo, ano, cor, tipo) VALUES (%s, %s, %s, %s)'
            cursos.execute(sql, dadosAeronave)
            self.banco.commit()
            print('Cadastrando nova aeronave...')
            sleep(1)
            print('\033[0;32mCadastrado!\033[m')
            self.menuAdm()

    def listarAeronave(self):
        self.conexao()
        try:
            with self.banco.cursor() as cursos:
                cursos.execute('SELECT * from aeronaves')
                aeronaves = cursos.fetchall()
        except:
            print('\033[0;31mErro ao fazer a consulta com o Banco de Dados aeronaves\033[m')
        print(linha)
        print('LISTA DE AERONAVES'.center(50))
        print(linha)
        for i in aeronaves:
            if i['tipo'] == 1:
                tipo = 'Avião'
            elif i['tipo'] == 2:
                tipo = 'Helicoptéro'
            else:
                tipo = 'Drone'
            print(
                f'ID: {i["idAeronave"]} - Modelo: {i["modelo"]} - Ano: {i["ano"]} - Cor: {i["cor"]} - Tipo: {i["tipo"]}')
        try:
            if autenticado:
                self.menuAdm()
        except:
            main.main()

    def deletarAeronave(self):
        self.conexao()
        id = int(input('Qual o ID da aeronave a ser deletada? '))
        print('Deletando...')
        sleep(1)
        with self.banco.cursor() as cursos:
            cursos.execute(f'DELETE FROM aeronaves WHERE idAeronave={id}')
            self.banco.commit()
            print('\033[0;34mDeletado!\033[m')
            sleep(1)
            self.menuAdm()

    def alterarAeronave(self):
        self.conexao()
        id = int(input('Qual o ID da aeronave quer deseja alterar? '))
        try:
            with self.banco.cursor() as cursos:
                cursos.execute(f'SELECT * from aeronaves WHERE idAeronave={id}')
                aeronaves = cursos.fetchall()
        except:
            print('Erro ao fazer a consulta com o Banco de Dados aeronaves')

        modelo = str(input(f'Modelo {aeronaves[0]["modelo"]}: ')).strip()
        ano = int(input(f'Ano {aeronaves[0]["ano"]}: '))
        cor = str(input(f'Cor {aeronaves[0]["cor"]}: ')).strip()
        tipo = int(input(f'Tipo {aeronaves[0]["tipo"]}: '))
        with self.banco.cursor() as cursos:
            cursos.execute(
                f'UPDATE aeronaves SET modelo="{modelo}", ano={ano}, cor="{cor}", tipo={tipo} WHERE idAeronave={id}')
            self.banco.commit()
            print('Atualizando dados...')
            sleep(1.5)
            print('Alterado!')
            self.menuAdm()
