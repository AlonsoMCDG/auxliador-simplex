from decimal import Decimal, getcontext

def print_format(num):
    pass

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

def multiplicacao_escalar(linha, escalar):
    linha = linha.copy()
    for i in range(len(linha)):
        linha[i] *= escalar
    return linha

def divisao_escalar(linha, escalar):
    if escalar == 0:
        return
    
    linha = linha.copy()
    for i in range(len(linha)):
        linha[i] /= escalar
    
    return linha

def somar_linhas(linha_1, linha_2):
    soma = [linha_1[i] + linha_2[i] for i in range(len(linha_1))]

    return soma

def fazer_copia(tabela):
    variaveis, funcoes = tabela

    vars = variaveis
    funcs = { key: val.copy() for key, val in funcoes.items() }
    nova_tabela = (vars, funcs)

    return nova_tabela

def recalcular_linhas_tabela(tabela, funcao_pivo, variavel_pivo):
    tabela = fazer_copia(tabela)
    vars, funcs = tabela

    index_colula_pivo = vars.index(variavel_pivo)
    linha_pivo = funcs[funcao_pivo]
    linha_pivo = divisao_escalar(linha_pivo, funcs[funcao_pivo][index_colula_pivo]) # nova linha pivo

    for f, linha in funcs.items():
        
        # altera somente a linha pivô
        if f == funcao_pivo:
            funcs[f] = linha_pivo
            continue

        # altera as demais linhas

        coeficiente_pivo = linha[index_colula_pivo]
        linha_pivo_escalonada = multiplicacao_escalar(linha_pivo, (-1) * coeficiente_pivo)

        funcs[f] = somar_linhas(linha, linha_pivo_escalonada)
    
    return tabela


if __name__ == '__main__':
    tabela = (
        ['x1+', 'x1-', 'x2', 'x3', 'xF1', 'xF2', 'b'],
        {
            'z': [Decimal('-3'), Decimal('3'), Decimal('-7'), Decimal('-5'), Decimal('0'), Decimal('0'), Decimal('0')],
            'xF1': [Decimal('3'), Decimal('-3'), Decimal('1'), Decimal('2'), Decimal('1'), Decimal('0'), Decimal('9')],
            'xF2': [Decimal('-2'), Decimal('2'), Decimal('1'), Decimal('3'), Decimal('0'), Decimal('1'), Decimal('12')]
        }
    )

