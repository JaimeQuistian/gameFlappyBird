import pygame
import pygame_gui
import random

# Inicializamos Pygame
pygame.init()

# Configuración de la pantalla
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 600
Icon = pygame.image.load("Resures\pajaro.png")

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA)) #Crea la ventana con las dimenciones Ancho/Alto Pantalla
pygame.display.set_caption('Flappy Bird') #Establece el titulo
pygame.display.set_icon(Icon)
# Colores
BLANCO = (80, 180, 250) #Color de fondo RGB
NEGRO = (0, 0, 0) #Color del texto para el puntaje
VERDE = (0, 128, 0) #Color de las tuberias RGB

# Configuración de valores del juego
GRAVEDAD = 0.5
IMPULSO = 8
VELOCIDAD_TUBERIA = 5
ANCHO_TUBERIA = 70
ESPACIO_ENTRE_TUBERIAS = 150

# Configuración de nuestra ave
ALTO_PAJARO = 30
ANCHO_PAJARO = 30

# Cargar imágenes
ave = pygame.image.load('Resures/red.png')
ave = pygame.transform.scale(ave, (ANCHO_PAJARO, ALTO_PAJARO)) #Asignar tamaño al ave

imagen = pygame.image.load('Resures\cieloFondo.jpg')
imagen = pygame.transform.scale(imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))

class Pajaro:
    def __init__(self):
        self.rect = pygame.Rect(100, ALTO_PANTALLA // 2, ANCHO_PAJARO, ALTO_PAJARO)
        self.velocidad = 0

    def saltar(self):
        self.velocidad = -IMPULSO

    def mover(self):
        self.velocidad += GRAVEDAD
        self.rect.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(ave, self.rect.topleft)

class Tuberia:
    def __init__(self, x):
        self.altura = random.randint(50, ALTO_PANTALLA - ESPACIO_ENTRE_TUBERIAS - 50)
        self.rect_arriba = pygame.Rect(x, 0, ANCHO_TUBERIA, self.altura)
        self.rect_abajo = pygame.Rect(x, self.altura + ESPACIO_ENTRE_TUBERIAS, ANCHO_TUBERIA, ALTO_PANTALLA)

    def mover(self):
        self.rect_arriba.x -= VELOCIDAD_TUBERIA
        self.rect_abajo.x -= VELOCIDAD_TUBERIA

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, VERDE, self.rect_arriba)
        pygame.draw.rect(pantalla, VERDE, self.rect_abajo)

    def fuera_de_pantalla(self):
        return self.rect_arriba.x < -ANCHO_TUBERIA

def main():
    pygame.display.set_caption('Flappy Bird')
    reloj = pygame.time.Clock()
    pajaro = Pajaro()
    tuberias = [Tuberia(ANCHO_PANTALLA + 200 * i) for i in range(3)]
    puntaje = 0
    corriendo = True
    manager = pygame_gui.UIManager((ANCHO_PANTALLA, ALTO_PANTALLA))

    while corriendo:
        tiempo_delta = reloj.tick(30) / 1000.0
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pajaro.saltar()
            manager.process_events(evento)

        # Mover el pájaro y las tuberías
        pajaro.mover()
        for tuberia in tuberias:
            tuberia.mover()

        # Eliminar tuberías fuera de pantalla y añadir nuevas
        if tuberias[0].fuera_de_pantalla():
            tuberias.pop(0)
            tuberias.append(Tuberia(ANCHO_PANTALLA))
            puntaje += 1

        # Comprobar colisiones
        for tuberia in tuberias:
            if pajaro.rect.colliderect(tuberia.rect_arriba) or pajaro.rect.colliderect(tuberia.rect_abajo) or pajaro.rect.y > ALTO_PANTALLA or pajaro.rect.y < 0:
                corriendo = False
                if mostrar_puntaje(puntaje):
                    return True  # Reiniciar el juego
                else:
                    return False  # Salir del juego

        # Dibujar
        pantalla.blit(imagen, (0,0))
        pajaro.dibujar(pantalla)
        for tuberia in tuberias:
            tuberia.dibujar(pantalla)

        # Mostrar puntaje
        fuente = pygame.font.SysFont(None, 36)
        texto = fuente.render(f"Puntaje: {puntaje}", True, NEGRO)
        pantalla.blit(texto, (10, 10))

        manager.update(tiempo_delta)
        manager.draw_ui(pantalla)

        pygame.display.flip()

def mostrar_puntaje(puntaje):
    # Crear una nueva ventana para mostrar el puntaje
    ventana_puntaje = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Puntaje Final')
    manager = pygame_gui.UIManager((600, 600),'color.json')

    texto_puntaje = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((200, 200), (200, 50)),
        text=f'Puntaje alcanzado: {puntaje}',
        manager=manager
    )

    boton_reiniciar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO_PANTALLA // 2 - 50, ALTO_PANTALLA // 2 - 50), (100, 50)),
        text='Reiniciar',
        manager=manager
    )
    boton_salir = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO_PANTALLA // 2 - 50, ALTO_PANTALLA // 2 + 10), (100, 50)),
        text='Salir',
        manager=manager
    )

    reloj = pygame.time.Clock()
    mostrando_puntaje = True

    while mostrando_puntaje:
        tiempo_delta = reloj.tick(30) / 1000.0
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Verifica si se cierra la ventana.
                mostrando_puntaje = False
                pygame.quit()
                return False
            if evento.type == pygame_gui.UI_BUTTON_PRESSED: # Verifica si se presiona el botón 'Reiniciar'.
                if evento.ui_element == boton_reiniciar:
                    mostrando_puntaje = False
                    return True
                if evento.ui_element == boton_salir: # Verifica si se presiona el botón 'Salir'.
                    mostrando_puntaje = False
                    pygame.quit()
                    return False

            manager.process_events(evento)

        manager.update(tiempo_delta)
        ventana_puntaje.fill(BLANCO)
        manager.draw_ui(ventana_puntaje)
        pygame.display.update()

def mostrar_menu():
    pygame.display.set_caption('Flappy Bird')
    # Inicializamos el gestor de UI con color de fondo
    manager = pygame_gui.UIManager((ANCHO_PANTALLA, ALTO_PANTALLA), 'color.json')

    # Creamos los botones
    boton_iniciar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO_PANTALLA // 2 - 50, ALTO_PANTALLA // 2 - 50), (100, 50)),
        text='Iniciar/Jugar',
        manager=manager
    )
    boton_cerrar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO_PANTALLA // 2 - 50, ALTO_PANTALLA // 2 + 10), (100, 50)),
        text='Cerrar',
        manager=manager
    )

    reloj = pygame.time.Clock()
    menu_abierto = True

    while menu_abierto:
        tiempo_delta = reloj.tick(30) / 1000.0
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                menu_abierto = False
                pygame.quit()
                return False
            if evento.type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == boton_iniciar:
                    menu_abierto = False
                    return True
                if evento.ui_element == boton_cerrar:
                    menu_abierto = False
                    pygame.quit()
                    return False

            manager.process_events(evento)

        manager.update(tiempo_delta)
        pantalla.fill(BLANCO)
        manager.draw_ui(pantalla)
        pygame.display.update()

if __name__ == "__main__":
    while mostrar_menu(): # Mientras mostrar_menu() devuelva True, continúa ejecutando el bucle.
        if not main(): # Ejecuta la función main() y si devuelve False, rompe el bucle y termina el programa.
            break