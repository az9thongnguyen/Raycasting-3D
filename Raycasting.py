import tkinter as tk
import math
from V2D import *

# author Thongnguyen

FOV = math.pi/3
ROV = 120
DISTANCE = 450
ARROW = 10

BACKGROUND_COLOR = "black"
PLAYER_COLOR = "red"
RAY_COLOR = "blue"
BOX_COLOR = "white"

RAW_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Raycasting:
    def __init__(self, root) -> None:

        # Root
        self.root = root
        self.root.bind('<KeyPress>', self.onKeyPress)
        self.root.title("Raycasting")

        # Map 2D
        self.map2d = tk.Canvas(self.root, width=500,
                               height=500, bg=BACKGROUND_COLOR)
        self.map2d.pack(side=tk.LEFT, pady=5)

        self.box_size = int(self.map2d['width']) / len(RAW_MAP)

        # Player
        self.p_pos = V2D(275, 288)
        self.p_dir = V2D(-0.5, 1)
        self.p_id = None
        self.p_ray = []

        # Map 3D

        self.map3d = tk.Canvas(self.root, width=500, height=500, bg='blue')
        self.map3d.pack(side=tk.RIGHT, pady=5)

        self.map3d.create_rectangle(0, 0, 500, 200, fill='grey')
        self.map3d.create_rectangle(0, 200, 500, 500, fill='black')

        self.wall3D = []

        self.__init__map()

        pass

    def __init__map(self):
        # Draw raw map:
        for ri, row in enumerate(RAW_MAP):
            for ci, box in enumerate(row):
                x = ci*self.box_size
                y = ri*self.box_size
                if box == 1:
                    self.map2d.create_rectangle(
                        x, y, x+self.box_size, y+self.box_size, fill=BOX_COLOR, outline='grey')
                else:
                    self.map2d.create_rectangle(
                        x, y, x+self.box_size, y+self.box_size, fill=BACKGROUND_COLOR, outline='grey')

        # Draw ray and wall 3D
        step = FOV/ROV
        dest = V2D(self.p_dir.x, self.p_dir.y)
        dest.rotateInRad(-FOV/2)
        step_w = 500/ROV

        x1, y1 = 500 - step_w, 50
        x2, y2 = 500, 350
        for i in range(ROV):
            # init ray
            self.p_ray.append(self.map2d.create_line(
                self.p_pos.x, self.p_pos.y, self.p_pos.x + dest.x *
                DISTANCE, self.p_pos.y - dest.y*DISTANCE,
                fill=RAY_COLOR))

            dest.rotateInRad(step)

            # init wall
            self.wall3D.append(self.map3d.create_rectangle(
                x1, y1, x2, y2, fill=RAY_COLOR, outline='blue'))
            x1 -= step_w
            x2 -= step_w

        # init player
        self.p_id = self.map2d.create_oval(
            self.p_pos.x-self.box_size/8, self.p_pos.y-self.box_size/8,
            self.p_pos.x+self.box_size/8, self.p_pos.y+self.box_size/8, fill=PLAYER_COLOR)

        self.update_map()

        pass

    def update_map(self):
        # Map 2D
        step = FOV/ROV
        dest = V2D(self.p_dir.x, self.p_dir.y)
        dest.rotateInRad(-FOV/2)
        col_src = int(self.p_pos.x // self.box_size)
        row_src = int(self.p_pos.y // self.box_size)

        # Map 3D
        step_w = 500/ROV
        x1_w, y1_w = 500 - step_w, 50
        x2_w, y2_w = 500, 350

        for i in range(ROV):
            angle = dest.getAngleRad()
            goUp = (0 < angle and angle < math.pi)
            goRight = (math.pi*3/2 < angle or angle < math.pi/2)

            # i will fix this
            if(angle > math.pi/2 and angle < math.pi):
                angle = math.pi - angle
            elif (angle > math.pi and angle < 3*math.pi/2):
                angle = angle - math.pi
            elif(angle > 3*math.pi/2 and angle < 2*math.pi):
                angle = 2*math.pi - angle

            # ======================================================= #

            # Check vertical intersection

            Tan = math.tan(angle)
            z = 0

            if goRight:
                z = (col_src+1)*self.box_size - self.p_pos.x
            else:
                z = self.p_pos.x - col_src*self.box_size

            hor = DISTANCE
            for h in range(10):
                if goUp:
                    yi = int((self.p_pos.y - z*Tan) // self.box_size)
                else:
                    yi = int((self.p_pos.y + z*Tan) // self.box_size)

                if goRight:
                    xi = int((self.p_pos.x + z) // self.box_size)
                else:
                    xi = int((self.p_pos.x - z) // self.box_size)-1

                if xi < 0 or yi < 0 or xi > 9 or yi > 9:
                    break

                if RAW_MAP[yi][xi] == 1:
                    hor = math.sqrt((z**2) + (z*Tan)**2)
                    break
                z += self.box_size

            # ======================================================= #

            # Check horizontal intersection
            Tan = 1/math.tan(angle)
            z = 0
            if goUp:
                z = self.p_pos.y - row_src*self.box_size
            else:
                z = (row_src + 1) * self.box_size - self.p_pos.y
            ver = DISTANCE
            for h in range(10):
                if goRight:
                    xi = int((self.p_pos.x + z*Tan) // self.box_size)
                else:
                    xi = int((self.p_pos.x - z*Tan) // self.box_size)

                if goUp:
                    yi = int((self.p_pos.y - z) // self.box_size) - 1
                else:
                    yi = int((self.p_pos.y + z) // self.box_size)

                if xi < 0 or yi < 0 or xi > 9 or yi > 9:
                    break

                if RAW_MAP[yi][xi] == 1:
                    ver = math.sqrt((z**2) + (z*Tan)**2)
                    break
                z += self.box_size

            # Check distance and render
            dist = min(hor, DISTANCE)
            dist = min(ver, dist)
            self.map2d.coords(self.p_ray[i], self.p_pos.x, self.p_pos.y,
                              self.p_pos.x + dest.cos()*dist, self.p_pos.y - dest.sin()*dist)
            dest.rotateInRad(step)

            # Draw 3D
            ca = self.p_dir.getAngleRad() - dest.getAngleRad()
            temp = dist*math.cos(ca)
            height = 100*300/temp
            if (height > 320):
                height = 320
            y1_w = 225 - height/2
            y2_w = 225 + height/2
            self.map3d.coords(self.wall3D[i], x1_w,
                              y1_w, x2_w, y2_w)

            if(hor > ver):
                self.map3d.itemconfig(self.wall3D[i], fill='#00008B')
            else:
                self.map3d.itemconfig(self.wall3D[i], fill='#0000FF')
            x1_w -= step_w
            x2_w -= step_w

        pass

    def onKeyPress(self, event):
        key = event.keysym
        if key == "a":
            self.p_dir.rotateInRad(math.pi/72)
            self.update_map()
        elif key == "d":
            self.p_dir.rotateInRad(-math.pi/72)
            self.update_map()
        elif key == "w":
            ix = int((self.p_pos.x + self.p_dir.x *
                     (5 + self.box_size/8)) // self.box_size)
            iy = int((self.p_pos.y - self.p_dir.y *
                     (5 + self.box_size/8)) // self.box_size)

            # Hit the wall
            if(RAW_MAP[iy][ix] != 1):
                self.map2d.move(self.p_id, self.p_dir.x*5, -self.p_dir.y*5)
                self.p_pos.x += self.p_dir.x*5
                self.p_pos.y -= self.p_dir.y*5
                self.update_map()
        elif key == "s":
            ix = int((self.p_pos.x - self.p_dir.x *
                     (5 + self.box_size/8)) // self.box_size)
            iy = int((self.p_pos.y + self.p_dir.y *
                     (5 + self.box_size/8)) // self.box_size)
            # Hit the wall
            if(RAW_MAP[iy][ix] != 1):
                self.map2d.move(self.p_id, -self.p_dir.x*5, self.p_dir.y*5)
                self.p_pos.x -= self.p_dir.x*5
                self.p_pos.y += self.p_dir.y*5
                self.update_map()
        pass

    def run(self):
        self.root.mainloop()
