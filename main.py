import tkinter as tk
from tkinter import ttk
import calculo as calc
from decimal import Decimal

class Tela(tk.Frame):
    class Tabela:
        def __init__(self, master, controlador, titulo = 'Tabela', tabela = None, tk_vars = None):
            self.frm_tabela = master
            self.titulo_tabela = tk.StringVar(value=titulo)

            self.tk_vars = tk_vars

            if tk_vars is None:
                self.tk_vars = {
                    'variaveis': [], # rótulos das variáveis
                    'funcoes': {}, # coeficientes de cada variável de cada função restritiva
                    'pivos': {'linha': tk.StringVar(value='f1'), 'coluna': tk.StringVar(value='x2')} # linha e coluna pivôs
                }

            # tabela --> ([variáveis], {funções})
            self.tabela = tabela
            variaveis, funcoes = ([], dict())

            if tabela is not None:
                variaveis, funcoes = tabela
            else:
                # valores padrão, para exemplo
                variaveis = ['x1a', 'x1b', 'x2', 'x3', 'xF1', 'xF2', 'b']
                funcoes = {
                    'z': [Decimal('-3'), Decimal('3'), Decimal('-7'), Decimal('-5'), Decimal('0'), Decimal('0'), Decimal('0')],
                    'f1': [Decimal('3'), Decimal('-3'), Decimal('1'), Decimal('2'), Decimal('1'), Decimal('0'), Decimal('9')],
                    'f2': [Decimal('-2'), Decimal('2'), Decimal('1'), Decimal('3'), Decimal('0'), Decimal('1'), Decimal('12')]
                }
            

            tk.Label(self.frm_tabela, textvariable=self.titulo_tabela, bg="#d8d8d8"
                     ).grid(row=0, column=0, columnspan=len(variaveis) + 1, sticky='nswe')

            ### variáveis

            linha_atual = 1 # linha atual no gerenciador grid()

            tk.Label(self.frm_tabela, text='Variáveis:').grid(row=linha_atual, column=0)

            self.tk_vars['variaveis'] = [tk.StringVar(value=v) for v in variaveis]

            for col in range(len(variaveis)):
                celula = tk.Entry(self.frm_tabela, width=8, textvariable=self.tk_vars['variaveis'][col])
                celula.grid(row=linha_atual, column=1+col)
            linha_atual += 1
            
            ### coeficientes das funções

            tk.Label(self.frm_tabela, text='Coeficientes:'
                     ).grid(row=linha_atual, column=0)
            ttk.Separator(self.frm_tabela, orient='horizontal', 
                          ).grid(row=linha_atual, column=1, 
                                 columnspan=len(variaveis), sticky='we',
                                 padx=5)
            linha_atual += 1

            # definir as variáveis tk da funções
            for f in funcoes:
                self.tk_vars['funcoes'][f] = [tk.StringVar(value=f'{funcoes[f][col]}') for col in range(len(variaveis))]
            
            # inserir os campos para definir os valores dos coeficientes
            for f in funcoes:
                tk.Label(self.frm_tabela, text=f).grid(row=linha_atual, column=0)
                for col in range(len(variaveis)):
                    var = self.tk_vars['funcoes'][f][col]
                    celula = tk.Entry(self.frm_tabela, width=8, textvariable=var)
                    celula.grid(row=linha_atual, column=1+col)
                linha_atual += 1
            
            # define a tabela
            self.tabela = (variaveis, funcoes)
    
    def __init__(self, master):
        super().__init__(master)

        self.frm_table1 = tk.Frame(self)
        self.tabela1 = Tela.Tabela(self.frm_table1, self, 'Tabela atual')

        self.frm_table2 = tk.Frame(self)
        self.tabela2 = Tela.Tabela(self.frm_table2, self, 'Tabela resultante')

        self.frm_comandos = tk.Frame(self)
        self.inserir_frame_de_comandos(tabela=self.tabela1)
    
        self.frm_table1.grid(row=0, column=0, padx=10, pady=8)
        ttk.Separator(self, orient='horizontal').grid(row=1, column=0, sticky='nswe', padx=10)
        self.frm_comandos.grid(row=2, column=0, padx=10, pady=8)
        ttk.Separator(self, orient='horizontal').grid(row=3, column=0, sticky='nswe', padx=10)
        self.frm_table2.grid(row=4, column=0, padx=10, pady=8)

        self.btn_confirmar_calculo = tk.Button(self, 
                                               text='Trocar', 
                                               bg="#40a756",
                                               fg="#ffffff",
                                               padx=10, pady=5,
                                               command=self.transferir_tabela)
        self.btn_confirmar_calculo.grid(row=5, column=0, padx=10, pady=10)


    def inserir_frame_de_comandos(self, tabela: Tabela):
        variaveis, funcoes = tabela.tabela
        
        # coluna/variável pivô (entra na base)
        tk.Label(self.frm_comandos, 
                 text='Coluna pivô\n(que entra na base):', 
                 justify='right'
                 ).grid(row=0, column=0)
        ttk.Combobox(self.frm_comandos, 
                     values=variaveis,
                     state='readonly',
                     width=8,
                     textvariable=tabela.tk_vars['pivos']['coluna'],
                     ).grid(row=0, column=1)
        
        ttk.Separator(self.frm_comandos, 
                      orient='vertical'
                      ).grid(row=0, column=2, padx=10, pady=2, sticky='nswe')
        
        # linha pivô (sai da base)
        tk.Label(self.frm_comandos, 
                 text='Linha pivô\n(que sai da base):', 
                 justify='right'
                 ).grid(row=0, column=3)
        ttk.Combobox(self.frm_comandos, 
                     values=list(funcoes.keys()),
                     state='readonly',
                     width=8,
                     textvariable=tabela.tk_vars['pivos']['linha'],
                     ).grid(row=0, column=4)
        
        tk.Button(self.frm_comandos, 
                  text='Calcular nova tabela', 
                  bg="#161f99",
                  fg="#ffffff",
                  padx=10, pady=10,
                  command=lambda tab=tabela: self.on_click_calcular(tab),
                  ).grid(row=1, column=0, columnspan=5, pady=5)
    
    def on_click_calcular(self, tabela: Tabela):
        linha = tabela.tk_vars['pivos']['linha'].get()
        coluna = tabela.tk_vars['pivos']['coluna'].get()

        print(linha, coluna)

        antiga_tabela = self.tabela1.tabela
        resultante = calc.recalcular_linhas_tabela(antiga_tabela, linha, coluna)

        self.frm_table2.destroy()
        self.frm_table2 = tk.Frame(self)
        
        self.tabela2 = Tela.Tabela(self.frm_table2, self, 'Tabela resultante', tabela=resultante)
        self.frm_table2.grid(row=4, column=0, padx=10, pady=10)

    def transferir_tabela(self):
        self.frm_table1, self.frm_table2 = self.frm_table2, self.frm_table1
        self.tabela1, self.tabela2 = self.tabela2, self.tabela1

        self.frm_table1.grid_forget()
        self.frm_table2.grid_forget()

        self.frm_table1.grid(row=0, column=0, padx=10, pady=8)
        self.frm_table2.grid(row=4, column=0, padx=10, pady=8)

        # troca os títulos
        v1 = self.tabela1.titulo_tabela
        v2 = self.tabela2.titulo_tabela
        temp = v1.get()

        v1.set(v2.get())
        v2.set(temp)


if __name__ == '__main__':
    gui = tk.Tk()
    gui.geometry('800x450')
    gui.config(bg="#31313B")
    
    Tela(gui).pack()

    gui.mainloop()
