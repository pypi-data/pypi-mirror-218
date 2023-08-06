from unidecode import unidecode


def padronizar(text):
    return unidecode(text)


name = 'Carlão'
std_name = padronizar(name)
print(name, std_name)
