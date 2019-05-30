class Estado:
	"""
	A classe estado possui os seguintes atributos:
	nome -> identificação do estado
	transicao -> dicionário contendo os símbolos do alfabeto e suas respectivas transições
	final -> indicativo de estado final
	inicial -> indicativo de estado inicial
	"""
	def __init__(self, nome):
		self.nome = nome
		self.transicao = {}
		self.final = False
		self.inicial = False

def le_arquivo(arquivo):
	"""
	O formato do arquivo deve respeitar a seguinte ordem:
	*Tipo do atômato
	*Quantidade de estados
	*Alfabeto
	*Estado inicial
	*Estado final
	*Transições

	As transições devem respeitar a seguinte configuração:
	Origem Símbolo Destino (para AFD)
	ex.: q0 0 q0

	Origem Símbolo Destinos (para AFN)
	ex.: q0 a q1 q2

	Caso determinado estado não processe um síbolo, não é
	necessário especificar a transição no arquivo. Caso o
	seja feito, deve seguir o exemplo.
	ex.: 'q0 b '
	"""
	with open(arquivo, 'r') as f:
		tipo = f.readline().split()
		qtd_estados = f.readline().split()
		alfabeto = f.readline().split()
		lista_estados = criar_estados(alfabeto[0], int(qtd_estados[0]))

        # definindo estado inicial
		linha = f.readline().split()
		for e in lista_estados:
			if e.nome == linha[0]:
				e.inicial = True

        # definindo estado final
		linha = f.readline().split()
		for e in lista_estados:
			if e.nome == linha[0]:
				e.final = True

        # recebendo todas as transições
        # transicao = f.readline().split()    #[0] = estado; [1] = simbolo; [2:] = destinos
		for transicao in f:
			lista = []
			t = transicao.split()
			for e in lista_estados:
				if e.nome == t[0]:
					for destino in t[2:]:
						lista.append(destino)
					e.transicao[t[1]] = lista.copy()
			lista.clear()
	f.close()

	sair = True
	while sair:
		palavra = input('Palavra a ser processada: ')
		print('A palavra', palavra, processa_palavra(lista_estados, palavra), 'pelo', tipo[0])
		i = input('Sair? (S/N) ')
		sair = (False) if i.upper() == 'S' else (True)

def criar_estados(alfabeto, qtd_estados):
    """
    Criação de um dicionário auxiliar com todos os símbolos do alfabeto.
    Inicialmente, todos os estados levam à um estado "vazio",
    independente de qual símbolo tenha sido processado.
    """
    estados = []
    for i in range(0, qtd_estados):
        nome = 'q' + str(i)
        estados.append(Estado(nome))

    return estados

def setTransicaoAFD(lista_estados, alfabeto):
    """
    Recebe o alfabeto e define, para cada estado, a transição do mesmo.
    Por se tratar de um AFD, cada símbolo processado só leva à um único
    estado
    """
    for estado in lista_estados:
        for simbolo in alfabeto:
            index = input(estado.nome + '--' + simbolo + '-->')
            estado.transicao[simbolo] = index

def setTransicaoAFN(lista_estados, alfabeto):
	"""
	Recebe o alfabeto e define, para cada estado, a transição do mesmo.
    Por se tratar de um AFN, cada símbolo pode levar a mais de um estado.
	A lista "conjunto" é responsável por armazenar os estados destinos e
	posteriormente adicionada ao dicionário de transição.
	"""
	conjunto = []
	for estado in lista_estados:
		for simbolo in alfabeto:
			conjunto.clear()
			while True:
				index = input(estado.nome + '--' + simbolo + '-->')
				conjunto.append(index)
				if input('Adicionar mais estados? (S/N) ').upper() == 'N':
					break
			estado.transicao[simbolo] = conjunto.copy()

def setInicial(estados):
	"""
	Lista inicialmente todos os estados existentes
	O usuário entra com a id ".nome" do estado desejado
	"""
	for e in estados:
		print('Estado:', e.nome)

	cont = len(estados)
	while(cont == len(estados)):
		cont = 0
		index = input('Qual estado inicial? ')
		for e in estados:
			if e.nome != index:
				cont += 1
		if cont == len(estados):
			print('Estado inexistente')

	for elem in estados:
		if elem.nome == index:
			elem.inicial = True

def setFinal(estados):
	"""
	AFDs/AFNs podem ter mais de um estado final
	Sendo assim, é requerido uma quantidade para definir o loop
	"""
	qtd = int(input('Quantidade de estados finais:'))

	if qtd > len(estados):
		print("Quantidade maior do que a de estados existentes")
		while qtd > len(estados):
			qtd = int(input('Quantidade de estados finais:'))


	for i in estados:
		print('Estado:',i.nome)
	while qtd != 0:
		nome = input('Estado final:')
		for e in estados:
			if e.nome == nome and e.final == True:
				print('O estado', e.nome, 'já é um estado final')
			elif e.nome == nome and e.final == False:
				e.final = True
				qtd -= 1

def getPalavra(alfabeto):
	"""
	Recebe a palavra a ser processada pelo Autômato,
	caso contenha símbolos diferente do alfabeto, a palavra não
	será aceita
	"""
	i = True
	while i:
		palavra = input('Digite a palavra a ser preocessada: ')
		for simb in palavra:
			if alfabeto.count(simb) == 0:
				print('A palavra contém símbolos não existentes no alfabeto')
			else:
				i = False
	return palavra

def processa_palavra(lista_estados, palavra):
	"""
	Procura o estado inicial na lista de estados e o adiciona à lista
	de estados ativos.
	Para cada símbolo da palavra a ser processada, enquanto existirem
	estados ativos, verificar se o símbolo leva à algum estado. Se levar,
	adicioná-lo à fila de processamento, que, posteriormente, será incorporada
	como estados ativos.
	Se algum estado da lista de estados ativos final possuir o atributo ".final"
	igual à "True", então a palavra é aceita pelo autômato.

	"""
	# Procurando o estado inicial
	for e in lista_estados:
		if e.inicial == True:
			e_atual = e

	e_ativos = []
	e_ativos.append(e_atual)
	fila_proc = []

	for simb in palavra:
		while len(e_ativos) > 0:
	    	# Verificando se o estado ativado por 'simb' em 'e_atual'
	    	# é diferente de vazio. Se sim, colocá-los como estados ativos
			e_atual = e_ativos.pop()
			if e_atual.transicao.get(simb) is not None:
				for nome_estado in e_atual.transicao.get(simb):
					# Adicionar o elemento q possui o 'nome'especificado
					for e in lista_estados:
						if e.nome == nome_estado:
							fila_proc.append(e)
		e_ativos = fila_proc.copy()
		fila_proc.clear()

	for estado in e_ativos:
		if estado.final == True:
			return 'é aceita'
	return 'não é aceita'

def processa_palavraAFD(lista_estados, palavra):
	"""
	Procura o estado inicial na lista de estados e o torna estado atual.
	E, para cada símbolo da palavra, verificar qual estado destino e torná-lo
	o atual.
	Se no final da palavra ".final" for "True", então a palavra é aceita pelo
	autômato.
	"""
	# Busca o estado inicial
	for e in lista_estados:
		if e.inicial == True:
			e_atual = e
	# Para cada símbolo da Palavra
	# verificar qual estado é ativado e torná-lo o estado atual
	for simb in palavra:
		nome_prox = e_atual.transicao[simb]
		for e in lista_estados:
			if e.nome == nome_prox:
				e_atual = e
	# Se o ultimo estado possuir o atributo '.final' = true, então
	# a palavra é aceita
	return 'é aceita' if e_atual.final is True else 'não é aceita'
