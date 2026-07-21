import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Placement Preview Example")
clock = pygame.time.Clock()


class PlacementPreview:
    def __init__(self, radius=50):
        self.radius = radius
        # 1. Create a surface large enough to hold the circle and the line
        # pygame.SRCALPHA makes this surface completely transparent by default
        self.surface = pygame.Surface(
            (radius * 2, radius * 2), pygame.SRCALPHA)

        # 2. Draw the translucent shapes onto our preview surface once
        # Color format: (Red, Green, Blue, Alpha) where Alpha 0 is invisible, 255 is solid
        # Translucent green circle (Alpha = 100)
        pygame.draw.circle(self.surface, (0, 255, 0, 100),
                           (radius, radius), radius)

        # Translucent white line pointing up to show orientation (Alpha = 180)
        pygame.draw.line(self.surface, (255, 255, 255, 180),
                         (radius, radius), (radius, 0), 4)

    def draw(self, target_surface, mouse_pos):
        # 3. Blit the preview surface centered on the mouse position
        x = mouse_pos[0] - self.radius
        y = mouse_pos[1] - self.radius
        target_surface.blit(self.surface, (x, y))


# Game setup
preview = PlacementPreview(radius=60)

# Game loop
while True:
    screen.fill((30, 30, 30))  # Dark gray background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Draw the preview at the mouse position
    preview.draw(screen, mouse_pos)

    pygame.display.flip()
    clock.tick(60)
