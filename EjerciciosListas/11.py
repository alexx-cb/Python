# Realiza un programa que genere 10 números enteros aleatorios entre 0 y 200 ambos incluidos y que
# los almacene en una lista. A continuación, el programa debe mostrar el contenido de esa lista junto al
# índice (0 – 9). Seguidamente el programa debe colocar de forma alterna y en orden los menores o
# iguales de 100 y los mayores de 100: primero menor, luego mayor, luego menor, luego mayor…
# Cuando se acaben los menores o los mayores, se completará con los números que queden.
import random


aleatorios = [random.randint(0, 200) for _ in range(10)]


indices = [str(i) for i in range(len(aleatorios))]
valores = [str(v) for v in aleatorios]


anchos = [max(len(ix), len(val)) + 2 for ix, val in zip(indices, valores)]


cols_indices = " | ".join(f"{ix:^{w}}" for ix, w in zip(indices, anchos))
cols_valores = " | ".join(f"{val:^{w}}" for val, w in zip(valores, anchos))

cabecera = f"Índice | {cols_indices} |"
fila_valor = f"Valor  | {cols_valores} |"
separador = "-" * max(len(cabecera), len(fila_valor))

print(separador)
print(cabecera)
print(separador)
print(fila_valor)
print(separador)


aleatorios.sort()



menores = aleatorios[:5]
mayores = aleatorios[5:][::-1]


lista_intercalada = [item for par in zip(mayores, menores) for item in par]
print("NUEVO ARRAY")


indices_inter = [str(i) for i in range(len(lista_intercalada))]
valores_inter = [str(v) for v in lista_intercalada]
anchos_inter = [max(len(ix), len(val)) + 2 for ix, val in zip(indices_inter, valores_inter)]

cols_indices_inter = " | ".join(f"{ix:^{w}}" for ix, w in zip(indices_inter, anchos_inter))
cols_valores_inter = " | ".join(f"{val:^{w}}" for val, w in zip(valores_inter, anchos_inter))

cabecera_inter = f"Índice | {cols_indices_inter} |"
fila_valor_inter = f"Valor  | {cols_valores_inter} |"
separador_inter = "-" * max(len(cabecera_inter), len(fila_valor_inter))

print("\n" + separador_inter)
print(cabecera_inter)
print(separador_inter)
print(fila_valor_inter)
print(separador_inter)
