from threading import Thread
from time import sleep
from random import randint
#from typing_extensions import ParamSpecArgs

import init

class Nadador(Thread):
    '''
        Nadadores realizam as seguintes ações:
        - Ir ao vestiário 
        - Colocar a roupa de natação
        - Encontrar um armário para guardar os seus pertences
        - Tomar uma ducha
        - As crianças que forem aprendizes precisam pegar uma prancha para nadar
        - Nadar (raia exclusiva no caso dos adultos, ou compartilhada por 2 crianças) 
        - As crianças que forem aprendizes devem devolver a prancha
        - Retornar ao vestiário
        - Tomar outra ducha
        - Retirar seus pertences do armário e liberá-lo
        - Trocar de roupa
        - Ir embora

        Cada uma dessas ações corresponde a um método do Nadador. A sua responsabilidade 
        é desenvolver os comportamentos dentro dos métodos do nadador de modo que ele se
        comporte conforme a especificação contida no Moodle.

        Esses métodos são chamados no método run() do Nadador.
      
    '''
    # Construtor do nadador
    # Argumentos indicam o gênero e se é criança e aprendiz
    def __init__(self, id, genero, crianca = False, aprendiz = False):
        self.id     = id
        self.genero = genero
        self.crianca = crianca
        self.aprendiz = aprendiz

        if self.crianca == True:
            if self.aprendiz == False:
                if self.genero == 'M':
                    super().__init__(name=("Menino " + str(id)))
                else:
                    super().__init__(name=("Menina " + str(id)))
            elif self.genero == 'M':
                super().__init__(name=("O aprendiz " + str(id)))
            else:
                super().__init__(name=("A aprendiz " + str(id)))
        elif self.genero == 'M':
            super().__init__(name=("Nadador " + str(id)))
        else:
            super().__init__(name=("Nadadora " + str(id)))

    # Função que imprime mensagens de log
    def log(self, mensagem):
        espacos = (20 - len(self.name) - 3) * ' '
        #print('['+ self.name + '] ' + espacos + mensagem + '\n', end='')
        if  self.genero == 'M':
            print('\033[1;94m['+ self.name + ']\033[m ' + espacos + mensagem + '\n', end='')
        else:
            print('\033[1;31m['+ self.name + ']\033[m ' + espacos + mensagem + '\n', end='')

    # Representação do nadador nas mensagens de log
    def __repr__(self):
        return self.name

    # Comportamento do nadador
    def run(self):
        '''
            NÃO ALTERE A ORDEM DAS CHAMADAS ABAIXO.

            Você deve implementar os comportamentos dentro dos métodos invocados. 
            Observação: Comente no código qual o objetivo de uma dada operação, 
            ou conjunto de operações, para facilitar a correção do trabalho.
        '''

        self.log("Entrando na academia de natação.")

        self.entrar_vestiario()
        self.trocar_roupa()
        self.pegar_armario()
        self.tomar_ducha()
        
        self.sair_vestiario()
        if self.aprendiz:
            self.pegar_prancha()
        
        self.pegar_raia()
        self.nadar()
        self.liberar_raia()
        
        if self.aprendiz:
            self.devolver_prancha()        
        self.entrar_vestiario()
        self.tomar_ducha()
        self.liberar_armario()
        self.trocar_roupa()
        self.sair_vestiario()

        self.log("Saindo da academia de natação.")

    # Nadador entra no vestiário correspondente ao seu gênero
    def entrar_vestiario(self):
        '''
            IMPLEMENTE AQUI:
            O nadador deve entrar no vestiário correspondente ao seu gênero.

            OBJETIVO: foram criadas duas listas no init para representar o vestiario de cada genero. Ao entrar no vestiario o id do nadador 
            é adicionado na lista do seu genêro
        '''
        if self.genero == 'M':
            init.vestiario_mas.append(self.id)
        else:
            with init.mutex_vest_fem:
                # Impedir que a nadadora entre enquanto o funcionário estiver limpando
                if init.vest_fem_sendo_limpado == 1:
                    # Evita busy-wait porque a thread fica suspensa esperando o notify
                    init.cond_vest_fem.wait()
                init.vestiario_fem.append(self.id)
        
        self.log("Entrou no vestiário")

    # Nadador sai do vestiário         
    def sair_vestiario(self):
        '''
            IMPLEMENTE AQUI:
            O nadador deve sair do vestiário.
        '''
        # Apos a saida do vestiario o id que foi colocado na lista e` retirado.
        if self.genero == 'M':
            init.vestiario_mas.remove(self.id)
        else:
            init.vestiario_fem.remove(self.id)
            with init.mutex_vest_fem:
                if len(init.vestiario_fem) == 0:
                    # avisa o funcionário que estiver suspenso que ele pode começar a limpar
                    init.cond_vest_func.notify()

        self.log("Saiu do vestiário")

    # Nadador troca de roupa 
    def trocar_roupa(self):
        self.log("Trocando de roupa...")
        sleep(randint(init.tempo_troca_min, init.tempo_troca_max) * init.unidade_de_tempo)

    # Nadador encontra um armário e guarda seus pertences
    def pegar_armario(self):
        '''
            IMPLEMENTE AQUI:
            O nadador deve encontrar um armário para guardar os seus pertences.
            O armário precisa estar no vestiário correspondente ao seu gênero.
        '''
        # dependendo do genero do nadador ele decrementa o semaforo destinado impedindo que outros nadadores
        # possam ocupar o mesmo armario que ele.
        if self.genero == 'M':
            init.sem_arm_mas.acquire()
        else:
            init.sem_arm_fem.acquire()
        self.log("Pegou um armário")

    # Nadador libera o armário
    def liberar_armario(self):
        '''
            IMPLEMENTE AQUI:
            O nadador deve liberar o armário no qual guardou os seus pertences.
        '''
        # o nadador que termina de usar o armario incrementa o semaforo destinado possibilitando
        # que outros nadadores possam ocupar.
        if self.genero == 'M':
            init.sem_arm_mas.release()
        else:
            init.sem_arm_fem.release()
            
        self.log("Liberou um armário")

    # Nadador toma uma ducha antes ou depois de nadar
    def tomar_ducha(self):
        '''
            IMPLEMENTE AQUI:
            Encontrar um box livre para tomar ducha.
        ''' 
        # dependendo do genero do nadador ele decrementa o semaforo destinado impedindo que outros nadadores
        # possam ocupar a mesma ducha que ele.
        if self.genero == 'M':
            with init.mutex_ducha:
                if init.ducha_sendo_limpada == 1:
                    init.cond_ducha_masc.wait() # aguarda a liberacao da ducha
            init.sem_ducha_mas.acquire()
            init.duchas_masc_ocupadas += 1
        else:
            init.sem_ducha_fem.acquire()

        self.log("Tomando uma ducha...")
        sleep(randint(init.tempo_ducha_min, init.tempo_ducha_max) * init.unidade_de_tempo)
        self.log("Terminou de tomar uma ducha.")

        '''
            IMPLEMENTE AQUI:
            Liberar a ducha.
        '''
        # o nadador que termina de usar a ducha incrementa o semaforo destinado possibilitando
        # que outros nadadores possam ocupar.
        if self.genero == 'M':
            init.sem_ducha_mas.release()
            init.duchas_masc_ocupadas -= 1
            with init.mutex_ducha:
                if init.duchas_masc_ocupadas == 0:
                    # Quando não tiver nenhum nadador na ducha, 
                    # Avisa o funcionário que ele pode começar a limpar
                    init.cond_ducha_func.notify()

        else:
            init.sem_ducha_fem.release()

    # Nadador aprendiz deve pegar uma prancha antes de entrar na piscina
    def pegar_prancha(self):
        '''
            IMPLEMENTE AQUI:
            O nadador aprendiz deve pegar uma prancha para nadar.
        '''

        init.sem_prancha.acquire()

        self.log("Pegou uma prancha para nadar.")

    # Nadador aprendiz devolve a prancha que estava usando para nadar
    def devolver_prancha(self):
        self.log("Devolvendo uma prancha.")
        '''
            IMPLEMENTE AQUI:
            O nadador aprendiz deve devolver a prancha.
        '''
        init.sem_prancha.release()
        
    # Nadador tenta encontrar uma raia para nadar    
    def pegar_raia(self):
        '''
            IMPLEMENTE AQUI:
            O nadador deve encontrar uma raia para nadar. Adultos precisam
            de uma raia exclusiva, e 2 crianças podem compartilhar uma raia.
        '''
        
        # Crianças valem 0.5 e Adultos valem 1.

        # Cria uma fila de pessoas 
        init.escolha_raia.acquire()
        if self.crianca == True:
            if init.raias_ocupadas > 7.5: 
                # Mostrar a seguinte mensagem quando a piscina estiver lotada:
                self.log("Piscina lotada. Aguardando raia ser liberada...")
            # Controla o acesso das raias
            init.sem_raia.acquire()
            init.piscina.append(self.id)
            init.raias_ocupadas += 0.5
        else:
            if init.raias_ocupadas > 7:
                # Mostrar a seguinte mensagem quando a piscina estiver lotada:
                self.log("Piscina lotada. Aguardando raia ser liberada...")
            init.sem_raia.acquire()
            init.sem_raia.acquire()
            init.piscina.append(self.id)
            init.raias_ocupadas += 1
        init.escolha_raia.release()
           
        self.log("Conseguiu uma raia para nadar.")
        self.log("Na piscina: " + str(init.piscina))

    # Nadador libera a raia na qual estava nadando
    def liberar_raia(self):
        self.log("Liberando uma raia.")
        
        '''
            IMPLEMENTE AQUI:
            O nadador deve liberar a raia.
        '''
        #init.escolha_raia.acquire()
        if self.crianca == True:
            init.sem_raia.release()
            init.piscina.remove(self.id)
            init.raias_ocupadas -= 0.5
        else:
            init.sem_raia.release()
            init.sem_raia.release()
            init.piscina.remove(self.id)
            init.raias_ocupadas -= 1
        #init.escolha_raia.release()
        self.log("Na piscina: " + str(init.piscina))

    # Simula o tempo que o nadador fica na piscina nadando
    def nadar(self):
        self.log("Começou a nadar.")
        sleep(randint(init.tempo_nadando_min, init.tempo_nadando_max) * init.unidade_de_tempo)
        self.log("Terminou de nadar.")