# Escribe un programa que muestre tu horario de clase. Cada módulo o asignatura debe mostrarse en un color diferente.

print(f"{"Lunes":^45} | {"Martes":^45} | {"Miercoles":^45} | {"Jueves":^45} | {"Viernes":^45} \n"
      f"\033[36m{"Programacion Orientada a objetos":^45}\033[0m | \033[91m{"Análisis de datos en Python":^45}\033[0m | \033[91m{"Análisis de datos en Python":^45}\033[0m | \033[36m{"Programacion Orientada a objetos":^45}\033[0m | \033[35m{"Estructuras de control en Python":^45}\033[0m \n"
      f"\033[36m{"Programacion Orientada a objetos":^45}\033[0m | \033[92m{"Entornos y sintaxis en Python":^45}\033[0m | \033[91m{"Análisis de datos en Python":^45}\033[0m | \033[36m{"Programacion Orientada a objetos":^45}\033[0m | \033[35m{"Estructuras de control en Python":^45}\033[0m \n"
      f"\033[36m{"Programacion Orientada a objetos":^45}\033[0m | \033[92m{"Entornos y sintaxis en Python":^45}\033[0m | \033[91m{"Análisis de datos en Python":^45}\033[0m | \033[36m{"Programacion Orientada a objetos":^45}\033[0m | \033[35m{"Estructuras de control en Python":^45}\033[0m"
      )