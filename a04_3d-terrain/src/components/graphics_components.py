import numpy as np

class Texture2D:
    def __init__(self, texture):
        self.texture = texture


class ParticleEmitter:
    def __init__(self, sprite_sheet, life_time=10.0, emitting=True, emit_interval=1.0, max_particles=10, sprite_choices=None):
        self.sprite_sheet = sprite_sheet
        self.max_particles = max_particles
        self.particle_count = 0
        self.life_time = life_time
        self.emitting = emitting
        self.emit_interval = emit_interval
        self.emit_timer = 0.0

        if (sprite_choices is not None):
            self.sprite_choices = sprite_choices
        else:
            self.sprite_choices = np.arange(sprite_sheet.rows * sprite_sheet.columns)

        self.data_emit_time = []
        self.data_emit_position = []
        self.data_sprite_incices = []


class SpriteSheet:
    def __init__(self, texture, rows, columns):
        self.texture = texture
        self.rows = rows
        self.columns = columns