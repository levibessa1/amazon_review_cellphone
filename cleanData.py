
import os,sys,difflib
import re
import sys
import string
import pickle

"""retornará o texto do assunto informado abaixo"""
def read_text(arquivo):    
    arq = open(arquivo,"r")
    texto = arq.read()
    arq.close()
    
    return texto

###REMOVE ALGARISMO ROMANO###########
if sys.version_info[0] >= 3:
    unicode = str

numeral_map = zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
)

def roman_to_int(n):
    n = unicode(n).upper()

    i = result = 0
    for integer, numeral in numeral_map:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
    return result

def roman_to_int_repl(match):
    return str(roman_to_int(match.group(0)))

###REMOVE:PONTUAÇÕES,PALAVRAS QUE CONTÉM NÚMEROS,HÍFEM, ASPAS, COLCHETE###########

def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower() 
    text = re.sub(r'\[.*?\]',' ', text) #apaga colchetes e o que esta dentro
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub("\d+", "", text)
    #text = re.sub('\w*\d', '', text)  
    text = re.sub(r'\–',' ',text,flags=re.IGNORECASE) 

    return text

def clean_text_round2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    #text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n',' ', text)
    return text

#todas as funções a cima sendo chamadas em uma única função.
# tipo 1 padrão para texto, outro tipo é endereço.
# opcao save = true , indica gerar arquivo limpo
def clean_text(texto,tipo=1,save=False):
    if tipo!= 1:
        r1 = re.findall(r"\.txt",texto)
        if len(r1) == 1:
            endereco = texto
            texto = read_text(texto)
            texto = clean_text(texto,1,False)
        else: 
            print("\n\t!!!!PARAMETROS DA FUNÇÃO [clean_text] PASSADOS INCORRETAMENTE !!!\n --- o parametro não é um arquivo");exit()
    else:
        limpando = unicode.upper(texto)
        regex = re.compile(r'\b(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b')
        limpando = regex.sub(roman_to_int_repl, limpando)
        limpando = clean_text_round1(limpando)
        texto_limpo = clean_text_round2(limpando)
        

    if save:
        if tipo != 1:
            with open("cleanned_"+endereco, "w") as file:
                file.write(texto)
        else:
            with open("cleanned_text", "w") as file:
                file.write(texto)



    return(texto_limpo)

