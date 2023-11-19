# Square App. Version 2.0

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, StringProperty, ListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import math
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
  #p1_y = NumericProperty(200)

  def update(self, dt):
    pass

  def remove_last(self, last_touch_x, last_touch_y):
    with self.canvas:
      Color(0, 0, 0)
      d = 20.
      Ellipse(pos=(last_touch_x - d / 2, last_touch_y - d / 2), size=(d, d))

  def draw_new(self, touch_x, touch_y):
    print('draw new.')
    print('touch_x: ', round(touch_x))
    print('touch_y:', round(touch_y))
    with self.canvas:
      Color(0.5, 1, 1)
      d = 20.
      Ellipse(pos=(touch_x - d / 2, touch_y - d / 2), size=(d, d))

  def last_save(self):
    self.last_touch_x = self.touch_x
    self.last_touch_y = self.touch_y

  def angle_between_lines(self, p1, p2, p3):
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    angle = math.atan2(v2[1], v2[0]) - math.atan2(v1[1], v1[0])
    #angle = abs(angle)
    #angle = math.degrees(angle)%180
    # если нужен острый угол
    #return min(180 - angle, angle)
    return angle

  def draw_coord(self, touch_x, touch_y):
    print('draw coord.')
    print('touch_x: ', round(touch_x))
    print('touch_y:', round(touch_y))
    with self.canvas:
      Color(1, 0, 0)
      d = 20.
      Ellipse(pos=(touch_x - d / 2, touch_y - d / 2), size=(d, d))

  def calc_coord(self):
    print('Вычисляем координаты')
    self.a_coord = (self.touch_x - 90) * 100 / (980 - 90)
    self.remove_last(self.last_touch_x, 1005)
    self.draw_coord(self.touch_x, 1005)
    
    self.b_coord = (self.touch_y - 1000) * 100 / (1895 - 1000)
    self.remove_last(90, self.last_touch_y)
    self.draw_coord(90, self.touch_y)
    
    self.c_coord = 100 - self.a_coord
    self.remove_last(self.last_touch_x, 1895)
    self.draw_coord(self.touch_x, 1895)
    
    self.d_coord = 100 - self.b_coord
    self.remove_last(980, self.last_touch_y)
    self.draw_coord(980, self.touch_y)
    #print('a:', self.a_coord, '   b:', self.b_coord)
    #print('c:', self.c_coord, '   d:', self.d_coord)
    
    # неправильно работает
    #angle_dot = Vector(980, 1895).angle((self.touch_x, self.touch_y))
    #print('angle:', round(angle_dot))
    
    # вычисляем e_coord
    distance_gipot_e = Vector(90,1895).distance((self.touch_x, self.touch_y))
    distance_e = Vector(90,1895).distance((980, 1005))
    #print('гипотинуза:', round(distance_gipot_e))
    p1 = (self.touch_x, self.touch_y)
    p2 = (93, 1895) # вершина угла
    p3 = (980, 1005)
    ang = self.angle_between_lines(p1,p2, p3)
    #print("угол из функции:", round(ang, 1))
    e_prom = abs(math.cos(ang) * distance_gipot_e)
    self.e_coord = e_prom * 100 / distance_e
    #self.e_coord = abs(self.e_coord)
    #print('e_coord: ', round(self.e_coord))
    
    # отрисовка e_coord
    e_x_coord = e_prom * math.cos(45*math.pi/180) + 90
    e_y_coord = 1895 - e_prom * math.sin(45*math.pi/180)
    self.remove_last(self.last_e_x_coord, self.last_e_y_coord)
    self.draw_coord(e_x_coord, e_y_coord)
    self.last_e_x_coord = e_x_coord
    self.last_e_y_coord = e_y_coord
    
    # вычисляем f_coord
    distance_gipot_f = Vector(980,1895).distance((self.touch_x, self.touch_y))
    distance_f = Vector(980,1895).distance((90, 1005))
    #print('гипотинуза f:', round(distance_gipot_f))
    p1 = (self.touch_x, self.touch_y)
    p2 = (980, 1895) # вершина угла
    p3 = (90, 1005)
    ang_f = self.angle_between_lines(p1,p2, p3)
    #print("угол из функции:", round(ang_f, 1))
    f_prom = abs(math.cos(ang_f) * distance_gipot_f)
    self.f_coord = f_prom * 100 / distance_f
    #print('f_coord: ', round(self.f_coord))
    
    # отрисовка f_cood
    f_x_coord = 980 - f_prom * math.cos(45*math.pi/180)
    f_y_coord = 1895 - f_prom * math.sin(45*math.pi/180)
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
    print('draw_up')
    #print('touch_x:', round(self.touch_x))
    #print('touch_y:', round(self.touch_y))
    if self.touch_y > 1890:
      return
    self.remove_last(self.last_touch_x, self.last_touch_y)
    self.touch_y += 10
    self.draw_new(self.touch_x, self.touch_y)
    self.calc_coord()
    self.last_save()

  def draw_down(self):
    print('draw_down')
    #print('touch_x:', self.touch_x)
    #print('touch_y:', self.touch_y)
    if self.touch_y < 1005:
      return
    self.remove_last(self.last_touch_x, self.last_touch_y)
    self.touch_y -= 10
    self.draw_new(self.touch_x, self.touch_y)
    self.calc_coord()
    self.last_save()

  def draw_left(self):
    print('draw_left')
    #print('touch_x:', self.touch_x)
    #print('touch_y:', self.touch_y)
    if self.touch_x < 95:
      return
    self.remove_last(self.last_touch_x, self.last_touch_y)
    self.touch_x -= 10
    self.draw_new(self.touch_x, self.touch_y)
    self.calc_coord()
    self.last_save()

  def draw_right(self):
    print('draw_right')
    #print('touch_x:', self.touch_x)
    #print('touch_y:', self.touch_y)
    if self.touch_x > 975:
      return
    self.remove_last(self.last_touch_x, self.last_touch_y)
    self.touch_x += 10
    self.draw_new(self.touch_x, self.touch_y)
    self.calc_coord()
    self.last_save()

  def on_touch_down(self, touch):
    print('touch_down')
    #print('self.width', self.width)
    #print('self.height', self.height)
    #print('self.center', self.center)
    #print('self.pos', self.pos)
    #print('self.size', self.size)
    #if not (touch.x < 95 or touch.x > 975 or touch.y < 1005 or touch.y > 1890):
    self.touch_x = touch.x
    self.touch_y = touch.y
    print('self.touch_x: ', round(self.touch_x), 'self.touch_y:', round(self.touch_y))
    # точка в квадрате?
    if not self.is_point_square():
      return
    # зачеркиваем старую точку
    self.remove_last(self.last_touch_x, self.last_touch_y)
    # вычисляем координаты
    self.calc_coord()
    # рисуем новую точку
    self.draw_new(self.touch_x, self.touch_y)
    # сохраняем прошедшую точку
    self.last_save()

  def __init__(self, **kwargs):
    super(Square, self).__init__(**kwargs)
    global self_square
    self_square = self


#     if touch.x < self.width / 3:
#            self.player1.center_y = touch.y
#     if touch.x > self.width - self.width / 3:
#            self.player2.center_y = touch.y


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
      #Clock.schedule_interval(self.sq.update, 1.0 / 60.0)
      return parent


if __name__ == '__main__':
  SquareApp().run()