def main():
    cloth = VerletCloth()

    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        screen.fill((0, 0, 0))

        cloth.render(screen)

        pygame.display.set_caption(f'Verlet Cloth Physics | FPS: {round(clock.get_fps())}')
        pygame.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    from verlet_cloth import VerletCloth

    import pygame
    import sys
    
    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption('Verlet Cloth Physics')
    pygame.mouse.set_visible(True)

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    main()
    
    pygame.quit()
    pygame.mixer.quit()

    sys.exit()
