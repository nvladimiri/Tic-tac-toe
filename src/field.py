def new_field(width, height):
    """
    Функция создает чистое игровое поле
    размера width * height
    """
    return [['□' for i in range(width)] for j in range(height)]


def game_position_str(curr_game):
    """
    Функция получает на вход объект типа Game.

    Возвращает строку, отображающую
    состояния поля игры в данный момент врмемени,
    а также текущее положение курсора игрока.
    """
    i_pos = curr_game.position[0]
    j_pos = curr_game.position[1]
    answer = ""

    for i in range(curr_game.height):
        for j in range(curr_game.width):
            if i == i_pos and j == j_pos:
                answer += curr_game.field[i][j] + " ← "
            else:
                answer += curr_game.field[i][j] + "   "
        answer += '\n\n'
    return answer
