import numpy as np

# CREACION
array = np.ones((3,3))
print(array)

secuencia = np.arange(1,10).reshape(3,3)
print(secuencia)

print("Tipo dato:", secuencia.dtype)

# VECTORIZACION
a = np.array([[1,2,3]])
b = np.array([[4,5,6]])
print("suma:", a+b)


# BROADCASTIN
matriz = np.array([[1,2,3],[4,5,6],[7,8,9]])
escalar = 10
print("Matriz + escalar:\n" , matriz+escalar)

vector = np.array([1,0,-1])
print("matriz + vector:\n" , matriz+vector)


# SLICING
print("slicing:")
print("fila: ",matriz[0]) # primera fila
print("columna: ",matriz[:,0]) # primera columna
print("submatriz:\n",matriz[:2, :1]) # submatriz

# SLICING CONDICIONES
mask = matriz>5
print("valores mayores a 5: ", matriz[mask])

# reemplazar valores
matriz[matriz<4] =0
print("matriz modificada: ", matriz)

prueba = np.arange(1,17).reshape(4,4)
prueba[prueba>10] = -1

print("prueba: ", prueba)


# FUNCIONES MATEMATICAS
angulos = np.array([0, np.pi/2, np.pi])
print("seno de angulos: ", np.sin(angulos))


# PRUEBA FINAL
temperaturas = np.array([
[15, 18, 20], # Ciudad A
[22, 21, 19], # Ciudad B
[10, 12, 15] # Ciudad C
])

promedio = np.mean(temperaturas, axis=1)
promedio = np.round(promedio, 2)
print("promedio:", promedio)

ciudad = np.argmax(np.max(temperaturas, axis=1))
print("La ciudad con la maxima es la ciudad: ", ciudad+1)

print("temperaturas 2 dia: ", temperaturas[:3, 1:2])
temperaturas[temperaturas<15] =15
print("temperaturas:\n", temperaturas)


