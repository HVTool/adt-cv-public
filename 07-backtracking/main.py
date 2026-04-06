import os
import numpy as np

class SudokuSolver:
    def __init__(self):
        self.field = np.zeros([9, 9], dtype=int)

    def load(self, file_path: str) -> None:

        # list of lists (rows)
        loaded_rows: list[list[int]] = []

        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                values = line.split(";")

                integers = [int(value) for value in values] # převedení načtených hodnot na integer

                # Stejný zápis akorát v nezkrácené podobě
                # integers = []
                # for value in values:
                #     integers.append(int(value))

                loaded_rows.append(integers)

        # convert nested list to numpy array
        self.field = np.array(loaded_rows)

    def check_sequence(self, sequence: np.ndarray) -> bool:
        # Kontroluje zda v dodané sekvenci se nachází duplicity
        # Nula se jako duplicita nepočítá, protože značí prázdnou buňku
        # True === OK
        # False === Not OK

        seen = set()
        for cell in sequence:
            if cell == 0:
                continue
            if cell in seen:
                return False
            seen.add(cell)
        return True


    def check_row(self, row_index: int) -> bool:
        # pomoci řezu matice dodá ke kontrole celý řádek
        row_data = self.field[row_index, :]

        return self.check_sequence(row_data)

    def check_column(self, column_index: int) -> bool:
        # pomoci řezu matice dodá ke kontrole celý sloupec
        col_data = self.field[:, column_index]

        return self.check_sequence(col_data)

    def check_block(self, row_index: int, column_index: int) -> bool:
        # zjištění do kterého bloku daná buňka patří
        row_start = (row_index // 3) * 3
        col_start = (column_index // 3) * 3

        # získání daného bloku (podmatice) dat
        data = self.field[row_start: row_start + 3, col_start: col_start + 3]

        # zploštění podmatice (3x3) na pole (9x1)
        # tvar můžete zjistit pomocí .shape
        flatten_data = data.reshape(-1)

        return self.check_sequence(flatten_data)


    def check_one_cell(self, row_index: int , column_index: int) -> bool:
        valid_row = self.check_row(row_index)
        valid_col = self.check_column(column_index)
        valid_block = self.check_block(row_index, column_index)

        # Metoda vrátí True pouze pokud všechny 3 pravidla sudoku jsou splněna
        return valid_row and valid_col and valid_block

    def get_empty_cell(self) -> tuple[int, int] | None:
        """ Gets the coordinates of the next empty field. """
        for r in range(9):  # nejprve procházíme řádky
            for c in range(9):# poté sloupce
                if self.field[r, c] == 0:
                    return r, c

        return None

    def solve(self) -> bool:
        """ Recursively solves the sudoku. """

        # Zastavovací podmínka
        next_cell = self.get_empty_cell()
        if next_cell is None:
            return True

        r, c = next_cell

        for candidate in range(1, 10):
            self.field[r, c] = candidate # Zkoušení různých kandidátů

            is_valid = self.check_one_cell(r, c) # Je kandidát validní?
            if not is_valid:
                # Pokud není, tak skočím na dalšího kandidáta
                # a ani nebudu zkoušet doplňovat jiné
                # prázdné buňky (spuštěním další úrovně zanoření = rekurze)
                continue

            # Aktuální kandidát je zatím dobrý, zkusím s ním pokračovat dál
            # a doplnit ostatní prázdné buňky
            solved = self.solve()

            if solved:
                # Podařilo se to vyřešit -> chci se postupně vynořit z rekurze a nic dalšího nedělat
                return True

        # Sem se dostanu, pouze pokud další zanoření byli neúspěšné
        # a to znamená, že jsem v úplně slepé uličce -> chci tedy vynulovat co jsem vyplnit a vynořit se
        self.field[r, c] = 0
        return False


def main() -> None:
    sudoku_solver = SudokuSolver() # Vytvoření instance třídy SudokuSolver
    sudoku_solver.load("sudoku.csv") # Do vytvořené instance načtu sudoku ze souboru
    sudoku_solver.solve() # Načtené sudoku nechám vyřešit
    print(sudoku_solver.field) # A pak si ho vypsat

if __name__ == "__main__":
    os.chdir("07-backtracking")
    main()
