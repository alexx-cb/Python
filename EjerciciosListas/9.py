# Un restaurante nos ha encargado una aplicación para colocar a los clientes en sus mesas. En una
# mesa se pueden sentar de 0 (mesa vacía) a 4 comensales (mesa llena). Cuando llega un cliente se le
# pregunta cuántos son. De momento el programa no está preparado para colocar a grupos mayores a 4,
# por tanto, si un cliente dice por ejemplo que son un grupo de 6, el programa dará el mensaje
# “Lo siento, no admitimos grupos de 6, haga grupos de 4 personas como máximo e intente de nuevo”.
# Para el grupo que llega, se busca siempre la primera mesa libre (con 0 personas). Si no quedan mesas
# libres, se busca donde haya un hueco para todo el grupo, por ejemplo si el grupo es de dos personas, se
# podrá colocar donde haya una o dos personas. Inicialmente, las mesas se cargan con valores aleatorios
# entre 0 y 4. Cada vez que se sientan nuevos clientes se debe mostrar el estado de las mesas. Los grupos
# no se pueden romper aunque haya huecos sueltos suficientes. El funcionamiento del programa se ilustra
# a continuación
import random

mesas = []

for i in range(0,10):
    mesas.append(random.randint(0,4))

print(mesas)

grupo = int(input("¿Cuántos son? (Introduzca -1 para finalizar): "))

while grupo != -1:

    while grupo > 4:
        print(f"Lo siento, no admitimos grupos de {grupo}, haga grupos de 4 personas como máximo e intente de nuevo")
        print(mesas)
        grupo = int(input("¿Cuántos son? (Introduzca -1 para finalizar): "))

    while True:
        try:
            for i in range(0, len(mesas)):

                if mesas[i] == 0:
                    print("entra")
                    mesas[i] = grupo
                    break
                break


            for i in range(0, len(mesas)):
                if mesas[i]+grupo <= 4:
                    mesas[i] += grupo
                    break

        except:
            print("no se ha podido asignarles una mesa")

        finally:
            print(mesas)
            grupo = int(input("¿Cuántos son? (Introduzca -1 para finalizar): "))

