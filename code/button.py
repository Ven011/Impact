"""Button class for screens"""

class Button:
    def __init__(self, screen, button_name, x0, y0, x1, y1, callback):
        self.my_screen = screen
        self.my_name = button_name
        self.area = [x0, y0, x1, y1]  # [x0, y0] = top-left, [x1, y1] = bottom-right
        self.callback = callback

    def check_if_pressed(self, press_x, press_y):
        # check if the press is within my area
        if (self.area[0] <= press_x <= self.area[2]) and (self.area[1] <= press_y <= self.area[3]):
            # run the callback
            self.callback()

