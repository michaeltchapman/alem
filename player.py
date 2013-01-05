from panda3d.core import Point2


class Player():
    left_move = False
    right_move = False
    up_move = False
    down_move = False

    move_speed = 0.1

    def __init__(self, app):
        self.position = Point2(0,0)
        self.health = 100
        self.model = app.loader.loadModel('models/box')
        self.model.setScale(0.5)
        self.model.reparentTo(app.render)
        self.model.setPos(self.position.x, self.position.y, 0)

    def update(self, timer):
        if self.left_move:
            self.position.x = self.position.x - self.move_speed
        if self.right_move:
            self.position.x = self.position.x + self.move_speed
        if self.up_move:
            self.position.y = self.position.y + self.move_speed
        if self.down_move:
            self.position.y = self.position.y - self.move_speed
        print self.position
        self.model.setPos(self.position.x, self.position.y, 0)

        return

    def move_left(self, switch):
        self.left_move = switch

    def move_right(self, switch):
        self.right_move = switch

    def move_up(self, switch):
        self.up_move = switch

    def move_down(self, switch):
        self.down_move = switch




