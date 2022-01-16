#Exercicio 4.1
impar = lambda x: x%2 != 0 

#Exercicio 4.2
positivo = lambda x: x>= 0 

#Exercicio 4.3
comparar_modulo = lambda x,y : x^2 > y^2 

#Exercicio 4.4
import math
cart2pol = lambda x,y : (math.sqrt(x^2 + y^2) , math.acos(x/1) if x > 0 else math.radians(90))

#Exercicio 4.5
ex5 = lambda f,g,h : lambda x,y,z: h(f(x,y),g(y,z)) 

#Exercicio 4.6
def quantificador_universal(lista, f):
    return map(f,lista)

#Exercicio 4.9
def ordem(lista, f):
    return min([lista[n + 1] for n in range(len(lista)-1) if not f(lista[n], lista[n+1])])

#Exercicio 4.10
def filtrar_ordem(lista, f):
    m = ordem(lista, f)
    return (m, [n for n in lista if n != m]) 

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    if lista == []:
        return []
    else:
        f = [lista[n + 1] for n in range(len(lista)-1) if not ordem(lista[n], lista[n+1])]
        if f == []:
            return lista
        else:
            m = min(f)
            lista =  [m] + [n for n in lista if n != m]
            return ordenar_seleccao(lista, ordem)
    return None
