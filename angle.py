import math
 
def angle_between_lines(p1, p2, p3):
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    angle = math.atan2(v2[1], v2[0]) - math.atan2(v1[1], v1[0])
    angle = math.degrees(angle)%180
    # если нужен острый угол
    # return min(180 - angle, angle)
    return angle

p1 = (198, 1699)
p2 = (90, 1985) # вершина угла
p3 = (980, 1005)
ang = angle_between_lines(p1,p2, p3)
print(ang)