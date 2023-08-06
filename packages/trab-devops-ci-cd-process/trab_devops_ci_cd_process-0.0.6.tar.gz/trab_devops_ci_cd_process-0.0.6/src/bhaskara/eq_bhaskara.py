# Este codigo encontra as raízes de uma equação de 2° grau: ax^2 + bx + c = 0

import math
# import os


def raizes(a, b, c):

    # os.system('cls' if os.name == 'nt' else 'clear')
    print("agora estou no arquivo que calcula as raizes da eq 2° grau")
    print("\nA eq. 2ºgrau {}x2 + {}x + ({}) =0".format(a, b, c))
    delta = b**2 - 4*a*c

    if delta < 0:
        print("não possui raízes reais.")
        x1 = x2 = None
    elif delta == 0:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = x1
        print("possui apenas uma raiz real: ", x1)
    else:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        print("possui duas raízes reais: ", x1, " e ", x2)

    return (x1, x2)


# x1, x2 = raizes(a, b, c)

# fim = input("\nTecle enter para saír ou digite 'sair'\n")
