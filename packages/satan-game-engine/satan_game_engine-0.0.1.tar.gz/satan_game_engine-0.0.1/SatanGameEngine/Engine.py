import pygame as pg
import sys
import threading

from SatanGameEngine.Colors import *

class Game:
    def __init__(self, width=800, height=600, title="satan's game", fps=60):
        pg.init()
        self.fps = fps
        self.show_fps = False
        self.width = width
        self.height = height
        self.original_title = title
        self.title = self.original_title
        self.window = pg.display.set_mode((self.width, self.height))
        self.display = pg.display
        self.running = True
        self.clock = pg.time.Clock()
        self.dt = 0
        self.objects = []

    def load_image(self, image_path, scale):
        image = pg.image.load(image_path)
        scaled_image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        return scaled_image

    def draw(self, window_color=COLOR.BLACK):
        self.window.fill(window_color)

        for game_object in self.objects:
            game_object.draw()

        pg.display.flip()

    def add_object(self, game_object):
        self.objects.append(game_object)

    def remove_object(self, game_object):
        try:
            self.objects.remove(game_object)
        except ValueError:
            pass

    def move(self, obj, get_new_pos, speed):
        def move_thread():
            obj_pos = (obj.x, obj.y)
            new_pos = get_new_pos()  # Get the initial new position
            distance_x = new_pos[0] - obj_pos[0]
            distance_y = new_pos[1] - obj_pos[1]
            distance_total = max(abs(distance_x), abs(distance_y))

            while distance_total > 0:
                obj_pos = (obj.x, obj.y)
                new_pos = get_new_pos()  # Get the updated new position
                distance_x = new_pos[0] - obj_pos[0]
                distance_y = new_pos[1] - obj_pos[1]
                distance_total = max(abs(distance_x), abs(distance_y))

                if distance_total == 0:
                    break

                distance = min(distance_total, speed * 100 * self.dt)
                distance_ratio = distance / distance_total
                step_x = distance_x * distance_ratio
                step_y = distance_y * distance_ratio
                obj.x += step_x
                obj.y += step_y
                distance_total -= distance

                self.update()
                self.draw()

        thread = threading.Thread(target=move_thread)
        thread.start()


    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False

        for game_object in self.objects:
            game_object.handle_input()
            game_object.update()

        self.dt = self.clock.tick(self.fps) * 0.001
        self.set_fps_display(self.show_fps)

    def set_fps_display(self, value: bool):
        if value:
            self.title = f"{self.original_title} | {self.clock.get_fps():.2f} FPS"
        else:
            self.title = self.original_title

    def run(self):
        while self.running:
            self.update()
            self.draw()
            pg.display.set_caption(self.title)

        pg.quit()
        sys.exit()
