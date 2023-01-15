import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Создаем атрибут сетки
        self.grid: tp.List[tp.List[tp.Any]] = [[]] 

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT: #type: ignore
                    running = False

            # Очистка экрана
            self.screen.fill(pygame.Color("white"))

            # Рисуем сетку и клетки
            self.draw_lines()
            self.draw_grid()

            # Обновляем поле
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if not randomize:
            return [[0 for _ in range(self.cell_width)] for __ in range(self.cell_height)]
        return [
            [random.randint(0, 1) for _ in range(self.cell_width)] for __ in range(self.cell_height)
        ]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 1:
                    rect_desc = (
                        j * self.cell_size,
                        i * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    )
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect_desc)

    def is_valid_coordinates(self, top: int, left: int) -> bool:
        """
        Определяет, являются ли координаты top и left валидными для текущей сетки
        Валидными считаются такие, которые не выходят за пределы поля
        Parametrs
        ---------
        top : int
            Индекс ряда, в котором находится точка
        left : int
            Индекс столбца, в котором находится точка
        """
        if top >= 0 and top < self.cell_height and left >= 0 and left < self.cell_width:
            return True
        return False

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        res = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                top, left = cell[0] + i, cell[1] + j
                if self.is_valid_coordinates(top, left):
                    res.append(self.grid[top][left])

        return res

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = [[0 for _ in range(self.cell_width)] for __ in range(self.cell_height)]

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                temp = sum(self.get_neighbours((i, j)))
                if self.grid[i][j] == 1:
                    if temp == 2 or temp == 3:
                        new_grid[i][j] = 1
                else:
                    if temp == 3:
                        new_grid[i][j] = 1
        return new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
