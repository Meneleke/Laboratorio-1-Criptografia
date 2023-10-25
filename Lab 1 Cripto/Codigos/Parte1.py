import sys

def cifrar_cesar(texto, corrimiento):
    resultado = ''
    for caracter in texto:
        if caracter.isalpha():
            # Determinar si el caracter es mayúscula o minúscula
            if caracter.isupper():
                inicio = ord('A')
            else:
                inicio = ord('a')
            
            # Aplicar el cifrado César
            caracter_cifrado = chr((ord(caracter) - inicio + corrimiento) % 26 + inicio)
            resultado += caracter_cifrado
        else:
            resultado += caracter  # Mantener caracteres que no son letras sin cambios
    
    return resultado

if len(sys.argv) != 3:
    print("Uso: python programa.py <texto_a_cifrar> <corrimiento>")
    sys.exit(1)

texto_a_cifrar = sys.argv[1]
corrimiento = int(sys.argv[2])

texto_cifrado = cifrar_cesar(texto_a_cifrar, corrimiento)
print("Texto cifrado:", texto_cifrado)
