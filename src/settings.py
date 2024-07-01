WIDTH = 1920
HEIGHT = 1080
SCREEN_SIZE = (WIDTH, HEIGHT)
SCREEN_CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60


RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def mod_rgb(imagen, frames):
    """Cambia el color de la imagen en rgb basado en frames"""
    imagen_copy = imagen.copy()
    width, height = imagen_copy.get_size()
    for x in range(width):
        for y in range(height):
            r, g, b, a = imagen_copy.get_at((x, y))
            r = (r + frames) % 256
            g = (g + frames * 2) % 256  # Ajusta la velocidad de cambio para el canal G
            b = (b + frames * 3) % 256  # Ajusta la velocidad de cambio para el canal B
            imagen_copy.set_at((x, y), (r, g, b, a))
    return imagen_copy