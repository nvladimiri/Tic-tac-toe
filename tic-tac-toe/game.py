from random import randint


class Game:
    def __init__(self, field, player_symbol, opponent_symbol):
        self.field = field
        self.player_symbol = player_symbol
        self.opponent_symbol = opponent_symbol
        self.winner = None
        self.height = len(field)
        self.width = len(field[0])
        self.position = [0, 0]  # Положение курсора

    def player_symbol_changed(self):
        """
        Возвращает True и меняет символ на поле,
        если на текущая позиция пуста
        Возвращает False и не менят символа на поле,
        в противном случае.
        """
        if self.field[self.position[0]][self.position[1]] == '□':
            self.field[self.position[0]][self.position[1]] = self.player_symbol
            return True
        return False

    def computer_symbol_changed(self):
        """
        Компьютер ищет любое рандомное свободное поле
        и ставит туда свой симол.
        """
        random_position = [randint(0, self.height - 1), randint(0, self.width - 1)]
        while self.field[random_position[0]][random_position[1]] != '□':
            random_position = [randint(0, self.height - 1), randint(0, self.width - 1)]
        self.field[random_position[0]][random_position[1]] = self.opponent_symbol
        return

    def prepare_field(self):
        """
        В случае, когда игрок ходит вторым,
        первый ход делает компьютер, ищя любое
        рандомное поле и ставя на него свой символ.
        """
        if self.opponent_symbol == 'x':
            random_position = [randint(0, self.height - 1), randint(0, self.width - 1)]
            self.field[random_position[0]][random_position[1]] = self.opponent_symbol
        return

    def ending(self):
        """
        Функция проверяет закончена ли игра,
        а также определяет победителя, вписывая его символ
        в поле self.winner в случае победы / поражения,
        или остовляя там значение None в случае ничьи.

        Возвращает True если игра окончена,
        в противном случае возвращает False.
        """
        # Есть ли заполненные строка/столбец/диагональ
        full_column = full_row = full_diagonal = False

        # Проверка выигрыша по строкам
        for row in self.field:
            if row[1:] == row[:-1] and row[0] != '□':
                full_row = True
                self.winner = row[0]

        # Проверка выигрыша по столбцам
        for i in range(self.width):
            curr_col = []
            for j in range(self.height):
                curr_col.append(self.field[j][i])
            if curr_col[1:] == curr_col[:-1] and curr_col[0] != '□':
                full_column = True
                self.winner = curr_col[0]

        # Проверка выигрыша по диагоналям
        if self.width >= self.height:
            # Алгоритм для первого вида прямоугольных полей
            for i in range(self.width - self.height + 1):
                left_diag = []
                for j in range(self.height):
                    left_diag.append(self.field[j][i + j])
                if left_diag[1:] == left_diag[:-1] and left_diag[0] != '□':
                    full_diagonal = True
                    self.winner = left_diag[0]

            for i in range(self.width - self.height + 1):
                right_diag = []
                for j in range(self.height):
                    right_diag.append(self.field[j][i + self.height - 1 - j])
                if right_diag[1:] == right_diag[:-1] and right_diag[0] != '□':
                    full_diagonal = True
                    self.winner = right_diag[0]
        else:
            # Алгоритм для второго вида прямоугольных полей
            for i in range(self.height - self.width + 1):
                left_diag = []
                for j in range(self.width):
                    left_diag.append(self.field[i + j][j])
                if left_diag[1:] == left_diag[:-1] and left_diag[0] != '□':
                    full_diagonal = True
                    self.winner = left_diag[0]

            for i in range(self.height - self.width + 1):
                right_diag = []
                for j in range(self.width):
                    right_diag.append(self.field[-i + self.height - 1 - j][j])
                if right_diag[1:] == right_diag[:-1] and right_diag[0] != '□':
                    full_diagonal = True
                    self.winner = right_diag[0]

        if full_diagonal or full_column or full_row:
            return True

        # Проверка на ничью
        all_symbols = set()
        for row in self.field:
            all_symbols = all_symbols | set(row)
        if '□' not in all_symbols:
            return True

        return False
