class Ball:
    def __init__(self, pos, rad, vel):
        self.pos = pos
        self.rad = rad

        self.vel = vel

        self.selected = False

    def update(self, dt):
        self.pos += self.vel * dt