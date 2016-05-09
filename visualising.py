import pygame
from numpy import copy

BLACK = 0  , 0  , 0
WHITE = 255, 255, 255
RED =   255, 0  , 0
GREEN = 0  , 150, 0
BLUE =  0  , 0  , 255

SCALE = 40  # multiply each coordinate by this while rescaling
DELAY = 50

class visio:

    def __init__(self, resolution, polygon, scale=SCALE, delay=DELAY):
        pygame.init()
        self.figure = copy(polygon)
        self.resolution = resolution
        self.screen = pygame.display.set_mode(resolution)
        self.scale = scale
        self.delay = delay
        self.pause_pressed = True
        self.last = 0
        self.text_pause = "[pause]"
        self.myfont = pygame.font.SysFont("helvetica", 20)
        self.label_pause = self.myfont.render(self.text_pause, 1, RED)
        self.label_finish = self.myfont.render("FINISH", 1, GREEN)

        for i in range(self.figure.shape[0]):
            self.figure[i] *= scale
            self.figure[i][1] = resolution[1] - self.figure[i][1]

    def visualize(self, segments, finish):
        time = pygame.time.get_ticks()

        for i in range(self.last, segments.shape[0]):   # rescaling - changing coordinates of points
            segments[i] *= self.scale
            segments[i][0][1] = self.resolution[1] - segments[i][0][1]
            segments[i][1][1] = self.resolution[1] - segments[i][1][1]
        self.last = segments.shape[0]

        running = True

        while running:
            self.screen.fill(WHITE)
            for line in segments:
                pygame.draw.aaline(self.screen, BLUE, line[0], line[1])
            pygame.draw.aalines(self.screen, BLACK, True, self.figure)

            if self.pause_pressed:
                self.screen.blit(self.label_pause, (self.resolution[0]-self.myfont.size(self.text_pause)[0], 5))
            if finish:
                self.screen.blit(self.label_finish, (5, 5+self.myfont.size("Delay")[1]))
            label_delay = self.myfont.render("Delay: "+str(self.delay)+" ms", 1, RED)
            self.screen.blit(label_delay, (5, 5))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.delay += 5
            elif keys[pygame.K_LEFT] and self.delay >= 5:
                self.delay -= 5

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_p:
                        self.pause_pressed = not self.pause_pressed

            pygame.display.flip()

            if not finish and pygame.time.get_ticks() - time > self.delay and not self.pause_pressed:
                running = False