import pygame
import sys
import time

print("Starting pygame test...")

# Initialize pygame
pygame.init()
print("Pygame initialized")

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Test Window")
print("Window created")

# Fill background with red
screen.fill((255, 0, 0))
pygame.display.flip()
print("Window should be visible now (filled with red)")

# Keep the window open for 5 seconds
print("Keeping window open for 5 seconds...")
start_time = time.time()
running = True

while running and time.time() - start_time < 5:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Keep updating the display
    pygame.display.flip()
    
print("Test complete")
pygame.quit()
sys.exit(0) 