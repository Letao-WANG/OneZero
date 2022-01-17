class Move(object):
    def __init__(self, x_coor, y_coor, value):
        self.x_coor = x_coor
        self.y_coor = y_coor
        self.value = value
        
    def __repr__(self):
        return "x:" + str(self.x_coor) + "y:" + str(self.y_coor) + "v:" + str(self.value)
