import curses


class CursesForm:

    def __init__(self, parent_window, y, x, prompt):
        self.x = x + len(prompt)
        self.y = y
        self.parent_window = parent_window
        self.prompt = prompt
        parent_window.move(y, x)
        parent_window.addstr(prompt)
        parent_window.refresh()
        self.value = ''

    def addch(self, c):
        self.parent_window.addstr(c)

    def interact(self, c):
        if c == 127:  # backspace
            if len(self.value) > 0:
                self.x -= 1
                self.parent_window.move(self.y, self.x)
                self.parent_window.addstr(' ')
                self.parent_window.move(self.y, self.x)
                self.value = self.value[:-1]
        else:
            c = chr(c)
            self.value += c
            self.parent_window.move(self.y, self.x)
            self.addch(c)
            self.parent_window.refresh()
            self.x += 1


class SubmitForm(CursesForm):

    def __init__(self, parent_window, y, x, prompt):
        super(SubmitForm, self).__init__(parent_window, y, x, prompt)

    def interact(self, c):
        if c == 10:  # enter
            return True
        return False

class PasswordForm(CursesForm):

    def __init__(self, parent_window, y, x, prompt):
        super(PasswordForm, self).__init__(parent_window, y, x, prompt)

    def addch(self, c):
        self.parent_window.addstr('*')
