import re

txt = "Meu texto começa com Inicio e terminar com um numero 59 no Fim"

x = re.search("^Meu.*Fim$", txt)

if x:
    print("Encontrou texto")
else:
    print("Não foi dessa vez!")

splitar = re.split(" ", txt)
print(splitar)

substituir = re.sub("o", "a", txt)
print(substituir)

procuraTudo = re.findall("m", txt)
print(len(procuraTudo))

procuraRange = re.findall("[a-c]", txt)
print(procuraRange)

procuraNumeros = re.findall("\d", txt)
print(procuraNumeros)

palavraIncompleta = re.findall("In..io", txt)
print(palavraIncompleta)

comecaCom = re.findall("^Meu", txt)
print(comecaCom)

terminaCom = re.findall("Fim$", txt)
print(terminaCom)

qualquerCoisa = re.search("In.*io", txt)
print(qualquerCoisa)

#txt = "hello planet"
umOuMais = re.findall("he..o", txt)
print(umOuMais)

umaPalavraOutra = re.findall("Inicio|Fim", txt)
print(umaPalavraOutra)

#grupoPalavras = re.findall(("Inicio", "Fim"), txt)
#print(grupoPalavras)

#txt = "Åland"
#buscaASCII = re.findall("\w", txt, re.ASCII)
buscaASCII = re.findall("\w", txt, re.A)
print(buscaASCII)

debugInformation = re.findall("Inicio", txt, re.DEBUG)
print(debugInformation)

txt = """Meu 
nome
é
Mizael"""
ignoraCaracter = re.findall("é.Mizael", txt, re.DOTALL)
print(ignoraCaracter)

txt = """eu
meu
seu
alceu
teu
eu
"""
comecoCadaLinha = re.findall("^eu", txt, re.MULTILINE)
print(comecoCadaLinha)


txt = "Comeco de um texto no pain no gain e _ain"
comecaString = re.findall("\AComeco", txt)
print(comecaString)

comecaTermina = re.findall(r"\bain", txt)
print(comecaTermina)

comecaTermina = re.findall(r"ain\b", txt)
print(comecaTermina)

comecaTermina = re.findall(r"\Bain", txt)
print(comecaTermina)

comecaTermina = re.findall(r"ain\B", txt)
print(comecaTermina)

qualquerLetra = re.findall(r"\wain", txt)
print(qualquerLetra)

naoContem = re.findall(r"\W", txt)
print(naoContem)

txt = "Texto com numeros 8853"

buscaNumeros = re.search("[0-9]", txt)
print(buscaNumeros)

numeroOcorrencia = re.split("o", txt, 3)
print(numeroOcorrencia)

txt = "Texto com um numero de letras o e fontes que comecam com c"
substituindo = re.sub("o", "1", txt, 2)
print(substituindo)