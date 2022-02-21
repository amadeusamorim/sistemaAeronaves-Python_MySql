import admin as adm
from time import sleep
linha = '-'*50


def main():
    print(linha)
    print('SISTEMA DE AERONAVES'.center(50))
    print(linha)
    sleep(1)
    print('1. Para logar como Administrador.\n2. Para cadastrar um usuário. \n3. Ver catálogo. \n0. Para sair.')
    print(linha)
    sleep(1)
    op = int(input('Digite a opção desejada: '))
    print(linha)
    if op == 1:
        adm.admin().login()
    elif op == 2:
        adm.admin().cadastro()
    elif op == 3:
        adm.aeronaves().listarAeronave()
    else:
        pass


if __name__ == '__main__':
    main()
