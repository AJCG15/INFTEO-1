# 1 extencion
#===========================================
print("----Resultado de verificacion----")
mi_conjunto = {1, 2, 3, 4}

# Conjunto de referencia
referencia = {1, 2, 3, 4}

if mi_conjunto == referencia:
    print("Verificación exitosa")
else:
    print("Verificación fallida")
print()    
    
# 2 compresion
#============================================
print("----Resultado de compresion----")
numeros_pares = {n for n in range(1, 21) if n % 2 == 0}

print("Resultado de la creación del conjunto")
print("Los números pares generados son:", numeros_pares)

def verificar_pares(cj):
    conjunto_esperado = set(range(2, 21, 2))
    
    if cj == conjunto_esperado:
        print(" el conjunto es correcto")
    else:
        print("el conjunto no coincide")


verificar_pares(numeros_pares)
print()

# 3 conjunto
#=======================================================
print("----Resultado de conjunto----")
mi_conjunto = {3, 7, 9, 12, 5}
print("el conjunto es ",mi_conjunto," y tiene ",len(mi_conjunto),"elementos")
# Cardinalidad
if len(mi_conjunto) == 6:
    print("correcto")
else:
    print("error") 
print()

# 4 conjunto finito
#=========================================================
print("---- Resultado de conjunto infinito-----")
lista_numeros = list(range(1, 101))

# Mostrar resultado
print(" Resultado de la lista ")
print("Números generados:", lista_numeros)


def comprobar_tamaño(lst):
    return len(lst) == 100


if comprobar_tamaño(lista_numeros):
    print(" La lista tiene 100 elementos")
else:
    print(" La lista no tiene el tamaño esperado")
print()

# 5 union
#========================================================
print("----Resultado de la union----")
conjunto_x = set(range(10, 41))
conjunto_y = set(range(30, 61))


union_xy = conjunto_x | conjunto_y


print("Conjunto X:", conjunto_x)
print("Conjunto Y:", conjunto_y)
print("Unión:", union_xy)


if union_xy == conjunto_x.union(conjunto_y):# para verificar si esta procesando los datos
    print("correcto")
else:
    print("error")
    
print()

# 6 interseccion
#========================================================

conjunto_x = set(range(10, 41))   # del 10 al 40
conjunto_y = set(range(30, 61))   # del 30 al 60

print("----Resultado de la Intersección----")
print("Conjunto X:", conjunto_x)
print("Conjunto Y:", conjunto_y)

interseccion_xy = conjunto_x & conjunto_y
print("Intersección de X & Y:", interseccion_xy)

if interseccion_xy == conjunto_x.intersection(conjunto_y):
    print("correcto")
else:
    print("error")
print()

#7 Diferencia
#==============================================================
conjunto_x = set(range(10, 41))   
conjunto_y = set(range(30, 61))   

print("----Resultado de la Diferencia----")
print("Conjunto X:", conjunto_x)
print("Conjunto Y:", conjunto_y)

diferencia_xy = conjunto_x - conjunto_y
print("Diferencia X - Y:", diferencia_xy)

if diferencia_xy == conjunto_x.difference(conjunto_y):
    print("correcto")
else:
    print("error")
print()

# 8 Diferencia simetrica
#================================================================
conjunto_x = set(range(10, 41))   
conjunto_y = set(range(30, 61))   

print("----Resultado de la Diferencia Simétrica----")
print("Conjunto X:", conjunto_x)
print("Conjunto Y:", conjunto_y)

diferencia_sim_xy = conjunto_x ^ conjunto_y
print("Diferencia Simétrica X ^ Y:", diferencia_sim_xy)

if diferencia_sim_xy == conjunto_x.symmetric_difference(conjunto_y):
    print("Correcto")
else:
    print("Error")
print()

# 9 complemento
#====================================================================

Univer = set(range(50, 151))    
Conjun= set(range(80, 121))    

print("-----Resultado de Complemento------")
print("Universo:", Univer)
print("Conjunto C:", Conjun)


Comp = Univer - Conjun
print("Complemento de C en el Universo:", Comp)


union_total = Conjun | Comp
interseccion = Conjun & Comp

if union_total == Univer and len(interseccion) == 0:
    print("Correcto")
else:
    print("Error")
print()

# 10 producto cartesiano
#===============================================================
X = set(range(2, 7))   # Conjunto X: 2 al 6
Y = set(range(12, 18)) # Conjunto Y: 12 al 17

print("-----Resultado de Producto Cartesiano----")
print("Conjunto X:", X)
print("Conjunto Y:", Y)

prod_cart = {(x, y) for x in X for y in Y}
print("Producto cartesiano X × Y:", prod_cart)

if len(prod_cart) == len(X) * len(Y):
    print("Correcto")
else:
    print("Error")
print()

# 11 Reflesiva
#==============================================================
X = set(range(2, 7))  

print("----Resultado de Relación Reflexiva----")
print("Conjunto X:", X)

rel_ref = {(x, x) for x in X}# Generar relación reflexiva
print("Relación reflexiva generada:", rel_ref)

def verificar_reflexividad(conj, relacion):
    for elem in conj:
        if (elem, elem) not in relacion:
            print("Error")
            return False
    print("Correcto")
    return True
verificar_reflexividad(X, rel_ref)
print()

# 12 simetrica
#===============================================================
R = {(2, 3), (3, 2), (4, 4), (5, 6), (6, 5)}

print("----Resultado de Relación Simétrica----")
print("Relación definida:", R)

def verificar_sim(R):
    for (x, y) in R:
        if (y, x) not in R:
            print("Error")
            return False
    print("Correcto")
    return True
verificar_sim(R)
print()

# 13 antisimetrica
#===========================================================
# Relación definida
S = {(2, 3), (3, 3), (4, 5)}

print("----Resultado de Relación Antisimétrica----")
print("Relación definida:", S)

def verificar_anti(a):
    for (x, y) in R:
        if (y, x) in R and x != y:
            print("correcto")
            return False
    print("error")
    return True
verificar_anti(S)
print()

# 14 transitiva
#==========================================================
T = {(2, 3), (3, 4), (2, 4)}

print("----Resultado de Relación Transitiva----")
print("Relación definida:", T)

def verificar_trans(T):
    for (x, y) in T:
        for (y2, z) in T:
            if y == y2 and (x, z) not in T:
                print("Error")
                return False
    print("Correcto")
    return True
verificar_trans(T)
print()

# 15 Relacion de Equivalencia
#===============================================================
X = set(range(2, 7))  

print("----Resultado de Relación de Equivalencia----")

# Relación de equivalencia
R_eq = {(x, x) for x in X} | {(x, y) for x in X for y in X if x % 2 == y % 2}

def verificar_equiv(X, R):
# Verificar reflexividad: cada elemento debe relacionarse consigo mismo
    for x in X:
        if (x, x) not in R:
            print(f"Error: el elemento {x} no es reflexivo")
            return False

# Verificar simetría: si (x, y) existe, (y, x) también debe existir
    for (x, y) in R:
        if (y, x) not in R:
            print(f"Error: la pareja ({x}, {y}) no tiene simétrica ({y}, {x})")
            return False

# Verificar transitividad: si (x, y) y (y, z) existen, (x, z) también debe existir
    for (x, y) in R:
        for (y2, z) in R:
            if y == y2 and (x, z) not in R:
                print(f"Error: la transitividad falla para ({x}, {y}) y ({y2}, {z})")
                return False

    print("Correcto: la relación es de equivalencia")
    return True
verificar_equiv(X, R_eq)
print()

# 16 Relaciones de Orden
#=========================================================================
X = set(range(2, 7))  
print("----Resultado de Relación de Orden----")
print("Conjunto generado:", X)

# Relación de orden: pares (x, y) donde x <= y
R_ord = {(x, y) for x in X for y in X if x <= y}


def verificar_orden(X, R):
#cada elemento debe relacionarse consigo mismo    
    for x in X:
        if (x, x) not in R:
            print(f"Error: el elemento {x} no cumple reflexividad")
            return False
# si (x, y) y (y, x) existen, entonces x debe ser igual a y
    for (x, y) in R:
        if (y, x) in R and x != y:
            print(f"Error: la antisimetría falla para ({x}, {y})")
            return False
# si (x, y) y (y, x) existen, entonces x debe ser igual a y
    for (x, y) in R:
        for (y2, z) in R:
            if y == y2 and (x, z) not in R:
                print(f"Error: la transitividad falla para ({x}, {y}) y ({y2}, {z})")
                return False

    print("Correcto: la relación es de orden")
    return True
verificar_orden(X, R_ord)
print()

# 17 inyectiva
#==================================================================
print("----Resultado de función inyectiva-----")

def f(x):
    return 3 * x  

D = range(1, 6)  
Y = [f(x) for x in D]

def es_inyectiva(a):
# Una función es inyectiva si todos los valores son únicos
    return len(a) == len(set(a))


if es_inyectiva(Y):
    print("Correcto")
else:
    print("Error")
print()

# 18 sobreyectiva
#====================================================
print("-----Resultado de función sobreyectiva-----")

def f(x):
    return x % 4  # Cambié a módulo 4 para variar

# Dominio y codominio
D = range(12)        
C = {0, 1, 2, 3}    

Y = [f(x) for x in D]

def es_sobreyectiva(C, Y):
    # Una función es sobreyectiva si todo elemento del codominio aparece en la imagen
    return C.issubset(set(Y))

if es_sobreyectiva(C, Y):
    print("Correcto")
else:
    print("Error")
print()

# 19 Biyectiva
#===========================================================
print("----Resultado de función biyectiva----")

def f(x):
    return x + 2  

# Dominio y codominio
D = range(0, 10)        
C = set(range(2, 12))   

Y = [f(x) for x in D]

def es_biyectiva(C, Y):
# Una función es biyectiva si es inyectiva y sobreyectiva
    return C.issubset(set(Y)) and len(set(Y)) == len(Y)

if es_biyectiva(C, Y):
    print("Correcto")
else:
    print("Error")
print()

# 20 Reflexiva
#================================================================
X = set(range(2, 7)) 
# Relacion
R = {(2, 3), (3, 4), (4, 5), (5, 6)}

print("=== Resultado de Clausura Reflexiva ===")
print("Conjunto X:", X)
print("Relación inicial R:", R)

#reflexiva: agregar (x, x) para todo x en X
R_ref = R | {(x, x) for x in X}

def es_reflexiva(X, R):
    # Una relación es reflexiva si (x, x) está en R para todo x en X
    return all((x, x) in R for x in X)

if es_reflexiva(X, R_ref):
    print("Correcto")
else:
    print("Error")
print()

# 21 simetrica
#=========================================================================
X = set(range(2, 7))  
R = {(2, 3), (4, 5)}

print("----Resultado de Clausura Simétrica----")
print("Conjunto X:", X)
print("Relación inicial R:", R)

def clausura_sim(R):
    # Agrega todos los pares invertidos (b, a)
    return R | {(b, a) for (a, b) in R}

def es_sim(R):
    for (x, y) in R:
        if (y, x) not in R:
            print("Error")
            return False
    print("Correcto")
    return True
R_sim = clausura_sim(R)
es_sim(R_sim)
print()

#22 transitivo
#======================================================================
X = set(range(2, 7))  
R = {(2, 3), (3, 4)}

print("----Resultado de Clausura Transitiva----")
print("Conjunto X:", X)
print("Relación inicial R:", R)

def clausura_trans(R):
    nueva = set(R)  
    while True:
        agregado = False
        pares_actuales = list(nueva)
        # Revisar todos los pares para agregar los nuevos que cumplan transitividad
        for (x, y) in pares_actuales:
            for (y2, z) in pares_actuales:
                if y == y2 and (x, z) not in nueva:
                    nueva.add((x, z))
                    agregado = True
        if not agregado: 
            break
    return nueva

# Función para verificar transitividad
def es_trans(R):
    for (x, y) in R:
        for (y2, z) in R:
            if y == y2 and (x, z) not in R:
                print("Error")
                return False
    print("Correcto")
    return True
R_trans = clausura_trans(R)
es_trans(R_trans)
print()

# 23 equivalencia
#=====================================================================
print("----Resultado de Clausura Transitiva----")
def reflex(R, X):
    # Recorremos cada elemento del conjunto
    for x in X:
        if (x, x) not in R:
            return False
    return True

def simet(R):
    # Recorremos cada par de la relación
    for (x, y) in R:
        if (y, x) not in R:
            return False
    return True

def trans(R):
    # Recorremos cada par y buscamos pares que formen transitividad
    for (x, y) in R:
        for (a, b) in R:
            if y == a and (x, b) not in R:
                return False
    return True

def equiva(R, X):
    # Verificamos las tres propiedades
    if reflex(R, X) and simet(R) and trans(R):
        return True
    else:
        return False

X = {1, 2, 3}
R = {(1,1), (2,2), (3,3), (1,2), (2,1), (2,3), (3,2)}

if equiva(R, X):
    print("Correcto: la relación es de equivalencia")
else:
    print("Error: la relación no es de equivalencia")




