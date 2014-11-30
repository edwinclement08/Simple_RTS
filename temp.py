class ammunition:
    speed = 0
    point_to_decrease = 0

    get_speed = {'bullet', }

    def __init__(self, (x, y), angle, ammunition_type):
        self.start_position = (x, y)
        self.angle = angle
        self.type = ammunition_type
        self.speed =