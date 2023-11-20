# Square App. Version 2.0

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, StringProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.graphics import Color, Ellipse
from math import atan2, cos, pi, sin
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')
Config.write()


global self_square
self_square = ObjectProperty()

class Square(Widget):
  touch_x = NumericProperty()
  touch_y = NumericProperty()

  a_coord = NumericProperty(0)
  b_coord = NumericProperty(0)
  c_coord = NumericProperty(0)
  d_coord = NumericProperty(0)
  e_coord = NumericProperty(0)
  f_coord = NumericProperty(0)
  a_coord_str = StringProperty('')

  last_touch_x = NumericProperty(1)
  last_touch_y = NumericProperty(1)
  last_e_x_coord = NumericProperty(1)
  last_e_y_coord = NumericProperty(1)
  last_f_x_coord = NumericProperty(1)
  last_f_y_coord = NumericProperty(1)

  p1_x = NumericProperty(130)
  p1_y = NumericProperty(200)
  square_side = NumericProperty(500)
  d = NumericProperty(10)

  def update(self, dt):
    pass

  def remove_last(self, last_touch_x, last_touch_y):
    with self.canvas:
      Color(0, 0, 0)
      Ellipse(pos=(last_touch_x - self.d / 2, last_touch_y - self.d / 2), size=(self.d, self.d))

  def draw_new(self, touch_x, touch_y):
    with self.canvas:
      Color(0.5, 1, 1)
      Ellipse(pos=(touch_x - self.d / 2, touch_y - self.d / 2), size=(self.d, self.d))

  def last_save(self):
    self.last_touch_x = self.touch_x
    self.last_touch_y = self.touch_y

  def angle_between_lines(self, p1, p2, p3):
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    angle = atan2(v2[1], v2[0]) - atan2(v1[1], v1[0])
    return angle

  def draw_coord(self, touch_x, touch_y):
    with self.canvas:
      Color(1, 0, 0)
      Ellipse(pos=(touch_x - self.d / 2, touch_y - self.d / 2), size=(self.d, self.d))

  def calc_coord(self):
    self.a_coord = (self.touch_x - self.p1_x) * 100 / self.square_side
    self.remove_last(self.last_touch_x, self.p1_y)
    self.draw_coord(self.touch_x, self.p1_y)
    
    self.b_coord = (self.touch_y - self.p1_y) * 100 / self.square_side
    self.remove_last(self.p1_x, self.last_touch_y)
    self.draw_coord(self.p1_x, self.touch_y)
    
    self.c_coord = 100 - self.a_coord
    self.remove_last(self.last_touch_x, self.p1_y + self.square_side)
    self.draw_coord(self.touch_x, self.p1_y + self.square_side)
    
    self.d_coord = 100 - self.b_coord
    self.remove_last(self.p1_x + self.square_side, self.last_touch_y)
    self.draw_coord(self.p1_x + self.square_side, self.touch_y)

    distance_gipot_e = Vector(self.p1_x,self.p1_y + self.square_side).distance((self.touch_x, self.touch_y))
    distance_e = Vector(self.p1_x, self.p1_y + self.square_side).distance((self.p1_x + self.square_side, self.p1_y))
    p1 = (self.touch_x, self.touch_y)
    p2 = (self.p1_x, self.p1_y + self.square_side) # вершина угла
    p3 = (self.p1_x + self.square_side, self.p1_y)
    ang = self.angle_between_lines(p1,p2, p3)
    e_prom = abs(cos(ang) * distance_gipot_e)
    self.e_coord = e_prom * 100 / distance_e

    e_x_coord = e_prom * cos(45*pi/180) + self.p1_x
    e_y_coord = (self.p1_y + self.square_side) - e_prom * sin(45*pi/180)
    self.remove_last(self.last_e_x_coord, self.last_e_y_coord)
    self.draw_coord(e_x_coord, e_y_coord)
    self.last_e_x_coord = e_x_coord
    self.last_e_y_coord = e_y_coord
    
    # вычисляем f_coord
    distance_gipot_f = Vector(self.p1_x + self.square_side, self.p1_y + self.square_side).distance((self.touch_x, self.touch_y))
    distance_f = Vector(self.p1_x + self.square_side, self.p1_y + self.square_side).distance((self.p1_x, self.p1_y))
    p1 = (self.touch_x, self.touch_y)
    p2 = (self.p1_x + self.square_side, self.p1_y + self.square_side) # вершина угла
    p3 = (self.p1_x, self.p1_y)
    ang_f = self.angle_between_lines(p1,p2, p3)
    f_prom = abs(cos(ang_f) * distance_gipot_f)
    self.f_coord = f_prom * 100 / distance_f

    f_x_coord = (self.p1_x + self.square_side) - f_prom * cos(45*pi/180)
    f_y_coord = (self.p1_y + self.square_side) - f_prom * sin(45*pi/180)
    self.remove_last(self.last_f_x_coord, self.last_f_y_coord)
    self.draw_coord(f_x_coord, f_y_coord)
    self.last_f_x_coord = f_x_coord
    self.last_f_y_coord = f_y_coord

  def is_point_square(self):
    if ( (self.touch_x < self.p1_x) or
         (self.touch_x > (self.p1_x + self.square_side)) or
         (self.touch_y < self.p1_y) or
          self.touch_y > (self.p1_y + self.square_side) ):
      return False
    else:
      return True

  def draw_up(self):
    if self.touch_y > (self.p1_y + self.square_side-5):
      return
    self.remove_last(self.last_touch_x, self.last_touch_y)
    self.touch_y += 10
    self.draw_new(self.touch_x, self.touch_y)
    self.calc_coord()
    self.last_save()

  def draw_down(self):
    if self.touch_y < self.p1_y + 5:
      return
    self.remove_last(self.last_touch_x, self.last_touch_y)
    self.touch_y -= 10
    self.draw_new(self.touch_x, self.touch_y)
    self.calc_coord()
    self.last_save()

  def draw_left(self):
    if self.touch_x < self.p1_x + 5:
      return
    self.remove_last(self.last_touch_x, self.last_touch_y)
    self.touch_x -= 10
    self.draw_new(self.touch_x, self.touch_y)
    self.calc_coord()
    self.last_save()

  def draw_right(self):
    if self.touch_x > (self.p1_x + self.square_side - 10):
      return
    self.remove_last(self.last_touch_x, self.last_touch_y)
    self.touch_x += 10
    self.draw_new(self.touch_x, self.touch_y)
    self.calc_coord()
    self.last_save()

  def on_touch_down(self, touch):
    self.touch_x = touch.x
    self.touch_y = touch.y
    if not self.is_point_square():
      return
    self.remove_last(self.last_touch_x, self.last_touch_y)
    self.calc_coord()
    self.draw_new(self.touch_x, self.touch_y)
    self.last_save()

  def __init__(self, **kwargs):
    super(Square, self).__init__(**kwargs)
    global self_square
    self_square = self


class Buttons(Widget):
  global self_square
  
  def up(self):
    print('up button pressed')
    self_square.draw_up()
  
  def down(self):
    print('down button pressed')
    self_square.draw_down()

  def left(self):
    print('left button pressed')
    self_square.draw_left()

  def right(self):
    print('right button pressed')
    self_square.draw_right()

class Labels(Widget):
  pass
  
class SquareApp(App):
  def build(self):
      parent = Widget()
      self.sq = Square()
      self.but = Buttons()
      parent.add_widget(self.sq)
      parent.add_widget(self.but)
      return parent


if __name__ == '__main__':
  SquareApp().run()