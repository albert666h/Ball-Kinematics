class Ball:
    def __init__(self, pos, rad, vel, mass):
        self.pos = pos
        self.rad = rad

        self.vel = vel
        self.mass = mass

        self.selected = False

    def update(self, dt):
        self.pos += self.vel * dt
