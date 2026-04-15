import shutil
import pandas as pd
import numpy as np
import h5py

# MOSTRAR DATOS
serie = pd.Series([10,20,30,40,50], index=['a','b','c','d','e'])
print("Serie:\n", serie)

diccionario = {'a':1,'b':2,'c':3,'d':4}
serie_dict = pd.Series(diccionario)
print("Serie_dict:\n", serie_dict)


# CREACION DATAFRAMES

data = {
    'Ciudad': ['Madrid', 'Barcelona', 'Sevilla'],
    'Población': [3.3e6, 1.6e6, 0.7e6],
    'Temperatura': [15, 18, 20]
}
df = pd.DataFrame(data)
print("df:\n", df)


notas = pd.Series([5,9,10,4,3,8,4,6], index=["raul", "sergio", "pepe", "jose", "luis", "marcos", "maria", "jaqueline"])
print("notas:\n", notas)

nombres= {
    "nombre": ['jose', 'marcos', "elena"],
    "edad": [14,20,21]
}
df_nombres = pd.DataFrame(nombres)
print("df_nombres:\n", df_nombres)


# INDEXACION, SELECCION, FILTRADO
# loc e iloc
print("fila con el indice 0:\n", df.loc[0])
print("fila 0, columna 'ciudad' (loc):", df.loc[0, 'Ciudad'])

print("fila 1, columnas 0 y 1 (iloc):\n", df.iloc[0, 0:2])
print(df[0:1])


json = {
    "pais": ["Brasil", "Rusia", "India", "China", "Sudáfrica"],
    "capital": ["Brasilia", "Moscú", "Nueva Dehli", "Pekín", "Pretoria"],
    "area": [8.516, 17.10, 3.286, 9.597, 1.221],
    "población": [200.4, 143.5, 1252, 1357, 52.98]
        }
datos = pd.DataFrame(json)


datos.index= ["BR","RU","IN","CH","SA"]
print(datos)

# datos.reset_index(drop=True) para eliminar el index creado
# datos.set_index("pais") para poner una columna como index

filtro = df['Temperatura']>16
print(df[filtro])

print("usando query:\n",df.query('Temperatura>16'))

print(df.loc[2, ['Ciudad', "Población"]])
print(df.query('Población>1000000'))


# IMPORTACION DE FICHEROS
# nist_1b_202401_filtered_03.h5

# shutil.move("C:/Users/Alejandro/Downloads/nist_1b_202401_filtered_03.h5",
#             "C:/Users/Alejandro/Desktop/Python/AnalisisDatos")

def explore(name, obj):
    print(name)

# with h5py.File('nist_1b_202401_filtered_03.h5', 'r') as f:
#     f.visititems(explore)
#     f.close()

with h5py.File('nist_1b_202401_filtered_03.h5', 'r') as f:
    # Accedo al campo que quiero
    dset = f["Earth_Radiance_Filtered/Band A (Total)"]

    # variables para cada campo, tiempo, radiacion e interpolacion
    # creo un numpy array para cada campo y lo meto entero en la variable
    time = np.array(dset["DSCOVREpochTime"][:], dtype=np.float64)
    radiance = dset["EarthRadiance"][:]

    """
    Radiance == big-endian
    
    Por lo que en mi pc (little-endian) es incompatible 
    - byteswap() -> intercambia los bytes == AB CD -> CD AB
    - view() -> reinterpretas los datos con un nuevo formato
    - newbyteoreder() -> ajustado al sistema local (little-endian) 
    """
    radiance = radiance.byteswap().view(radiance.dtype.newbyteorder('='))
    interp = dset["isInterpolated"][:]

    # Creo un dataFrame de Pandas con los datos del dataset
    df_nasa = pd.DataFrame({
        "time": time,
        "radiance": radiance,
        "is_interpolated": interp
    })


print(df_nasa)