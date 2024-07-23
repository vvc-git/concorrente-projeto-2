from threading import Thread
from time import sleep

import init

class Funcionario(Thread):
    '''
        Nadadores devem ser criados periodicamente e realizar as seguintes ações:
        - Limpar os vestiários masculino e feminino.
        - Descansar.

        A sua responsabilidade é implementar os métodos com o comportamento do
        funcionário, respeitando as restrições impostas no enunciado do trabalho.
     
    '''

    # Construtor da classe Funcionario
    def __init__(self, id):
        # Atributos default
        self.id     = id
        self.genero = 'M'
        self.trabalhando = False

        super().__init__(name=("Funcionario " + str(id)))

    # Imprime mensagem de log
    def log(self, mensagem):
        espacos = (16 - len(self.name)) * ' '
        #print('['+ self.name + '] ' + espacos + mensagem + '\n', end='')
        print('\033[1;97m['+ self.name + ']\033[m ' + espacos + mensagem + '\n', end='')


    # Comportamento do Funcionario
    def run(self):
        '''
            NÃO ALTERE A ORDEM DAS CHAMADAS ABAIXO.

            Você deve implementar os comportamentos dentro dos métodos da classe.
            Observação: Comente no código qual o objetivo de uma dada operação, 
            ou conjunto de operações, para facilitar a correção do trabalho.
        '''
        self.log("Iniciando o expediente")
        self.trabalhando = True     

        while self.trabalhando == True :
            self.limpar_vest_masculino()
            self.limpar_vest_feminino()
            self.descansar()

        self.log("Terminando o expediente")

    # Funcionário limpa o vestiário masculino. O vestiário não precisa estar vazio.
    # Porem os boxes precisam estar vazios
    def limpar_vest_masculino(self):
        self.log("Iniciando limpeza do vestiário masculino")
        sleep(init.tempo_limpeza_vestiario * init.unidade_de_tempo)
        '''
            IMPLEMENTE AQUI:
            Aguarde que todas as duchas sejam liberadas.
        '''
        with init.mutex_ducha:
            if init.duchas_masc_ocupadas != 0:
                init.cond_ducha_func.wait() # aguarda ducha livre para seu acesso
            #self.log('iniciando a limpeza da ducha')
            init.ducha_sendo_limpada = 1
            self.log('iniciando a limpeza da ducha')
            
        sleep(init.quant_duchas_por_vestiario * init.tempo_limpeza_ducha * init.unidade_de_tempo)
        self.log("Concluída a limpeza do vestiário masculino")
        '''
            IMPLEMENTE AQUI:
            Libere as duchas para uso.
        '''
        with init.mutex_ducha:
            init.ducha_sendo_limpada = 0
            init.cond_ducha_masc.notify_all()

    # Funcionário limpa o vestiário feminino. ATENÇÃO: o vestiário precisa estar vazio!!!
    def limpar_vest_feminino(self):
        '''
            IMPLEMENTE AQUI:
            Aguarde que o vestiário feminino esteja vazio para entrar.
        '''
        with init.mutex_vest_fem:
            if len(init.vestiario_fem) != 0:
                init.cond_vest_func.wait()
            init.vest_fem_sendo_limpado = 1

        self.log("Iniciando limpeza do vestiário feminino")
        sleep(init.tempo_limpeza_vestiario * init.unidade_de_tempo)
        sleep(init.quant_duchas_por_vestiario * init.tempo_limpeza_ducha * init.unidade_de_tempo)
        self.log("Concluída a limpeza do vestiário feminino")
        '''
            IMPLEMENTE AQUI:
            Libere o acesso ao vestiário feminino.
        '''
        with init.mutex_vest_fem:
            init.vest_fem_sendo_limpado = 0
            init.cond_vest_fem.notify_all()

    # Funcionário descansa durante um tempo
    def descansar(self):
        self.log("Hora do intervalo de descanso.")
        sleep(init.tempo_descanso * init.unidade_de_tempo)
        self.log("Fim do intervalo de descanso.")

