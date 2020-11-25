import imaplib
import re

def descomponer_texto(lista):
    message_id_list = list()
    char = 0
    aux = 0
    message_id = ""
    for x in lista:
        while char < len(x):
            if (aux == 1):
                message_id += x[char]
            if (x[char] == "<"):
                aux += 1
            if (x[char] == ">"):
                aux-=1
            char += 1

        message_id_list.append(message_id[0: len(message_id)-1])
        message_id = ""
        aux = 0
        char = 0

    return message_id_list

def importar_datos():
    file = open('datos.txt', 'r')
    datos = list();
    char = 0
    dato = ""
    for x in file:
        while char < len(x):
            if( x[char] == "," or char == len(x) - 1):
                datos.append(dato)
                dato = ""
            else:
                dato += x[char]
            char += 1

        dato = ""
        char = 0

    file.close()
    return datos

def validation_check(input_string, regex):
    match = re.match(regex, input_string)
    return bool(match)

def verificar_regex(lista, regex):
    for i in lista:
        if validation_check(i, regex) == False:
            print("-------------------------------------------------------------------------")
            print("¡ALERTA! Email no coincide con la expresión regular verificadora:")
            print("     Message-ID: {}".format(i))

EMAIL = 'joacovialj@gmail.com'
PASSWORD = 'deltoide789'
SERVER = 'imap.gmail.com'

mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)

mail.select('inbox')

print("-------------------------------------------------------------------------")
print('EMAILS RECIBIDOS DESDE INBOX')

datos = importar_datos()
dominio = datos[0]
regex = datos[1]
fecha = datos[2]

filtro = '(FROM ' + dominio + ') (SINCE '+ fecha + ')'

print("-------------------------------------------------------------------------")
print("SE FILTRA POR EL DOMINIO {} DESDE LA FECHA {}".format(dominio, fecha))
typ, data = mail.search(None,  filtro)
message_ids = list()
for num in data[0].split():
    typ, data = mail.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
    message_ids.append(data[0][1].decode('utf-8'))

message_ids = descomponer_texto(message_ids)

print("-------------------------------------------------------------------------")
print("Hay {} emails de la dirección {}.".format(len(message_ids),dominio))

verificar_regex(message_ids, regex)
