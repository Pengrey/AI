#Exercicio 1.1
def comprimento(lista):
	if lista == []:
		return 0
	return comprimento(lista[1:]) + 1

#Exercicio 1.2
def soma(lista):
	if lista == []:
		return 0
	return soma(lista[1:]) + lista[0]

#Exercicio 1.3
def existe(lista, elem):
	if lista == []:
		return False
	if lista[0] == elem:
		return True
	return existe(lista[1:], elem)

#Exercicio 1.4
def concat(l1, l2):
	if l2 == [] or l2 == None:
		return l1

	if l1 == [] or l1 == None:
		return l2

	l1.append(l2[0])	
	return concat(l1,l2[1:])

#Exercicio 1.5
def inverte(lista):
	if lista == []:
		return lista
	return inverte(lista[1:]) + [lista[0]]

#Exercicio 1.6
def capicua(lista):
	if lista == []:
		return True
	if lista[0] != lista[-1]:
		return False
	return capicua(lista[1:-1])
	

#Exercicio 1.7
def explode(lista):
	if lista == []:
		return []

	if lista[1:] == []:
		return lista[0]
	
	return explode([lista[0]]) + explode(lista[1:])

#Exercicio 1.8
def substitui(lista, original, novo):
	if lista == []:
		return None

	if lista[1:] == []:		
		if lista[0] == original:
			return [novo]
		else: 
			return  lista
	
	return substitui([lista[0]], original, novo) + substitui(lista[1:], original, novo)

#Exercicio 1.9
def junta_ordenado(lista1, lista2):
	if lista1 == []:
		return lista2

	if lista2 == []:
		return lista1

	if lista1[1:] == []:
		if lista1[0] < lista2[0]:
			return [lista1[0],lista2[0]]
		else:
			return [lista2[0],lista1[0]]

	return junta_ordenado([lista1[0]], [lista2[0]]) + junta_ordenado(lista1[1:], lista2[1:])

#Exercicio 2.1
def separar(lista):
	if lista[1:] == []:
		return [[lista[0][0]],[lista[0][1]]]
	
	l = separar(lista[1:])
	l1 = l[0]
	l2 = l[1]
	return ([lista[0][0]] + l1, [lista[0][1]] + l2) 

#Exercicio 2.2
def remove_e_conta(lista, elem):
	if lista == []:
		return None

	if lista[1:] == []:		
		if lista[0] == elem:
			return ([], 1)
		else: 
			return  lista
	
	l = remove_e_conta(lista[1:], elem)
	l1 = l[0]
	c = l[1]

	if lista[0] == elem:
		f1 = ([], 1)
	else: 
		f1 = ([lista[0]], 0)

	return (f1[0] + l1, f1[1] + c)

#Exercicio 3.1
def cabeca(lista):
	if lista == []:
		return None
	return lista [0]

#Exercicio 3.2
def cauda(lista):
	if lista == [] or lista[1:] == []:
		return None
	return lista [1:]

#Exercicio 3.3
def juntar(l1, l2):

	'''
	# Code without weird inputs
	if l1[1:] == []:
		return [(l1[0],l2[0])]
	return [(l1[0],l2[0])] + juntar(l1[1:], l2[1:])
	'''

	''' 
	# Version with different call counts
	if l1[1:]  == [] or l2[1:] == []:
		if l1[1:]  == [] and l2[1:] == []:
			return [(l1[0],l2[0])]
		else:
			return None
	else:
		j = juntar(l1[1:], l2[1:])
		if j == None:
			return j
		else:
			return [(l1[0],l2[0])] + j
	'''
	if comprimento(l1) != comprimento(l2):
		return None
	if l1 == [] or l2 == []:
		return []
	else:
		return [(l1[0], l2[0])] + juntar(l1[1:], l2[1:])

#Exercicio 3.4
def menor(lista):
	if lista == []:
		return None
	if lista[1:] == []:
		return lista[0]

	m = lista[0]
	n = menor(lista[1:])

	if n < m:
		return n
	else:
		return m

#Exercicio 3.6
def max_min(lista):
	if lista == []:
		return None
	if lista[1:] == []:
		return (lista[0], lista[0])
	
	n = lista[0]
	r = max_min(lista[1:])
	# Check max
	if r[1] < n:
		r[1] = n

	# Check min
	if r[0] > n:
		r[0] = n
		
	return r
