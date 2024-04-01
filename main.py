import time
import random

class Pessoa:
    def __init__(self, cpf, nome, telefone, senha):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.senha = senha

class Hashing:
    def __init__(self, tamanho):
        self._tamanho = tamanho
        self._slots = [None] * self._tamanho
        self._valores = [None] * self._tamanho

    def _funcao_hash(self, cpf):
        cpf_int = int(cpf)
        return cpf_int % self._tamanho

    def inserir(self, pessoa):
        cpf = pessoa.cpf
        indice = self._funcao_hash(cpf)
        if self._valores[indice] is None:
            self._slots[indice] = cpf
            self._valores[indice] = [pessoa]
        elif not any(p.cpf == cpf for p in self._valores[indice]):
            self._valores[indice].append(pessoa)

    def buscar(self, cpf):
        indice = self._funcao_hash(cpf)
        if self._valores[indice] is not None:
            for pessoa in self._valores[indice]:
                if pessoa.cpf == cpf:
                    return pessoa
        return None

class BuscaBinaria:
    def __init__(self):
        self.lista_pessoas = []

    def inserir(self, pessoa):
        cpf = pessoa.cpf
        esquerda, direita = 0, len(self.lista_pessoas)
        while esquerda < direita:
            meio = (esquerda + direita) // 2
            if self.lista_pessoas[meio].cpf < cpf:
                esquerda = meio + 1
            else:
                direita = meio
        if esquerda < len(self.lista_pessoas) and self.lista_pessoas[esquerda].cpf != cpf:
            self.lista_pessoas.insert(esquerda, pessoa)

    def buscar(self, cpf):
        esquerda, direita = 0, len(self.lista_pessoas)
        while esquerda < direita:
            meio = (esquerda + direita) // 2
            if self.lista_pessoas[meio].cpf < cpf:
                esquerda = meio + 1
            else:
                direita = meio
        if 0 <= esquerda < len(self.lista_pessoas) and self.lista_pessoas[esquerda].cpf == cpf:
            return self.lista_pessoas[esquerda]
        else:
            return None

class BuscaSequencial:
    def __init__(self):
        self.lista_pessoas = []

    def inserir(self, pessoa):
        if not any(pessoa.cpf == p.cpf for p in self.lista_pessoas):
            self.lista_pessoas.append(pessoa)

    def buscar(self, cpf):
        for pessoa in self.lista_pessoas:
            if pessoa.cpf == cpf:
                return pessoa
        return None

def gerar_cpf():
    return str(random.randint(10000000000, 99999999999))

def gerar_dados_pessoa():
    cpf = gerar_cpf()
    nome = "Pessoa" + str(random.randint(1, 100000))
    telefone = str(random.randint(100000000, 999999999))
    senha = "senha" + str(random.randint(1, 100000))
    return Pessoa(cpf, nome, telefone, senha)

def calcular_media(lista):
    soma = 0
    for elemento in lista:
        soma += elemento
    return soma / len(lista)

def tempo_formatado(segundos):
    if segundos < 60:
        return f"{segundos:.5f} segundos"
    elif segundos < 3600:
        minutos = segundos // 60
        segundos_restantes = segundos % 60
        return f"{int(minutos)} minutos e {segundos_restantes:.1f} segundos"
    else:
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segundos_restantes = segundos % 60
        return f"{int(horas)} horas, {int(minutos)} minutos e {segundos_restantes:.1f} segundos"

def testar_desempenho(estrutura, dados):
    tempos_insercao = []
    tempos_busca = []

    for i in range(3):
        inicio_insercao = time.time()
        for pessoa in dados:
            estrutura.inserir(pessoa)
        fim_insercao = time.time()
        tempo_insercao = fim_insercao - inicio_insercao
        tempos_insercao.append(tempo_insercao)

        inicio_busca = time.time()
        for j in range(100):
            cpf_busca = gerar_cpf()
            estrutura.buscar(cpf_busca)
        fim_busca = time.time()
        tempo_busca = fim_busca - inicio_busca
        tempos_busca.append(tempo_busca)

    tempo_medio_insercao = calcular_media(tempos_insercao)
    tempo_medio_busca = calcular_media(tempos_busca)

    return tempo_medio_insercao, tempo_medio_busca

tamanhos = [10000, 100000, 200000]

for tamanho in tamanhos:
    print(f"\nTeste para {tamanho} elementos:")

    dados = []
    for i in range(tamanho):
        pessoa = gerar_dados_pessoa()
        dados.append(pessoa)

    hashing = Hashing(tamanho)
    tempo_insercao_hashing, tempo_busca_hashing = testar_desempenho(hashing, dados)
    print(f"Hashing - Tempo Médio de Inserção: {tempo_formatado(tempo_insercao_hashing)}")
    print(f"Hashing - Tempo Médio de Busca: {tempo_formatado(tempo_busca_hashing)}")

    busca_binaria = BuscaBinaria()
    tempo_insercao_binaria, tempo_busca_binaria = testar_desempenho(busca_binaria, dados)
    print(f"Busca Binária - Tempo Médio de Inserção: {tempo_formatado(tempo_insercao_binaria)}")
    print(f"Busca Binária - Tempo Médio de Busca: {tempo_formatado(tempo_busca_binaria)}")

    busca_sequencial = BuscaSequencial()
    tempo_insercao_sequencial, tempo_busca_sequencial = testar_desempenho(busca_sequencial, dados)
    print(f"Busca Sequencial - Tempo Médio de Inserção: {tempo_formatado(tempo_insercao_sequencial)}")
    print(f"Busca Sequencial - Tempo Médio de Busca: {tempo_formatado(tempo_busca_sequencial)}")