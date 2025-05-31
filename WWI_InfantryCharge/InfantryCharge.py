import pygame
import random
import math
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Batalla de Verdun - 1916")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
GREEN = (34, 139, 34)
BLUE = (0, 0, 128)
YELLOW = (255, 255, 0)


# Cargar imágenes (usaremos formas básicas por simplicidad)
# En una implementación real, podrías cargar sprites

# Clases
class Soldier:
    def __init__(self, x, y, is_french):
        self.x = x
        self.y = y
        self.is_french = is_french
        self.speed = random.uniform(0.5, 1.5)
        self.alive = True
        self.wounded = False
        self.wound_time = 0
        self.direction = 1 if is_french else -1
        self.color = BLUE if is_french else GRAY
        self.target_x = random.randint(WIDTH // 2, WIDTH) if is_french else random.randint(0, WIDTH // 2)
        self.falling = False
        self.fall_angle = 0
        self.death_time = 0

    def update(self, explosions, bullets):
        if not self.alive:
            self.death_time += 1
            return

        # Movimiento
        if not self.wounded and not self.falling:
            move_x = random.uniform(-0.5, 1) * self.direction * self.speed
            self.x += move_x

            # Movimiento hacia adelante con cierta aleatoriedad
            if random.random() < 0.7:
                self.x += 0.5 * self.direction * self.speed

            # Movimiento en Y (avanzar hacia las trincheras enemigas)
            if self.is_french:
                self.y += random.uniform(-0.2, 0.5)
            else:
                self.y += random.uniform(-0.5, 0.2)

            # Mantener dentro de límites
            self.x = max(0, min(WIDTH, self.x))
            self.y = max(100, min(HEIGHT - 50, self.y))

        # Verificar explosiones cercanas
        for exp in explosions:
            dist = math.sqrt((self.x - exp.x) ** 2 + (self.y - exp.y) ** 2)
            if dist < exp.radius and random.random() < 0.3:
                if random.random() < 0.5:
                    self.wounded = True
                    self.wound_time = random.randint(30, 180)
                else:
                    self.falling = True
                    self.alive = False

        # Verificar balas
        for bullet in bullets:
            if bullet.active and abs(self.x - bullet.x) < 10 and abs(self.y - bullet.y) < 10:
                if random.random() < 0.7:  # 70% de probabilidad de ser herido por bala
                    self.wounded = True
                    self.wound_time = random.randint(30, 180)
                    bullet.active = False
                elif random.random() < 0.3:  # 30% de muerte instantánea
                    self.falling = True
                    self.alive = False
                    bullet.active = False

        # Actualizar estado de herido
        if self.wounded:
            self.wound_time -= 1
            if self.wound_time <= 0:
                if random.random() < 0.2:  # 20% de probabilidad de recuperarse
                    self.wounded = False
                else:
                    self.falling = True
                    self.alive = False

        # Caída (muerte)
        if self.falling and self.fall_angle < 90:
            self.fall_angle += 5

    def draw(self, screen):
        if not self.alive and self.death_time > 300:  # No dibujar cadáveres después de 300 frames
            return

        # Dibujar soldado
        if self.alive and not self.falling:
            # Cuerpo
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
            # Cabeza
            pygame.draw.circle(screen, (200, 150, 100), (int(self.x + 3 * self.direction), int(self.y - 7)), 4)

            # Sangre si está herido
            if self.wounded:
                for _ in range(3):
                    blood_x = self.x + random.uniform(-5, 5)
                    blood_y = self.y + random.uniform(-5, 5)
                    pygame.draw.circle(screen, DARK_RED, (int(blood_x), int(blood_y)), 2)
        elif self.falling:
            # Dibujar soldado caído
            angle_rad = math.radians(self.fall_angle)
            fall_length = 10
            end_x = self.x + fall_length * math.cos(angle_rad) * self.direction
            end_y = self.y + fall_length * math.sin(angle_rad)

            pygame.draw.line(screen, self.color, (self.x, self.y), (end_x, end_y), 3)
            pygame.draw.circle(screen, (200, 150, 100), (int(end_x), int(end_y - 2)), 4)

            # Charcos de sangre
            if random.random() < 0.1 and self.fall_angle > 45:
                blood_size = random.randint(3, 8)
                pygame.draw.circle(screen, DARK_RED, (int(self.x), int(self.y + 5)), blood_size)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = random.randint(20, 40)
        self.growth_rate = random.uniform(0.5, 1.5)
        self.active = True

    def update(self):
        self.radius += self.growth_rate
        if self.radius >= self.max_radius:
            self.active = False

    def draw(self, screen):
        if self.active:
            alpha = 255 * (1 - self.radius / self.max_radius)
            explosion_surface = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(explosion_surface, (255, 165, 0, alpha),
                               (self.max_radius, self.max_radius), self.radius)
            pygame.draw.circle(explosion_surface, (255, 0, 0, alpha / 2),
                               (self.max_radius, self.max_radius), self.radius / 2)
            screen.blit(explosion_surface, (self.x - self.max_radius, self.y - self.max_radius))


class Bullet:
    def __init__(self, x, y, is_french):
        self.x = x
        self.y = y
        self.speed = random.uniform(3, 6)
        self.direction = 1 if is_french else -1
        self.active = True

    def update(self):
        self.x += self.speed * self.direction
        if self.x < 0 or self.x > WIDTH:
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.line(screen, YELLOW, (self.x, self.y), (self.x - 3 * self.direction, self.y), 1)


class Smoke:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 2
        self.max_radius = random.randint(10, 20)
        self.growth_rate = random.uniform(0.2, 0.5)
        self.lifetime = random.randint(50, 150)
        self.age = 0
        self.active = True

    def update(self):
        self.radius += self.growth_rate
        self.age += 1
        self.y -= 0.2  # El humo sube

        if self.age >= self.lifetime or self.radius >= self.max_radius:
            self.active = False

    def draw(self, screen):
        if self.active:
            alpha = 255 * (1 - self.age / self.lifetime)
            smoke_surface = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(smoke_surface, (100, 100, 100, alpha),
                               (self.max_radius, self.max_radius), self.radius)
            screen.blit(smoke_surface, (self.x - self.max_radius, self.y - self.max_radius))


# Función para dibujar el terreno
def draw_terrain(screen):
    # Cielo
    pygame.draw.rect(screen, (70, 70, 100), (0, 0, WIDTH, HEIGHT // 3))

    # Tierra (campo de batalla)
    pygame.draw.rect(screen, BROWN, (0, HEIGHT // 3, WIDTH, HEIGHT))

    # Trincheras francesas (lado izquierdo)
    for i in range(0, HEIGHT // 3, 10):
        pygame.draw.line(screen, BLACK, (50, HEIGHT // 3 + i), (100, HEIGHT // 3 + i + 5), 2)

    # Trincheras alemanas (lado derecho)
    for i in range(0, HEIGHT // 3, 10):
        pygame.draw.line(screen, BLACK, (WIDTH - 50, HEIGHT // 3 + i), (WIDTH - 100, HEIGHT // 3 + i + 5), 2)

    # Alambre de púas
    for i in range(20):
        # Lado francés
        pygame.draw.circle(screen, (150, 150, 150), (30, HEIGHT // 3 + 10 + i * 15), 2)
        pygame.draw.line(screen, (150, 150, 150), (20, HEIGHT // 3 + 10 + i * 15), (40, HEIGHT // 3 + 10 + i * 15), 1)

        # Lado alemán
        pygame.draw.circle(screen, (150, 150, 150), (WIDTH - 30, HEIGHT // 3 + 10 + i * 15), 2)
        pygame.draw.line(screen, (150, 150, 150), (WIDTH - 20, HEIGHT // 3 + 10 + i * 15),
                         (WIDTH - 40, HEIGHT // 3 + 10 + i * 15), 1)

    # Craters
    for _ in range(5):
        crater_x = random.randint(100, WIDTH - 100)
        crater_y = random.randint(HEIGHT // 3, HEIGHT - 50)
        pygame.draw.circle(screen, (80, 60, 40), (crater_x, crater_y), random.randint(10, 30))
        pygame.draw.circle(screen, (60, 40, 20), (crater_x, crater_y), random.randint(5, 15))


# Función principal
def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20)

    # Crear soldados franceses
    french_soldiers = [Soldier(random.randint(50, 150), random.randint(HEIGHT // 3, HEIGHT - 100), True) for _ in
                       range(30)]

    # Crear soldados alemanes
    german_soldiers = [
        Soldier(random.randint(WIDTH - 150, WIDTH - 50), random.randint(HEIGHT // 3, HEIGHT - 100), False) for _ in
        range(20)]

    explosions = []
    bullets = []
    smoke_particles = []

    frame_count = 0
    running = True

    while running and frame_count < 1800:  # 60 segundos a 30 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Generar explosiones aleatorias
        if random.random() < 0.05:
            x = random.randint(100, WIDTH - 100)
            y = random.randint(HEIGHT // 3, HEIGHT - 50)
            explosions.append(Explosion(x, y))

            # Humo después de explosión
            for _ in range(3):
                smoke_particles.append(Smoke(x + random.uniform(-10, 10), y + random.uniform(-10, 10)))

        # Generar balas aleatorias
        if random.random() < 0.2:
            if random.random() < 0.6:  # 60% balas francesas
                x = random.randint(50, 150)
                y = random.randint(HEIGHT // 3, HEIGHT - 50)
                bullets.append(Bullet(x, y, True))
            else:  # 40% balas alemanas
                x = random.randint(WIDTH - 150, WIDTH - 50)
                y = random.randint(HEIGHT // 3, HEIGHT - 50)
                bullets.append(Bullet(x, y, False))

        # Actualizar todos los elementos
        for soldier in french_soldiers + german_soldiers:
            soldier.update(explosions, bullets)

        for explosion in explosions[:]:
            explosion.update()
            if not explosion.active:
                explosions.remove(explosion)

        for bullet in bullets[:]:
            bullet.update()
            if not bullet.active:
                bullets.remove(bullet)

        for smoke in smoke_particles[:]:
            smoke.update()
            if not smoke.active:
                smoke_particles.remove(smoke)

        # Dibujar
        draw_terrain(screen)

        # Dibujar humo primero (para que quede detrás)
        for smoke in smoke_particles:
            smoke.draw(screen)

        # Dibujar explosiones
        for explosion in explosions:
            explosion.draw(screen)

        # Dibujar balas
        for bullet in bullets:
            bullet.draw(screen)

        # Dibujar soldados
        for soldier in french_soldiers + german_soldiers:
            soldier.draw(screen)

        # Mostrar contador de bajas
        french_dead = sum(1 for s in french_soldiers if not s.alive)
        german_dead = sum(1 for s in german_soldiers if not s.alive)

        dead_text = font.render(f"Bajas: Franceses {french_dead}/30 - Alemanes {german_dead}/20", True, WHITE)
        screen.blit(dead_text, (10, 10))

        # Mostrar tiempo transcurrido
        time_passed = frame_count // 30  # Convertir a segundos
        time_text = font.render(f"Tiempo: {time_passed}s / 60s", True, WHITE)
        screen.blit(time_text, (10, 40))

        pygame.display.flip()
        clock.tick(30)
        frame_count += 1

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()