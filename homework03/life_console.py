from time import sleep

import curses

from life import GameOfLife
from ui import UI

BORDER_PAIR = 1
CELL_PAIR = 2

class Console(UI):
    def __init__(self, life: GameOfLife, speed: int = 10) -> None:
        super().__init__(life)
        self.speed = speed
        self.cell_size = 2
        self.top_space = 5

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        # асчет координат начала рамки
        t = (screen.getmaxyx()[0] - self.life.cols * self.cell_size - self.top_space - 1) // 2 + self.top_space
        l = (screen.getmaxyx()[1] - self.life.rows * self.cell_size * 2 - 1) // 2
        # Расчет координат конца рамки
        b = t + 1 + self.cell_size * self.life.rows
        r = l + 1 + self.cell_size * self.life.cols * 2
        # Атрибуты консоли для рисования рамки
        attrs = curses.color_pair(BORDER_PAIR) | curses.A_BOLD | curses.A_REVERSE
        # Подключаем атрибуты
        screen.attron(attrs)
        # Рисуем верхнюю и нижнюю рамки
        for i in range(l, r + 1):
            screen.addch(t, i, ' ')
            screen.addch(b, i, ' ')
        # Рисуем боковые рамки
        for j in range(t, b + 1):
            screen.addch(j, l, ' ')
            screen.addch(j, r, ' ')
            screen.addch(j, l - 1, ' ')
            screen.addch(j, r + 1, ' ')
        # Выключаем атрибуты
        screen.attroff(attrs)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        # Расчет координат начала рамки
        t = (screen.getmaxyx()[0] - self.life.cols * self.cell_size - self.top_space) // 2 + self.top_space
        l = (screen.getmaxyx()[1] - self.life.rows * self.cell_size * 2) // 2 + 1
        # Атрибуты консоли для рисования клетки
        attrs = curses.color_pair(CELL_PAIR) | curses.A_BOLD | curses.A_REVERSE
        # Подключаем атрибуты
        screen.attron(attrs)
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    for k in range(self.cell_size):
                        for p in range(self.cell_size * 2):
                            screen.addch(t + self.cell_size * i + k, l + self.cell_size * j * 2 + p, ' ')
        # Выключаем атрибуты
        screen.attroff(attrs)

    def run(self) -> None:
        # Инициализация графики
        screen = curses.initscr()
        # Удаляем курсор
        curses.curs_set(0)
        # Заполняем палитры
        curses.start_color()
        curses.init_pair(BORDER_PAIR, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        curses.init_pair(CELL_PAIR, curses.COLOR_GREEN, curses.COLOR_GREEN)

        running = True
        while running:
            # Надо что-нибудь почистить
            screen.clear()
            # Напечатаем название
            hello_msg = 'Game of Life'
            screen.addstr(1, (screen.getmaxyx()[1] - len(hello_msg)) // 2, hello_msg)
            # Отрисуем поле
            self.draw_borders(screen)
            # Отрисуем клетки
            self.draw_grid(screen)
            #ледующее поколение
            self.life.step()

            # Обновим экранчик
            screen.refresh()

            if not self.life.is_changing:
                # Игра закончена, напишем об этом и выйдем
                end_msg = 'The end. Good bye!'
                screen.addstr(3, (screen.getmaxyx()[1] - len(end_msg)) // 2, end_msg)
                screen.getch()
                running = False

            sleep(self.speed / 60)

        curses.endwin()

if __name__ == '__main__':
    life = GameOfLife((10, 10))
    gui = Console(life)
    gui.run()
