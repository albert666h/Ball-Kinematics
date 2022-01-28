class Ball:
    def __init__(self, pos, vel, mass):
        self.pos = pos
        self.rad = mass

        self.vel = vel
        self.mass = mass

        self.selected = False

    def update(self, dt):
        self.pos += self.vel * dt
