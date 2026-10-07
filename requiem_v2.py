import random

mapa = {
    "hall": {"oeste": "oficina", "este": "ala_este", "subterraneo": "subterraneo"},
    "oficina": {"este": "hall", "norte": "cuarto_oscuro"},
    "cuarto_oscuro": {"sur": "oficina"},
    "ala_este": {"oeste": "hall", "sur": "pasillo"},
    "pasillo": {"norte": "ala_este", "calles": "calles"},
    "subterraneo": {"arriba": "hall"}
}

ubicacion = "hall"
inventario = ["linterna", "pistola"]
balas = 3
salud_jugador = 3
salud_zombie = 2
juego_activo = True
linterna_encendida = False
jefe_derrotado = False
estatua_movida = False

TITULO = "\033[1;96m"
ALERTA = "\033[1;91m"
OBJETO = "\033[93m"
EXITO = "\033[1;92m"
RESET = "\033[0m"

def procesar_accion(comando_jugador):
    global ubicacion, balas, jefe_derrotado, linterna_encendida, juego_activo, salud_jugador, salud_zombie, estatua_movida

    match comando_jugador:

        case "oeste":
            if "oeste" in mapa[ubicacion]:
             ubicacion = mapa[ubicacion]["oeste"]
             print("Te mueves hacia el oeste.")
            else:
                print("No puedes ir por ahí.")

        case "este":
            if "este" in mapa[ubicacion]:
             ubicacion = mapa[ubicacion]["este"]
             print("Te mueves hacia el este.")
            else:
                print("No puedes ir por ahí.")

        case "norte":
            if "norte" in mapa[ubicacion]:
             ubicacion = mapa[ubicacion]["norte"]
             print("Te mueves hacia el norte.")
            else:
                print("No puedes ir por ahí.")

        case "sur":
            if ubicacion == "hall":
                if "llave de picas" in inventario:
                    print("Metes la llave de picas en la cerradura. ¡Clic! la enorme puerta se abre hacia el exterior..")
                    ubicacion = "calles_frente"
                else:
                    print("Empujas la puerta, pero está cerrada con llave. Tiene grabada una pica.")             
            elif "sur" in mapa[ubicacion]:
                ubicacion = mapa[ubicacion]["sur"]
                print("Te mueves hacia el sur.")
            else:
                print("No  puedes ir por ahí.")

        case "subterraneo":
            if ubicacion == "hall":
                if estatua_movida:
                      print("Bajas por las frías escaleras de piedra hacia la oscuridad...")
                      ubicacion = "subterraneo"
                else:
                    print("La enorme estatua bloquea el camino. Parece que necesita una pieza en su base para moverse..")
            else:
    
                print("No puedes ir por ahí.")

        case "calles":
            if ubicacion == "pasillo":
                print("Empujas la pesada puerta de emergencia para salir del edificio.")
                ubicacion = "callejon_emergencia"
            elif ubicacion == "subterraneo" and jefe_derrotado:
                print("Avanzas a través del agujero humeante en la pared...")
                ubicacion = "calles_alcantarrilla"
            else:
             print("No hay salida hacia las calles desde aquí.")

        case "ayuda":
            print(f"\n{TITULO}--- GUÍA DE SUPERVIVENCIA ---{RESET}")
            print("Sistema: salir")
            print("Movimiento: norte, sur, este, oeste, arriba, abajo")
            print("Exploración: buscar, inventario, salida")
            print("Acción: disparar, curar")

            if "linterna" in inventario:
                print("Iluminación: encender linterna, apagar linterna")

            if "polvora" in inventario or "chatarra" in inventario:
                print("Supervivencia: fabricar munición")

            if "medallon del leon" in inventario:
                print("Puzzles: colocar medallon")

            if ubicacion == "subterraneo" or (ubicacion == "pasillo" and salud_zombie > 0):
                print("Combate avanzado: esquivar")
                
            if "lanzagranadas" in inventario:
                print("Armas pesadas: usar lanzagranadas")

            print("----------------------------\n")

        case "buscar":
                if ubicacion == "hall" and "llave de picas" not in inventario and "chatarra" not in inventario:
                        print(f"Revisas atrás del mostrador. Encuentras una {OBJETO}'llave de picas'{RESET} y {OBJETO}'chatarra'{RESET}.")
                        inventario.append("llave de picas")
                        inventario.append("chatarra")
    
                elif ubicacion == "subterraneo":
                        if "lanzagranadas" not in inventario:
                            print("Te deslizas por el lodo esquivando los escombros...")
                            print(f"¡Encuentras un {OBJETO}'lanzagranadas'{RESET} peaso entre los restos de un soldado!")
                            inventario.append("lanzagranadas")
                        else:
                            print("No hay tiempo para buscar más. ¡El monstruo te persigue!")
                
                elif ubicacion == "ala_este" and "medallon del leon" not in inventario:
                    if linterna_encendida:
                        print("Revisas las taquillas destrozadas bajo la luz de tu linterna.")
                        print(f"¡Encuentras un pesado {OBJETO}'medallon del leon'{RESET} de bronce!")
                        inventario.append("medallon del leon")
                    else:
                        print("Está demasiado oscuro. Si metes la mano ahí sin ver, algo podría morderte.")
                        
                elif ubicacion == "oficina_oeste" and "hierba verde" not in inventario and "polvora" not in inventario:
                            print(f"Revisas el escritorio del policía. Encuentras una {OBJETO}'hierba verde'{RESET} y {OBJETO}'polvora'{RESET}.")
                            inventario.append("hierba verde")
                            inventario.append("polvora")

                else:
                    contador_busquedas_inutiles +=1
                    if contador_busquedas_inutiles ==1:
                        print("No encuentras nada de valor aquí")
                    elif contador_busquedas_inutiles == 2:
                        print(f"{ALERTA} Ya revisaste a fondo. Seguir buscando aquí es una pérdida de tiempo.{RESET}")
                    elif contador_busquedas_inutiles == 3:
                        print(f"{ALERTA}¡Deja de hacer ruido! Estás revolviendo basura inútil y podrías atraer a los infectados...{RESET}")   
                    else:
                        print(f"\n{ALERTA}¡TE LO ADVERTI! Hiciste demasiado ruido...{RESET}")
                        print(f"{ALERTA}De las sombras emerge un infectado enorme empuñando un hacha de bomberos.{RESET}")
                        print(f"{ALERTA}Antes de que puedas reaccionar, el hacha se hunde en tu cabeza.{RESET}")
                        salud_jugador = 0
                        print(f"Tu salud cae de golpe a: {salud_jugador}")
                        print(f"\n{ALERTA} Tu terquedad te costó la vida... Fin del juego.{RESET}")
                        juego_activo = False
                        
                elif ubicacion == "oficina":
                        if "hierba verde" not in inventario and "polvora" not in inventario:
                            print(f"Revisas el escritorio del policía. Encuentras una {OBJETO}'hierba verde'{RESET} y {OBJETO}'polvora'{RESET}.")
                            inventario.append("hierba verde")
                            inventario.append("polvora")
                        else:
                            print("Solo quedan papeles manchados de sangre y grapadoras vacías.")
                else:
                    print("No hay nada interesante que buscar aquí.")
        
        case "fabricar municion":
                if "polvora" in inventario and "chatarra" in inventario:
                    print("Sacas tu herramienta de recarga. Combinas la pólvora con la chatarra metálica con cuidado...")
                    print(f"{EXITO}¡Has fabricado 2 balas nuevas!{RESET}")
        
                    balas += 2
                    inventario.remove("polvora")
                    inventario.remove("chatarra")
        
                    print(f"Balas totales: {balas}")
                else:
                    print("Te falta materiales. Necesitas 'pólvora' y 'chatarra' para fabricar munición.")
        
        case "encender linterna":
                if "linterna" in inventario:
                    linterna_encendida = True
                    print("¡Clic! Enciendes la linterna. Un rayo de luz ilumina tu camino.")
                else:
                    print("No tienes ninguna linterna.")
        
        case "apagar linterna":
                linterna_encendida = False
                print("Apagas la linterna para ahorrar batería.")
        
        case "usar lanzagranadas":
                    if ubicacion == "subterraneo":
                        if not linterna_encendida:
                            print("No ves absolutamente nada. Disparar a ciegas contra un monstruo es un suicidio. ¡Necesitas ver a tu objetivo!")
                        elif "lanzagranadas" in inventario:                        
                            print("¡Apuntas el enorme cañón del lanzagranadas al monstruo mutado y aprietas el gatillo!")
                            print("¡BOOM! La explosión ilumina el sótano y destroza el monstruo en pedazos.")
                            print("Detrás de sus restos, ves que la explosión voló una pared, revelando una salida hacia las 'calles'.")
        
                            mapa["subterraneo"]["calles"] = "calles"
                            inventario.remove("lanzagranadas")
                            jefe_derrotado = True
                        else:
                         print("¿De qué hablas? No tienes ningún lanzagranadas.")
                         
                    else:
                        print("Es un arma demasiado destructiva para usarla aquí. Guárdala para una emergencia.")
                        
        case "disparar":
                if balas > 0:
                    if ubicacion == "pasillo" and salud_zombie > 0:
                        print("¡Levantas tu pistola y apuntas!")
                        if balas > 0:
                            balas -=1
                            salud_zombie -= 1
                            print(f"le distes al zombie. Balas restantes: {balas}")

                            if salud_zombie <= 0:
                                print("¡El zombie se desploma sin vida!")
                            else:
                                salud_jugador -= 1
                                print(f"El zombie ruge y te araña violentamente. Salud actual: {salud_jugador}")
                                if salud_jugador <= 0:
                                    print("Caes al suelo desangrado...")
                                    juego_activo = False
                        else:
                            print("¡Clic, clic! Tu arma está vacía. Necesitas munición.")
                            print("¡El zombie aprovecha tu error y te muerde!")
                            salud_jugador -=1
                            if salud_jugador <=0:
                                print("No puedes resistir más... Fin del juego.")
                                juego_activo = False

                    elif ubicacion == "pasillo" and salud_zombie <= 0:
                        print("El oficial ya está muerto. No malgastes munición.")

                    elif ubicacion == "subterraneo" and not jefe_derrotado:
                        balas -=1
                        if linterna_encendida:
                            print("¡PUM! La bala impacta de lleno, pero rebota inofensivamente contra su gruesa piel mutada.")
                            print("El monstruo ruge enfurecido y se tensa, preparándose para aatacar. ¡Una pistola normal no le hara nada!")
                        else:
                            print("¡PUM! Disparas a ciegas en la oscuridad. Escuchas un gruñido ensordecedor que se prepara para embestirte.")

                        print(f"Te quedan {balas} balas.")

                    else:
                        if balas > 0:
                            balas -=1
                            print(f"¡PUM! disparas tu arma. El eco resuena en la habitación. Te quedan  {balas} balas.")
                else:
                    print("No te quedan balas en el cargador.")
        
        case "esquivar":
                if ubicacion == "pasillo" and salud_zombie > 0:
                    print("Intentas escabullirte por el estrecho pasillo esquivando al oficial...")

                    probabibilad = random.randint(1, 100)

                    if probabilidad <= 40:
                        print(f"{EXITO}Logras deslizarte por debajo de sus brazos podridos y evitas el daño.{RESET}")
                    else:
                        print(f"{ALERTA}Intentaste esquivar al zombie pero fallas, te termina acorralando contra la pared y hunde sus dientes en tu brazo.{RESET}")
                        salud_jugador -=1
                        print(f"Tu salud baja a: {salud_jugador}")

                        if salud_jugador <=0:
                            print(f"\n{ALERTA}Caes al suelo sin fuerzas. Eres la próxima comida del zombie... Fin del juego.{RESET}")
                            juego_activo = False

                elif ubicacion == "subterraneo" and not jefe_derrotado:
                    print("¡Te tiras al suelo justo cuando una garra gigante pasa silbando sobre tu cabeza!")
                    print("Sobreviviste a este ataque, pero no podrás esquivar para siempre.")
                else:
                    print("Estás saltando de un lado a otro sin razón. No hay nada amenazante aquí.")
        
        case "curar":
                if "hierba verde" in inventario:
                    salud_jugador += 1
                    inventario.remove("hierba verde")
                    print(f"{EXITO}Masticas la hierba verde. Su sabor es amargo pero tus heridas se cierran un poco.{RESET}")
                    print(f"{EXITO}Tu salud ha subido a: {salud_jugador}{RESET}")
                else:
                    print("Buscas desesperadamente en tu mochila, pero no tienes nada para curarte.")
        
        case "colocar medallon":
            if ubicacion == "hall":
                if "medallon del leon" in inventario:
                    print("Te acercas a la enorme estatua de la diosa en el centro del vestíbulo.")
                    print("Colocas el medallón de bronce en la ranura circular de la base. ¡Encaja perfectamente!")
                    print("Escuchas un fuerte estruendo mecánico. La estatua se desplaza, revelando unas escaleras hacia el 'subterraneo'.")

                    inventario.remove("medallon del leon")
                    estatua_movida = True
                elif estatua_movida:
                        print("Ya encajaste el medallón. El camino al subterráneo está abierto.")
                else:
                    print("No tienes nada en tu mochila que encaje en esa ranura.")
            else:
                print("No hay donde usar el medallón aquí.")
        
        case "salidas_posibles" | "salidas" | "salida":
            salidas = ", ".join(mapa[ubicacion].keys())
            print(f"Salidas disponibles desde aquí: {salidas}")
        
        case "inventario":
            print(f"\n{TITULO}--- INVENtARIO ---{RESET}")
            if len(inventario) > 0:
                for item in inventario:
                    print(f"- {item.capitalize()}")
            else:
                print("Tu mochila está vacía.")
            print("------------------\n")
        
        case "salir":
            print("Te rindes ante el terror... Fin del juego.")
            juego_activo = False
    
        case _:
            print("No entiendes cómo hacer eso. (Escribe 'ayuda' si estás perdido)")

juego_activo = True

while juego_activo:

    if ubicacion == "hall":
        print(f"\n{TITULO}--- HALL PRINCIPAL ---{RESET}")
        if estatua_movida:
            print("El inmenso vestíbulo de la comisaría. La estatua está desplazada, revelando escaleras al 'subterraneo'.")
            print("Al 'oeste' está la oficina. Al 'este' el pasillo de las celdas. Al 'sur' la puerta principal.")
        else:
            print("El inmenso vestículo de la comisaría. Hay una estatua de una diosa.")
            print("Notas que tiene una extraña ranura circular tallada en la base.")
            print("Al 'oeste' está la oficina. Al 'este' un pasillo oscuro. Al 'sur' hay una enorme puerta doble con una cerradura extraña.")

    elif ubicacion == "ala_este":   
        print(f"\n{TITULO}--- ALA ESTE ---{RESET}")
        if linterna_encendida:
            print("El haz de tu linterna corta la oscuridad. El lugar está destrozado.")
            print("Al 'oeste' puedes volver al hall. Al 'sur' ves la puerta hacia el pasillo de celdas.")
        else:
            print("Está completamente a oscuras. No ves más allá de tu nariz. Escuchas pasos arrastrándose.")
            print("La única salida que recuerdas está a tu espalda, hacia el 'oeste'.")

    elif ubicacion == "subterraneo":
        print(f"\n{TITULO}--- SUBTERRÁNEO ---{RESET}")
        print(f"Salud: {salud_jugador} | Balas: {balas}")
        print("El aire aquí es denso y huele a humedad. Las escaleras suben de regreso 'arriba' al hall.")

        if jefe_derrotado:
            print("Los restos del monstruo humean el suelo. Hay un agujero en la pared que lleva a las 'calles'.")
        elif linterna_encendida:
            print(F"¡El rayo de luz de tu linterna revela a un {ALERTA}monstruo mutante{RESET} bloqueando la salida!")
        else:
            print("Sientes que algo enorme respira en la oscuridad...")

    elif ubicacion == "oficina":
        print(f"\n{TITULO}--- OFICINA OESTE ---{RESET}")
        print("Archiveros volcados, sillas rotas y olor a pólvora. La única salida es de vuelta al 'este'.")
        print("Hay un escritorio de un policía que podrías 'buscar'.")

    elif ubicacion == "pasillo":
        print(f"\n{TITULO}--- PASILLO DE CELDAS ---{RESET}")
        print(f"Salud: {salud_jugador} | Balas: {balas}")
        if salud_zombie > 0:
            print(F"¡Un {ALERTA}oficial de policía zombificado{RESET} bloquea el pasillo!.")
            print(" Al 'norte' esta el hall y a las 'calles' esta la salida de emergencia.")
        else:
            print("El cadáver del oficial está en el suelo manchando las baldosas.")
            print("Al 'norte' esta el hall. La puerta de emergencia hacia las 'calles' esta libre.")

    elif ubicacion == "calles_frente":
        print(f"\n{TITULO}--- CALLES DE LA CIUDAD (FRENTE) ---{RESET}")
        print("Cruzas las enormes puertas del hall hacia la calle principal.")
        print("Una horda masiva de zombies te acorrala en las escaleras. No tienes suficiente munición...")
        print("No lograste escapar. Fin del juego.")
        juego_activo = False
        continue

    elif ubicacion == "callejon_emergencia":
        print(f"\n{TITULO}--- CALLEJÓN TRASERO ---{RESET}")
        if salud_zombie > 0:
            print("Intentas forzar la puerta de emergencia, pero el oficial zombie te muerde el cuello...")
            print("No loraste escapar. Fin del juego.")
        else:
                print("Empujas la puerta y sales a la lluviosa ciudad. Los callejones están llenos de fuego y destrucción.")
                print("Pero lograste salir de la comisaría con vida.")
                print("¡Felicidades! Has ganado el juego.")
        juego_activo = False
        continue                

    elif ubicacion == "calles_alcantarrilla":
        print(f"\n{TITULO}--- CALLES DE LA CIUDAD (ALCANTARRILLADO) ---{RESET}")
        print("Sales por el agujero en la pared hacia los oscuros callejones.")
        print("Escuchas cómo el subterráneo de la comisaría colapsa detrás de ti.")
        print(f"{EXITO}Sobreviviste a la verdadera pesadilla. Has ganado el juego{RESET}.")
        juego_activo = False
        continue            
    
    comando = input("\n¿Qué vas a hacer?: ").lower().strip()
    procesar_accion(comando)
