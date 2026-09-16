import pygame

pygame.init()

fenetre = pygame.display.set_mode((600, 600))
mon_image = pygame.image.load("omlogo.jpg")
NOIR= (0,0,0)
def draw_stickman():
    pygame.draw.circle(fenetre, NOIR, (200, 150), 50)
    pygame.draw.line(fenetre, NOIR, (200, 200), (200, 300), 5)
    pygame.draw.line(fenetre, NOIR, (150, 250), (250, 250), 5)
    pygame.draw.line(fenetre, NOIR, (200, 300), (150, 400), 5)
    pygame.draw.line(fenetre, NOIR, (200, 300), (250, 400), 5)

ouvert = True

while ouvert:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ouvert = False
    fenetre.blit(mon_image, (0, 0))
    draw_stickman()
    pygame.display.flip()


pygame.quit()