import pygame
pygame.init()
fonts = pygame.font.get_fonts()
print("Available fonts containing 'hiragino' or 'gothic':")
for f in fonts:
    if 'hiragino' in f.lower() or 'gothic' in f.lower():
        print(f)
