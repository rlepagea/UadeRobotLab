# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido: Rafael Lepage, Austin Zacarias Steel, Juan , Geronimo
#  Comision:          Lunes Noche
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO

# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)
    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    if len(comando) == 0:
        return False
    nombre = comando[0]
    if nombre in ("detenerse", "saludar"):
        return len(comando) == 1
    if nombre in ("avanzar", "girar"):
        if len(comando) != 3:
            return False
        velocidad = comando[1]
        tiempo = comando[2]
        if type(velocidad) not in (int, float) or type(tiempo) not in (int, float):
            return False
        return tiempo >= 0
    return False


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================

Velocidad_Max=0.20
Giro_Max =0.50
Tiempo_Max =10
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    # TU CODIGO ACA


    nombre = comando[0]
    try:
       if nombre == "avanzar":
        velocidad = comando[1]
        tiempo = comando[2]
        if velocidad > Velocidad_Max or velocidad < -Velocidad_Max:
            resultado = "Rechazado la velocidad supera " + str(Velocidad_Max) + " m/s."
        elif tiempo > Tiempo_Max:
            resultado = "Rechazado el tiempo supera " + str(Tiempo_Max) + " s."
        else:
            robot.avanzar(velocidad=velocidad, tiempo=tiempo)
            resultado = "Avanza Hacia " + str(velocidad) + " m/s durante " + str(tiempo) + " s."

       elif nombre =="girar":
         velocidad = comando[1]
         tiempo = comando[2]
         if velocidad >Giro_Max or velocidad<-Giro_Max:
            resultado= "Rechazado el giro supera "+ str(Giro_Max) + " rad/s "
         elif tiempo > Tiempo_Max:
            resultado = "Rechazado el tiempo supera " + str(Tiempo_Max) + " s."
         else:
            robot.girar(velocidad=velocidad,tiempo=tiempo)
            resultado = "Giro a " + str(velocidad)+ " rad/s durante " + str(tiempo)+" s "

       elif nombre =="detenerse":
         robot.detenerse()
         resultado= "El robot se detuvo"
    
       elif nombre =="saludar":
         robot.saludar()
         resultado="El robot saludo"
    except ErrorDeSeguridad as error:
        resultado ="rechazado por seguridad:"+ str(error)
    return resultado
    


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================

def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.
 
    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso
 
    Un comando invalido NO tiene que cortar la mision.
    """
    for comando in mision:
        if not comando_es_valido(comando):
            historial.append({
                "comando": comando,
                "estado": "rechazado",
                "motivo": motivo_invalido(comando),
            })
            continue
 
        resultado = ejecutar_comando(robot, comando)
        if resultado.lower().startswith("rechazado"):
            estado = "rechazado"
        else:
            estado = "ejecutado"
        historial.append({
            "comando": comando,
            "estado": estado,
            "motivo": resultado,
        })
 
 
def motivo_invalido(comando):
    """Devuelve un texto que explica por que un comando no es valido."""
    if len(comando) == 0:
        return "Rechazado: el comando esta vacio."
    nombre = comando[0]
    if nombre in ("detenerse", "saludar"):
        return "Rechazado: '" + str(nombre) + "' no lleva datos."
    if nombre in ("avanzar", "girar"):
        if len(comando) != 3:
            return "Rechazado: '" + nombre + "' necesita velocidad y tiempo."
        velocidad = comando[1]
        tiempo = comando[2]
        if type(velocidad) not in (int, float) or type(tiempo) not in (int, float):
            return "Rechazado: velocidad y tiempo tienen que ser numeros."
        if tiempo < 0:
            return "Rechazado: el tiempo no puede ser negativo."
    return "Rechazado: el comando '" + str(nombre) + "' no existe."
 
 


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    ejecutados = 0
    rechazados = []

    for registro in historial:
        if registro["estado"] == "ejecutado":
            ejecutados = ejecutados + 1
        else:
            rechazados.append(registro)

    print()
    print("=" * 50)
    print("              REPORTE DE LA MISION")
    print("=" * 50)
    print("Comandos totales:     " + str(len(historial)))
    print("Ejecutados con exito: " + str(ejecutados))
    print("Rechazados:           " + str(len(rechazados)))
    print("-" * 50)

    if len(rechazados) == 0:
        print("No hubo comandos rechazados. Mision completa.")
    else:
        print("Detalle de los rechazos:")
        numero = 1
        for registro in rechazados:
            print("  " + str(numero) + ". " + str(registro["comando"]))
            print("     Motivo: " + registro["motivo"])
            numero = numero + 1

    print("=" * 50)


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_BASICA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
