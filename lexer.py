# Buzdugan Mihaela

import copy

class DFA:
    currentState = None
    wordCurrent = []
    wordAcc = []
    
    def __init__(self, alphabet, initialState, listFinalState, delta, token):
        self.alphabet = alphabet
        self.initialState = initialState
        self.listFinalState =  listFinalState
        self.currentState = initialState
        self.delta = delta
        self.token = token
        return

    def nextConfig(self, value):
        if ((self.currentState, value) not in self.delta.keys()):
            self.currentState = None
            return

        self.currentState = self.delta[(self.currentState, value)]
        return

    def accept(self, word):
        self.currentState = self.initialState
        self.wordAcc = []
        self.wordCurrent = []

        for i in word:
            self.nextConfig(i)
            self.wordCurrent.append(i)

            if (self.currentState in self.listFinalState):
                self.wordAcc = copy.deepcopy(self.wordCurrent)

        return self.wordAcc


def runlexer(lexer, finput, foutput):

    # citesc cuvantul din finput
    fin = open(finput, "r")
    word = fin.read()

    # citesc lista de AFD-uri din fisierul lexer
    flex = open(lexer, "r")
    flex = flex.read()
    listAFDs = flex.split("\n\n")

    d = []
    for i in listAFDs:
            
        listLineAFD = i.split("\n")

        alphabet = list(listLineAFD[0])

        token = listLineAFD[1]

        initialState = int(listLineAFD[2])

        listFinalState = listLineAFD[-1].split(" ")
        mapListFS = map(int, listFinalState)
        listFinalState = list(mapListFS)

        # conditie pentru \n in alfabet
        if (alphabet[0] == '\\'):
            alphabet = [''.join(map(str, alphabet))]

            tranz = dict()
            for j in range(3, len(listLineAFD) - 1):
                tranzElem = listLineAFD[j].split(',')
                tranz[(int(tranzElem[0]), '\n')] = int(tranzElem[2])

        else:
            tranz = dict()
            for j in range(3, len(listLineAFD) - 1):
                tranzElem = listLineAFD[j].split(',')
                tranz[(int(tranzElem[0]), tranzElem[1][1])] = int(tranzElem[2])


        d.append(DFA(alphabet, initialState, listFinalState, tranz, token))

    fout = open(foutput, "w")

    wordAccMaxLen = 0
    index = 0

    while word is not "":
        for i in d:
            if len(i.accept(word)) > wordAccMaxLen:
                wordAccMaxLen = len(i.accept(word))
                index = i
        
        if (index.token == 'NEWLINE'):
            fout.write(str(index.token) + " " + '\\n')
        else:
            fout.write(str(index.token) + " " + ''.join(map(str, index.accept(word))))
            
        fout.write("\n")
    
        word = word[wordAccMaxLen:]
        wordAccMaxLen = 0
    
    fout.close()