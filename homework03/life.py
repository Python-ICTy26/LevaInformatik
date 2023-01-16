import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного пол
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if not randomize:
            return [[0 for _ in range(self.cols)] for __ in range(self.rows)]
        return [[random.randint(0, 1) for _ in range(self.cols)] for __ in range(self.rows)]

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
        if top >= 0 and top < self.rows and left >= 0 and left < self.cols:
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
                    res.append(self.curr_generation[top][left])

        return res

    def get_next_generation(self) -> Grid:
        new_grid = [[0 for _ in range(self.cols)] for __ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                temp = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 1:
                    new_grid[i][j] = 1 if temp in [2, 3] else 0
                else:
                    new_grid[i][j] = 1 if temp == 3 else 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations <= self.generations:  # type: ignore
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.prev_generation[i][j] != self.curr_generation[i][j]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        a = filename.read_text().splitlines()
        b = []
        m = 0
        n = 0
        for i in range(len(a)):
            x = []
            for j in range(0, len(a[i])):
                if a[i][j] == "1":
                    x.append(1)
                else:
                    x.append(0)
                n += 1
            b.append(x)
            m += 1
        game = GameOfLife((m, n))
        game.curr_generation = b
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                filename.write_text(f"{self.curr_generation[i][j]}")
            filename.write_text("\n")
