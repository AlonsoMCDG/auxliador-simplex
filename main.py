from decimal import Decimal, getcontext

def mostrar_tabela(tabela):
    # lista com o nomes das colunas; 
    # funçõoes com o valor de cada coluna.
    variaveis, funcoes = tabela

    largura = 9 # largura da coluna

    print('*** Tabela ***')

    # imprime o cabeçalho
    print(f'| {"f(x)":^{largura}} |', end='')
    for col in variaveis:
        print(f' {col:^{largura}} |', end='')
    print()

    # imprime as linhas
    for funcao, valores in funcoes.items():
        linha = f'| {funcao:^{largura}} |'

        for coluna in valores:
            linha += f' {coluna:^{largura}} |'

        print(linha)

def lista_decimal_para_float(lista):
    return [float(x) for x in lista]

def fazer_copia(tabela):
    variaveis, funcoes = tabela

    vars = variaveis
    funcs = {
        key: val.copy() for key, val in funcoes.items()
    }

    nova_tabela = (vars, funcs)

    return nova_tabela


def multiplicacao_escalar_da_linha(tabela, linha, escalar):
    tabela = fazer_copia(tabela)

    lin = tabela[1][linha]

    for col in range(len(lin)):
        lin[col] = lin[col] * escalar
    
    return tabela

def divisao_escalar_da_linha(tabela, linha, escalar):
    tabela = fazer_copia(tabela)

    lin = tabela[1][linha]

    for col in range(len(lin)):
        lin[col] = lin[col] / escalar
    
    return tabela

def calcular_razao_minima(tabela, coluna_pivo):
    vars, funcoes = tabela

    index_cp = vars.index(coluna_pivo)
    index_b = vars.index('b')

    print(f'Cálculo da razão mínima. (coluna pivô: \'{coluna_pivo}\')')

    for func, linha in funcoes.items():
        if func == 'z':
            continue # ignora a função objetivo

        valor_pivo = linha[index_cp]
        valor_b = linha[index_b]

        print(f'{func}: {valor_b} / {valor_pivo} ', end='')

        if valor_pivo == 0:
            print('-> prejudicada')
        else:
            print(f'= {valor_b / valor_pivo}')

def converter_valores_para_Decimal(funcoes):
    for funcao in funcoes.values():
        for i in range(len(funcao)):
            funcao[i] = Decimal(f'{funcao[i]}')
    
    return funcoes

#####

def get_escolha_menu():
    escolha = ''

    while True:
        print('Opções:')
        print('1. Multiplicar linha por um escalar')
        print('2. Dividir linha por um escalar')
        print('3. Mostrar tabela atual')
        print('0. Sair')
        
        try:
            escolha = int(input('Escolha: '))

            if 0 <= escolha <= 3:
                break
        except Exception as e:
            pass

    return escolha

def iniciar_modo_de_calculo(tabela):
    while True:
        escolha = get_escolha_menu()

        match escolha:
            case 1: pass # mutliplicar
            case 2: pass # dividir
            case 3: # mostrar tabela
                mostrar_tabela(tabela)
                pass
            case 0: break

    print('\nFim da execução.')

if __name__ == '__main__':
    getcontext().prec = 3  # define 3 casas decimais de precisão

    variaveis = ['x1a', 'x1b', 'x2', 'x3', 'xF1', 'xF2', 'b']
    funcoes = converter_valores_para_Decimal({
        'z':    [-3,  3, -7, -5, 0, 0,  0],
        'f1':   [ 3, -3,  1,  2, 1, 0,  9],
        'f2':   [-2,  2,  1,  3, 0, 1, 12]
    })

    tabela = (variaveis, funcoes)

    iniciar_modo_de_calculo(tabela)

    # mostrar_tabela(tabela)

    # coluna_pivo = 'x2'
    # calcular_razao_minima(tabela, coluna_pivo) # 'f1' tem a menor razão

    # linha_pivo = 'f1'
    # print(f'linha pivô: {lista_decimal_para_float(tabela[1][linha_pivo])}')

    # elemento_pivo = 1

    # nova_tabela = multiplicacao_escalar_da_linha(tabela, linha_pivo, elemento_pivo)

    # mostrar_tabela(nova_tabela)

