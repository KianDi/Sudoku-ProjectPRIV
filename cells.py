class Cell:

    sketched_value = 0
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        if self.value == 0 and self.sketched_value != 0:
            print(self.sketched_value)
        elif self.value != 0:
            print(self.value)



