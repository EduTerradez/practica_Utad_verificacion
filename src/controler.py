from random import randint
from board import Board
from pymongo import MongoClient

class Controler:
    def __init__(self):
        self.exit = False
        self.turn = randint(1,2)
        self.board = Board()
        self.isGameFinished = False
        self.player1Name = ''
        self.player2Name = ''
        self.client = MongoClient('localhost', 27017)
        self.dbs = self.client["baseDatosPalitos"]["Partidos"]
    def changeTurn(self):
        if self.turn == 1:
            self.turn = 2
        else: self.turn = 1
    def playMake(self):
        answer = []
        file1 = -1
        while file1 < 1 or file1 > 3:
            print "Introduce la fila a insertar(1, 2 o 3)"
            file1 = input()

        answer.append(file1)

        numSticks = -1
        while numSticks < 0 or numSticks > self.board.numSticks | numSticks > self.board.numSticksAvaliable(file1):
            print "Introduce un numero valido de palitos para eliminar"
            numSticks = input()

        answer.append(numSticks)
        return answer

    def gameFinished(self):
        winner = 0
        if self.board.numSticks == 1:
            self.isGameFinished = True
            if self.turn == 1:

                return 2
            else:
                return 1
        elif self.board.numSticks == 0:
            self.isGameFinished = True
            return self.turn

    def menu(self):
        print ''' Introduce el numero de la opcion que quieres elegir:
        1-Jugar!
        2-Consultar el historial.
        3-Salir. '''
        eleccion = input()
        if eleccion == 1:
            self.isGameFinished = False
            self.board = Board()
            #print 'Introduce el nombre del jugador 1:'
            self.player1Name = raw_input('Introduce el nombre del jugador 1:')
            #print 'Introduce el nombre del jugador 2:'
            self.player2Name = raw_input('Introduce el nombre del jugador 2:')
            self.play()
        elif eleccion == 2:
            print self.numPartidasJugadas()
            lista = self.showHistory()
            for x in lista:
                print x
        elif eleccion == 3:
            print 'Hasta Luego!!'
            self.exit = True

    def header(self):
        winner = 0
        print '''
            $$$$$$$$\ $$\                                           $$\ $$\   $$\                                $$$$$$\                                    $$ |
            \__$$  __|$$ |                                          $$ |\__|  $$ |                              $$  __$$\                                   $$ |
               $$ |   $$$$$$$\   $$$$$$\         $$$$$$\   $$$$$$\  $$ |$$\ $$$$$$\    $$$$$$\   $$$$$$$\       $$ /  \__| $$$$$$\  $$$$$$\$$$$\   $$$$$$\  $$ |
               $$ |   $$  __$$\ $$  __$$\       $$  __$$\  \____$$\ $$ |$$ |\_$$  _|  $$  __$$\ $$  _____|      $$ |$$$$\  \____$$\ $$  _$$  _$$\ $$  __$$\ $$ |
               $$ |   $$ |  $$ |$$$$$$$$ |      $$ /  $$ | $$$$$$$ |$$ |$$ |  $$ |    $$ /  $$ |\$$$$$$\        $$ |\_$$ | $$$$$$$ |$$ / $$ / $$ |$$$$$$$$ |\__|
               $$ |   $$ |  $$ |$$   ____|      $$ |  $$ |$$  __$$ |$$ |$$ |  $$ |$$\ $$ |  $$ | \____$$\       $$ |  $$ |$$  __$$ |$$ | $$ | $$ |$$   ____|
               $$ |   $$ |  $$ |\$$$$$$$\       $$$$$$$  |\$$$$$$$ |$$ |$$ |  \$$$$  |\$$$$$$  |$$$$$$$  |      \$$$$$$  |\$$$$$$$ |$$ | $$ | $$ |\$$$$$$$\ $$ |
               \__|   \__|  \__| \_______|      $$  ____/  \_______|\__|\__|   \____/  \______/ \_______/        \______/  \_______|\__| \__| \__| \_______|\__|
                                                $$ |
                                                $$ |
                                                \__|
            '''
        print"Juego para dos jugadores donde pierde quien elimine el ultimo palito, en cada turno puedes eliminar el numero que quieras de palitos de UNA fila."
        print"En cada jugada introduce el numero de fila y el numero de palitos. Mucha suerte!"
        raw_input("Press Enter to continue....")

    def play(self):
        self.board.paint()
        while(not self.isGameFinished):

            if self.turn == 1:
                print "Es el turno de " + self.player1Name
            elif self.turn == 2:
                print "Es el turno de " + self.player2Name
            answer = self.playMake()
            self.board.crossOut(answer[0], answer[1])
            self.board.paint()
            winner = self.gameFinished()
        self.changeTurn()
        self.insertResultadoPartido(winner)

    def insertResultadoPartido(self,winner):
        aux = {}
        if winner == 1:
            print "HA GANADO " + self.player1Name
            aux = {'Ganador': self.player1Name, 'Perdedor' : self.player2Name}
            return self.dbs.insert_one(aux).inserted_id
        elif winner == 2:
            print "HA GANADO " + self.player2Name
            aux = {'Ganador': self.player2Name, 'Perdedor' : self.player1Name}
            return self.dbs.insert_one(aux).inserted_id

    def numPartidasJugadas(self):
        num = 0
        aux = self.dbs.find()
        for partida in aux:
            num += 1
        return "Se han jugado " + str(num) + " partidas:"
    def showHistory(self):
        aux = {}
        aux =  self.dbs.find()
        print aux
        listaAuxiliar = []
        for partida in aux:
            listaAuxiliar.append( "Ganador: " + partida['Ganador'] + " Perdedor: " + partida['Perdedor'])
        return listaAuxiliar





