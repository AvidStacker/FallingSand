from colorsys import hsv_to_rgb
import pygame
import sys
import random

# Constants for window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Grid:
    def __init__(self, cell_size, grid_lines_enabled=True):
        self.cell_size = cell_size
        self.cols = WINDOW_WIDTH // cell_size
        self.rows = WINDOW_HEIGHT // cell_size
        self.grid = self.gen_2DArray(self.cols, self.rows)
        self.grid_lines_enabled = grid_lines_enabled  # Boolean to control grid lines
        self.current_hue = 0  # This will control the hue for new particles

    def gen_2DArray(self, cols, rows, initial_value=None):
        return [[initial_value for _ in range(rows)] for _ in range(cols)]
    
    def draw(self, surface):
        # Draw the grid and the particles
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, 
                                   self.cell_size, self.cell_size)
                particle = self.grid[col][row]
                if particle:
                    # Draw existing particles with their original hue
                    color = hsb_to_rgb_custom(particle['original_hue'], 255, 255)  # Original hue
                    pygame.draw.rect(surface, color, rect)  # Draw particle
                else:
                    pygame.draw.rect(surface, BLACK, rect)  # Draw empty space
                
                # Draw grid lines only if grid_lines_enabled is True
                if self.grid_lines_enabled:
                    pygame.draw.rect(surface, WHITE, rect, 1)  # Draw grid lines

    def update_grid_state(self):
        new_grid = self.gen_2DArray(self.cols, self.rows)
        for i in range(self.cols):
            for j in range(self.rows):
                particle = self.grid[i][j]
                if particle:
                    direction = 1
                    if random.uniform(0,1) < 0.5:
                        direction *= -1
                    if j == self.rows - 1:
                        new_grid[i][j] = particle
                    elif self.grid[i][j+1] is None:
                        new_grid[i][j + 1] = particle
                    elif 0 <= i + direction <= self.cols - 1 and self.grid[i + direction][j + 1] is None:
                        new_grid[i + direction][j + 1] = particle
                    elif 0 <= i - direction <= self.cols - 1 and self.grid[i - direction][j + 1] is None:
                        new_grid[i - direction][j + 1] = particle
                    else:
                        new_grid[i][j] = particle

        self.grid = new_grid

    def update_current_hue(self):
        # Gradually increase the current hue for new particles
        self.current_hue = (self.current_hue + 1) % 360

def hsb_to_rgb_custom(h, s, b, h_max=360, s_max=255, b_max=255):
    # Normalize HSB values to the range [0, 1]
    h_normalized = h / h_max
    s_normalized = s / s_max
    b_normalized = b / b_max
    
    # Convert to RGB using normalized values
    r, g, b = hsv_to_rgb(h_normalized, s_normalized, b_normalized)
    
    # Convert RGB from [0, 1] range to [0, 255] range
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    
    return (r, g, b)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Falling Sand Simulation")

    # Initialize Grid with grid_lines_enabled set to True
    grid = Grid(cell_size=10, grid_lines_enabled=True)

    FPS = 60
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:  # Press 'G' to toggle grid lines
                    grid.grid_lines_enabled = not grid.grid_lines_enabled  # Toggle grid lines
        
        if pygame.mouse.get_pressed()[0]:  # Left mouse button is held
            # Add particles where the mouse is clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // grid.cell_size
            row = mouse_y // grid.cell_size 
            if 0 <= col < grid.cols and 0 <= row < grid.rows:
                if not grid.grid[col][row]:  # Only place particle if empty
                    grid.grid[col][row] = {'original_hue': grid.current_hue}  # Assign current hue as original hue
        
        # Update the grid state (simulate particle falling)
        grid.update_grid_state()

        # Update the current hue for new particles
        grid.update_current_hue()

        # Draw the grid and particles
        grid.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)  # Cap the frame rate at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
