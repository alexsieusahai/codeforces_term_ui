import curses

from cursesForms import CursesForm, SubmitForm, PasswordForm
from cursesTable import CursesTable


class CursesInterface:

    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()

    def __draw_window_in_center(self, height, width):
        return curses.newwin(height, width, int((curses.LINES - 1) / 2 - height / 2), int((curses.COLS - 1) / 2 - width / 2))

    def __addstr_at_middle_x(self, window, astr, height):
        (max_y, max_x) = window.getmaxyx()
        window.move(height, int(max_x / 2 - len(astr) / 2))
        window.addstr(astr)

    def login(self):
        self.stdscr.clear()
        login_window_height = 15
        login_window_width = 90
        cursesForms = []
        login_window = self.__draw_window_in_center(login_window_height, login_window_width)
        login_window.keypad(True)
        self.__addstr_at_middle_x(login_window, 'Welcome to Codeforces CLI!', 1)

        emailForm = CursesForm(login_window, int(login_window_height / 5), 3, 'Handle/Email: ')
        cursesForms.append(emailForm)
        pwForm = PasswordForm(login_window, int(2*login_window_height/5), 3, 'Password: ')
        cursesForms.append(pwForm)
        submitForm = SubmitForm(login_window, int(2 * login_window_height / 3), int(login_window_width/2 - 3), 'Submit!')
        cursesForms.append(submitForm)
        cursesForms = cursesForms[::-1]

        login_window.border('|', '|', '-', '-')
        login_window.refresh()
        i = 0
        while True:
            currentForm = cursesForms[i]
            login_window.move(currentForm.y, currentForm.x)
            c = login_window.getch()
            if c == curses.KEY_UP:
                i = (i + 1) % len(cursesForms) 
            elif c == curses.KEY_DOWN:
                i = (i - 1) % len(cursesForms)
            else:
                shouldSubmit = currentForm.interact(c)
                if shouldSubmit:
                    break

        pw = cursesForms[1].value 
        email = cursesForms[2].value

        return {'email': email, 'pw': pw}

    def kill(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def select_problem_flow(self, problems):
        problem_window = curses.newwin(curses.LINES - 1, curses.COLS - 1)
        problem_table = CursesTable(problem_window)
        desiredCols = ['ContestId', 'Category', 'Name', 'Problem Type(s)', 'Submission Accuracy']
        for col in desiredCols:
            problem_table.add_header(col)
        for problem in problems:
            problem_table.add_row(problem)
        desired_problem = problem_table.get_entry_from_user()
        return desired_problem


if __name__ == "__main__":
    ci = CursesInterface()
    creds = ci.login()
    problems = []
    entry_dict = {
         'ContestId': '0',
         'Category': 'A',
         'Name': 'Some Number Theory Problem',
         'Submission Accuracy': '56%'
    }
    for i in range(60):
        entry_dict['ContestId'] = str(i)
        problems.append(entry_dict.copy())
    desired_problem = ci.select_problem_flow(problems)
    ci.kill()
    print(desired_problem)
