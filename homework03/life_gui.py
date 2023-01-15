import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        # Создание новго окна
        self.screen = pygame.display.set_mode((640, 480))

    def draw_lines(self) -> None:
        # Получили размеры экрана
        w, h = pygame.display.get_surface().get_size()
        # Количество столбцов и строк в поле
        c, r = self.life.cols, self.life.rows

        # Координаты начала сетки (пусть будет по-середине)
        l, t = (w - self.cell_size * c) // 2, (h - self.cell_size * r) // 2

        for x in range(c + 1):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (l, t + x * self.cell_size),
                (w - l, t + x * self.cell_size),
            )
        for y in range(r + 1):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (l + y * self.cell_size, t),
                (l + y * self.cell_size, h - t),
            )

    def draw_grid(self) -> None:
        # Получили размеры экрана
        w, h = pygame.display.get_surface().get_size()
        # Количество столбцов и строк в поле
        c, r = self.life.cols, self.life.rows

        # Координаты начала сетки (пусть будет по-середине)
        l, t = (w - self.cell_size * c) // 2, (h - self.cell_size * r) // 2

        for i in range(r):
            for j in range(c):
                if self.life.curr_generation[i][j] == 1:
                    bt, bl = t + self.cell_size * i, l + self.cell_size * j
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (bl, bt, self.cell_size, self.cell_size),
                    )

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT: #type: ignore
                    running = False

            # Очистка экрана
            self.screen.fill(pygame.Color("white"))

            # Рисуем сетку
            self.draw_lines()
            # Рисуем сетку
            self.draw_grid()

            # Переходим к следующему поколению
            self.life.step()

            if not self.life.is_changing:
                running = False

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
