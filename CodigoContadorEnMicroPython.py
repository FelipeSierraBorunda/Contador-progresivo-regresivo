# Importar librerías necesarias
import time
from machine import Pin

# Definir los estados posibles del sistema
class TIPODEESTADO:
    INICIAL = 0   # Estado inicial del contador
    FINAL = 1     # Estado final del contador
    PROGRESIVO = 2  # Contador aumentando
    REGRESIVO = 3   # Contador disminuyendo
    PAUSA = 4       # Contador en pausa

# Definir tipos de pausa
class TIPOPAUSA:
    PROGRESIVA = 2  # Pausa mientras el contador sube
    REGRESIVA = 3   # Pausa mientras el contador baja

# Definir pines de los segmentos del display de 7 segmentos
Seg_a = Pin(5, Pin.OUT)
Seg_b = Pin(18, Pin.OUT)
Seg_c = Pin(2, Pin.OUT)
Seg_d = Pin(22, Pin.OUT)
Seg_e = Pin(23, Pin.OUT)
Seg_f = Pin(4, Pin.OUT)
Seg_g = Pin(15, Pin.OUT)

# Definir pines de los cátodos para multiplexar el display
Catodo_0 = Pin(4, Pin.OUT)
Catodo_1 = Pin(2, Pin.OUT)
Catodo_2 = Pin(19, Pin.OUT)
Catodo_3 = Pin(21, Pin.OUT)

# Definir pines de los pulsadores de control
BtnAzul = Pin(36, Pin.IN)   # Controla el conteo progresivo
BtnRojo = Pin(39, Pin.IN)   # Controla el conteo regresivo
BtnBlanco = Pin(34, Pin.IN) # Reinicia el contador durante la pausa

# Matriz que define qué segmentos se encienden para cada dígito (0-9)
Digitos = [
    [1,1,1,1,1,1,0], # 0
    [0,1,1,0,0,0,0], # 1
    [1,1,0,1,1,0,1], # 2
    [1,1,1,1,0,0,1], # 3
    [0,1,1,0,0,1,1], # 4
    [1,0,1,1,0,1,1], # 5
    [1,0,1,1,1,1,1], # 6
    [1,1,1,0,0,0,0], # 7
    [1,1,1,1,1,1,1], # 8
    [1,1,1,0,0,1,1]  # 9
]

# Apaga todos los displays (evita superposición de dígitos al multiplexar)
def ApagarDisplays():
    Catodo_0.value(1)
    Catodo_1.value(1)
    Catodo_2.value(1)
    Catodo_3.value(1)

# Asigna los valores a los segmentos para mostrar un dígito específico
def AsignarSegmentos(BCD_Value):
    Seg_a.value(Digitos[BCD_Value][0])
    Seg_b.value(Digitos[BCD_Value][1])
    Seg_c.value(Digitos[BCD_Value][2])
    Seg_d.value(Digitos[BCD_Value][3])
    Seg_e.value(Digitos[BCD_Value][4])
    Seg_f.value(Digitos[BCD_Value][5])
    Seg_g.value(Digitos[BCD_Value][6])

# Función principal del programa
def main():
    ApagarDisplays()  # Asegura que el display inicie apagado
    print("Iniciando el Programa...")

    # Variables para almacenar el estado de los botones
    EstadoActualBtnAzul = EstadoActualBtnRojo = EstadoActualBtnBlanco = 0
    EstadoAnteriorBtnAzul = EstadoAnteriorBtnRojo = EstadoAnteriorBtnBlanco = 0
    BtnAzulPresionado = BtnRojoPresionado = BtnBlancoPresionado = 0

    # Variables del sistema
    Display = 0       # Control de dígito actual en multiplexado
    Cuenta = 0        # Valor actual del contador
    MilisAcum = 0     # Acumulador para el tiempo transcurrido
    ESTADOACTUAL = TIPODEESTADO.INICIAL  # Estado inicial del sistema
    TIPODEPAUSA = TIPOPAUSA.PROGRESIVA   # Tipo de pausa predeterminado

    # Bucle principal del programa
    while True:
        # Calcular decenas y unidades del número a mostrar
        Decenas = Cuenta // 10
        Unidades = Cuenta % 10

        ApagarDisplays()  # Apaga todos los displays antes de actualizar

        # Leer el estado de los botones
        EstadoActualBtnAzul = BtnAzul.value()
        EstadoActualBtnRojo = BtnRojo.value()
        EstadoActualBtnBlanco = BtnBlanco.value()

        # Mostrar decenas o unidades dependiendo del ciclo
        if Display == 0:
            AsignarSegmentos(Decenas)
            Catodo_2.value(0)  # Enciende display de decenas
        else:
            AsignarSegmentos(Unidades)
            Catodo_3.value(0)  # Enciende display de unidades

        Display = (Display + 1) & 1  # Alterna entre decenas y unidades
        time.sleep_ms(1)  # Espera breve para el multiplexado
        MilisAcum += 1

        # Detectar flancos descendentes en los botones (presión)
        if EstadoAnteriorBtnAzul == 1 and EstadoActualBtnAzul == 0:
            BtnAzulPresionado = 1
        if EstadoAnteriorBtnRojo == 1 and EstadoActualBtnRojo == 0:
            BtnRojoPresionado = 1
        if EstadoAnteriorBtnBlanco == 1 and EstadoActualBtnBlanco == 0:
            BtnBlancoPresionado = 1

        # Lógica del botón azul: Control del conteo progresivo
        if BtnAzulPresionado == 1:
            if ESTADOACTUAL in [TIPODEESTADO.INICIAL, TIPODEESTADO.PAUSA]:
                ESTADOACTUAL = TIPODEESTADO.PROGRESIVO
            elif ESTADOACTUAL == TIPODEESTADO.PROGRESIVO:
                ESTADOACTUAL = TIPODEESTADO.PAUSA
                TIPODEPAUSA = TIPOPAUSA.PROGRESIVA

        # Lógica del botón rojo: Control del conteo regresivo
        elif BtnRojoPresionado == 1:
            if ESTADOACTUAL in [TIPODEESTADO.FINAL, TIPODEESTADO.PAUSA]:
                ESTADOACTUAL = TIPODEESTADO.REGRESIVO
            elif ESTADOACTUAL == TIPODEESTADO.REGRESIVO:
                ESTADOACTUAL = TIPODEESTADO.PAUSA
                TIPODEPAUSA = TIPOPAUSA.REGRESIVA

        # Lógica del botón blanco: Reinicio durante la pausa
        elif BtnBlancoPresionado == 1 and ESTADOACTUAL == TIPODEESTADO.PAUSA:
            if TIPODEPAUSA == TIPOPAUSA.PROGRESIVA:
                ESTADOACTUAL = TIPODEESTADO.INICIAL
            elif TIPODEPAUSA == TIPOPAUSA.REGRESIVA:
                ESTADOACTUAL = TIPODEESTADO.FINAL

        # Actualización del contador cada 500 ms
        if MilisAcum >= 500:
            MilisAcum = 0
            if ESTADOACTUAL == TIPODEESTADO.PROGRESIVO:
                Cuenta = min(Cuenta + 1, 99)
                if Cuenta == 99:
                    ESTADOACTUAL = TIPODEESTADO.FINAL
            elif ESTADOACTUAL == TIPODEESTADO.REGRESIVO:
                Cuenta = max(Cuenta - 1, 0)
                if Cuenta == 0:
                    ESTADOACTUAL = TIPODEESTADO.INICIAL
            elif ESTADOACTUAL == TIPODEESTADO.INICIAL:
                Cuenta = 0
            elif ESTADOACTUAL == TIPODEESTADO.FINAL:
                Cuenta = 99

            # Imprime el estado actual en consola
            print("==============================")
            print(f"El numero es: {Cuenta}")
            print(f"El boton azul: {EstadoActualBtnAzul}")
            print(f"El boton rojo: {EstadoActualBtnRojo}")
            print(f"El boton blanco: {EstadoActualBtnBlanco}")
            print(f"ESTADO: {ESTADOACTUAL}")

        # Actualizar estados anteriores de los botones
        EstadoAnteriorBtnAzul = EstadoActualBtnAzul
        EstadoAnteriorBtnRojo = EstadoActualBtnRojo
        EstadoAnteriorBtnBlanco = EstadoActualBtnBlanco

        # Reiniciar el estado de presión de los botones
        BtnAzulPresionado = BtnRojoPresionado = BtnBlancoPresionado = 0

# Ejecutar la función principal si el archivo se corre directamente
if __name__ == "__main__":
    main()
