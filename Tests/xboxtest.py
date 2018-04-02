import pygame
pygame.init()
while 1:
    pygame.joystick.init()
    print(pygame.joystick.get_count())
    #pygame.joystick.quit()