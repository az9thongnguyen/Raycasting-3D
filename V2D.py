import math


class V2D:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        pass

    def __str__(self) -> str:
        return str((self.x, self.y))

    def __add__(self, o):
        return V2D(self.x+o.x, self.y+o.y)

    def __iadd__(self, i):
        self.x += i
        self.y += i
        return self

    def __sub__(self, o):
        return V2D(self.x-o.x, self.y-o.y)

    def __isub__(self, i):
        self.x -= i
        self.y -= i
        return self

    def __mul__(self, o):
        return self.x * o.x + self.y * o.y

    def __imul__(self, i):
        self.x *= i
        self.y *= i
        return self

    def __neg__(self):
        return V2D(-self.x, -self.y)

    def rotateInRad(self, angle):
        newAngle = self.getAngleRad() + angle
        m = self.magnitudes()
        self.x = m * math.cos(newAngle)
        self.y = m * math.sin(newAngle)
        pass

    def getAngleRad(self):
        res = math.asin(self.sin())
        if self.cos() < 0:
            res = math.pi - res
        elif self.sin() < 0:
            res = 2*math.pi + res
        return res

    def setAngleRad(self, angle):
        m = self.magnitudes()
        self.x = m * math.cos(angle)
        self.y = m * math.sin(angle)

    def magnitudes(self):
        return math.sqrt(self.x**2 + self.y**2)

    def sin(self):
        if self.magnitudes() == 0:
            return 0
        return self.y / self.magnitudes()

    def cos(self):
        if self.magnitudes() == 0:
            return 0
        return self.x / self.magnitudes()
