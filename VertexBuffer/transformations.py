from NumpyDiego import *
from gl import *

r = Renderer(800,800)

def line(A,B):
    x0, y0, x1, y1 = A.x, A.y , B.x, B.y
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    steep = dy > dx

    if steep:
      x0, y0 = y0, x0
      x1, y1 = y1, x1

      dy = abs(y1 - y0)
      dx = abs(x1 - x0)

    offset = 0
    threshold = 2.5 * dx
    
    # y = mx + b
    if x1 < x0:
      y = y1
      x0, x1 = x1, x0
      y0, y1 = y1, y0
    else:
      y = y0
    points = []
    for x in range(int(x0), int(x1) + 1):
      if steep:
        points.append((y, x))
      else:
        points.append((x, y))

      offset += dy * 2 
      if offset >= threshold:
        y += 1 if y0 < y1 else -1
        threshold += 2 * dx

    for point in points:
      r.point(*point)

points = [
  (200, 200), (400, 200),
  (400, 400), (200, 400)
]


prev_point = V3(*points[-1])
for point in points:
  point = V3(*point)
  line(prev_point, point)
  prev_point = point


r.display()