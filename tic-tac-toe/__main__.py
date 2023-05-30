import os
import sys
import argparse
import pickle as p
from curses import wrapper
from game import Game
from field import new_field, game_position_str


def get_params():
    """
    Функция для считывания параметров игры с консоли.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-load", action="store_true",
                        help="to continue last saved game")
    parser.add_argument("-size", nargs=2, type=int, default=[3, 3],
                        help="choose field size",)
    parser.add_argument("-player", choices=[1, 2], type=int, default=1,
                        help="start as player 1 or player 2")

    my_args = parser.parse_args()
    return my_args


def main(screen):
    if use_saved_files and os.path.isfile("gamesave.bin"):
        # Загрузить старую игру
        f = open("gamesave.bin", "rb")
        game = p.load(f)
        f.close()
    else:
        # Создать новую игру.
        game = Game(new_field(size_x, size_y), player_symbol, opponent_symbol)
        game.prepare_field()

    while not game.ending():
        title_str = "+-----------------+\n" \
                    "| TIC - TAC - TOE |\n" \
                    "+-----------------+\n\n"

        instructions_str = "Instructions:\n"\
                           "Press w, a, s, d to move cursor.\n"\
                           "Press e to change symbol.\n"\
                           "Press c to save game.\n"\
                           "Press r to restart game with current field size.\n"\
                           "Press q to quit.\n"

        # Обновление экрана + проверка размера терминала.
        screen.clear()
        try:
            screen.addstr(title_str + game_position_str(game) + instructions_str + '\n')
        except:
            screen.clear()
            screen.addstr("Please, make your terminal larger\nor\n"
                          "use smaller field sizes.\n\n"
                          "Press any button to quit and try again.")
            screen.getch()
            return

        ch = screen.getch()
        if ch == ord("q"):
            # Выход из игры
            return

        elif ch == ord("r"):
            # Рестарт игры
            game = Game(new_field(size_x, size_y), player_symbol, opponent_symbol)
            game.prepare_field()

        elif ch == ord("c"):
            # Сохранение игры
            f = open("gamesave.bin", "wb")
            p.dump(game, f)
            f.close()

        elif ch == ord("e"):
            # Изменение символа, на который указывает курсор
            if game.player_symbol_changed() and not game.ending():
                game.computer_symbol_changed()

        # Управление курсором
        elif ch == ord("w"):
            if game.position[0] > 0:
                game.position[0] -= 1

        elif ch == ord("a"):
            if game.position[1] > 0:
                game.position[1] -= 1

        elif ch == ord("s"):
            if game.position[0] < game.height - 1:
                game.position[0] += 1

        elif ch == ord("d"):
            if game.position[1] < game.width - 1:
                game.position[1] += 1

        # Обновление экрана
        screen.clear()
        screen.addstr(title_str + game_position_str(game) + instructions_str + '\n')

    # Определение победителя
    result = ""
    if game.winner is None:
        result = "It's a draw! :/\n" \
                 "Press any button to quit."
    elif game.winner == game.player_symbol:
        result = "Congratulations, you won!\n" \
                 "Press any button to quit."
    elif game.winner == game.opponent_symbol:
        result = "Unfortunately, you lost.\n" \
                 "Press any button to quit."

    screen.addstr(result)
    screen.getch()


if __name__ == "__main__":
    # Считывание параметров игры
    args = get_params()

    # Задание параметров
    size_x = args.size[0]  # Длина игрового поля
    size_y = args.size[1]  # Ширина игрового поля
    player_symbol = 'x' if args.player == 1 else 'o'
    opponent_symbol = 'o' if args.player == 1 else 'x'
    use_saved_files = args.load

    # Проверка введенных значений размера поля
    if not((0 < size_x < 100) and (0 < size_y < 100)):
        print("Please use integers in range 2 to 50 for field size.")
        sys.exit()

    # Запуск
    wrapper(main)
