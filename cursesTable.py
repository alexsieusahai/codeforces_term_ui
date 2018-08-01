import curses

class CursesTable:

    def __init__(self, table_window):
        self.table_window = table_window
        self.headers = []
        self.rows = []
        self.column_windows = []
        self.top_row = 0
        self.cursor_location = 3
        self.bottom_row = 0
        self.max_rows = table_window.getmaxyx()[0] - 3


    def __draw_header(self, column_window, i):
        column_window.move(1, 2)
        column_window.addstr(self.headers[i])
        column_window.move(2, 1)
        for i in range(column_window.getmaxyx()[1] - 1):
            column_window.addstr('-')


    def __draw_rows(self, column_window, header_index, beginning_dist):
        for i in range(self.top_row, self.bottom_row):
            if i >= len(self.rows):
                break
            row = self.rows[i]
            column_window.move(beginning_dist, 2)
            if self.headers[header_index] in row:
                column_window.addstr(str(row[self.headers[header_index]]))
            beginning_dist += 1


    def add_header(self, header):
        self.headers.append(header)


    def add_row(self, entry_dict):
        if self.bottom_row < self.max_rows:
            self.bottom_row += 1
        self.rows.append(entry_dict)


    def move_to_current_row(self):
        first_window = self.column_windows[0]
        first_window.move(self.cursor_location, 2)
        first_window.refresh()

    
    def move_down(self):
        if self.bottom_row < len(self.rows) - 1:
            self.cursor_location += 1
            if self.cursor_location - 2 > self.max_rows:
                self.cursor_location -= 1
                self.top_row += 1
                self.bottom_row += 1

    def move_up(self):
        self.cursor_location -= 1
        if self.cursor_location - 3 < 0:
            self.cursor_location += 1
            if self.top_row > 0:
                self.top_row -= 1
                self.bottom_row -= 1


    def draw(self):
        self.column_windows = []
        for i in range(len(self.headers)):
            column_window = curses.newwin(
                    0,
                    int((i+1)*self.table_window.getmaxyx()[1]/len(self.headers)),
                    0,
                    int(i*self.table_window.getmaxyx()[1]/len(self.headers))
                    )
            column_window.border('|', ' ', '-', '-', ' ', ' ', ' ', ' ')

            self.__draw_rows(column_window, i, 3)
            column_window.refresh()
            self.column_windows.append(column_window)

            header_window = curses.newwin(
                    3,
                    int((i+1)*self.table_window.getmaxyx()[1]/len(self.headers)),
                    0,
                    int(i*self.table_window.getmaxyx()[1]/len(self.headers))
                    )
            header_window.border()
            header_window.move(1, header_window.getyx()[1] + int(len(self.headers[i])/2))
            header_window.addstr(self.headers[i])
            header_window.refresh()

        self.move_to_current_row()

    
    def get_entry_from_user(self):
        self.draw()
        self.column_windows[0].keypad(True)
        c = self.column_windows[0].getch()

        while c != 10:  # Enter
            if c == ord('j') or c == curses.KEY_DOWN:
                self.move_down()
            if c == ord('k') or c == curses.KEY_UP:
                self.move_up()

            self.draw()
            c = self.column_windows[0].getch()
            self.column_windows[2].addstr(str(c))
            self.column_windows[2].refresh()

        return self.top_row + self.cursor_location - 3


if __name__ == "__main__":
    from cursesInterface import CursesInterface
    ci = CursesInterface()
    table_window = curses.newwin(curses.LINES - 1, curses.COLS - 1)
    table = CursesTable(table_window)
    for col in ['ContestId', 'Category', 'Name', 'Problem Type(s)', 'Submission Accuracy']:
        table.add_header(col)
    entry_dict = {
        'ContestId': '0',
        'Category': 'A',
        'Name': 'Some Number Theory Problem',
        'Submission Accuracy': '56%'
    }
    for i in range(60):
        entry_dict['ContestId'] = str(i)
        table.add_row(entry_dict.copy())

    entry = table.get_entry_from_user()

    ci.kill()
    print(entry)
