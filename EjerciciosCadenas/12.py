#Escribe un programa que genere la nómina (bien desglosada) de un empleado según las siguientes
# condiciones:
# • Se pregunta el cargo del empleado (1 - Prog. junior, 2 - Prog. senior, 3 – Jefe de proyecto), los
# días que ha estado de viaje visitando clientes durante el mes y su estado civil (1 - Soltero, 2 -
# Casado).
# • El sueldo base según el cargo es de 950, 1200 y 1600 euros según si se trata de un prog. junior,
# un prog. senior o un jefe de proyecto respectivamente.
# • Por cada día de viaje visitando clientes se pagan 30 euros extra en concepto de dietas. Al sueldo
# neto hay que restarle el IRPF, que será de un 25% en caso de estar soltero y un 20% en caso de
# estar casado.

print(f"1 - Programador Junior \n"
      f"2 - Programador Senior \n"
      f"3 - Jefe Proyecto \n")

cargo = int(input("Introduzca el cargo del empleado (1 - 3): "))
visitas = int(input("¿Cuántos días ha estado visitando clientes? "))
civil = int(input("Introduzca su estado civil (1 - Soltero, 2 - Casado): "))

sueldo =0
irpf =0

if cargo == 1:
    sueldo = 950
elif cargo == 2:
    sueldo = 1200
elif cargo == 3:
    sueldo = 1600

if civil == 1:
    irpf = 25
elif civil == 2:
    irpf = 20

print(f"{"---------------------------------":^20}\n"
      f"|{"Sueldo Base":<20} {sueldo:>10}|\n"
      f"|{"Dietas":<20} {visitas * 30:>10}|\n"
      f"{"---------------------------------":^20}\n"
      f"|{"Sueldo Bruto":<20} {sueldo + (visitas * 30):>10}|\n"
      f"|Retención IRPF ({irpf}%) {(sueldo + (visitas * 30)) * irpf / 100:>10}|\n"
      f"{"---------------------------------":^20}\n"
      f"|{"Sueldo Neto":<20} {sueldo + (visitas * 30) - (sueldo + (visitas * 30)) * irpf / 100:>10}|\n")