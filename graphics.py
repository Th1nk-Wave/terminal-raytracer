import sys


class window:
  def __init__(self,id,width,height,backgroundrgb = [28, 35, 51]):
    #initiate variables
    self.width = width
    self.height = height
    self.id = id
    self.bgR = backgroundrgb[0]
    self.bgG = backgroundrgb[1]
    self.bgB = backgroundrgb[2]

    self.objects = {}
    self.texts = {}
    self.toUpdate = [False for i in range(height)]
    self.toRender = [True for i in range(height)]

    self.renderSTR = []
    self.renderSTR_RAW = ""
    self.pixelMap = []
    
    #fill in pixel map
    for y in range(height):
      self.pixelMap.append([])
      for x in range(width):
        self.pixelMap[y].append({
          "color" : backgroundrgb,
          "char" : "  ",
          "data" : []
        })
    #pre update
    for y in self.pixelMap:
      lineSTR = ""
      oldrgb = []
      for x in y:
        rgb = x["color"]
        if rgb == oldrgb:
          lineSTR += x["char"]
        else:
          lineSTR += f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m{x['char']}"
        oldrgb = rgb
      self.renderSTR.append(lineSTR + f"\033[48;2;{self.bgR};{self.bgG};{self.bgB}m\n")

  def update(self):
    for y, needUpdate in enumerate(self.toUpdate):
      if needUpdate:
        lineSTR = ""
        oldrgb = []
        for x in self.pixelMap[y]:
          rgb = x["color"]
          if rgb == oldrgb:
            lineSTR += x["char"]
          else:
            lineSTR += f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m{x['char']}"
          oldrgb = rgb
        self.renderSTR[y] = lineSTR
        self.toUpdate[y] = False

  def render(self):
    for y, needRender in enumerate(self.toRender):
      if needRender:
        sys.stdout.write(f"\033[{y + 1};0H" + self.renderSTR[y])
        self.toRender[y] = False
    sys.stdout.write("\033[" + str(self.height + 1) + ";0H")

  def renderPixel(self,x,y):
    if self.toRender[y]:
      rgb = self.pixelMap[y][x]["color"]
      sys.stdout.write(f"\033[{y + 1};{x*2}H" + f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m{self.pixelMap[y][x]['char']}" + "\033[" + str(self.height + 1) + ";0H")
  
  def clear(self):
    for i, y in enumerate(self.pixelMap):
      self.toRender[i] = True
      self.toUpdate[i] = True
      for x in y:
        x["color"] = [self.bgR,self.bgG,self.bgB]
  
  def plot(self,x,y,color=[0,0,0],char="  ",data=[]):
    self.toUpdate[y] = True
    self.toRender[y] = True

    self.pixelMap[y][x]["color"] = color
    self.pixelMap[y][x]["char"] = char
    self.pixelMap[y][x]["data"] = data

  def line(self,x1,y1,x2,y2,color=[0,0,0],char="  ",data=[]):
    dx = x2 - x1
    dy = y2 - y1
    isSteep = abs(dy) > abs(dx)
    if isSteep:
      x1, y1 = y1, x1
      x2, y2 = y2, x2
    if x2 < x1:
      x1, x2 = x2, x1
      y1, y2 = y2, y1
    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    y = y1
    for x in range(x1, x2 + 1):
      if isSteep:
        self.plot(y,x,color,char,data)
      else:
        self.plot(x,y,color,char,data)
      error -= abs(dy)
      if error < 0:
        y += ystep
        error += dx

  def text(self,id,x,y,text):
    self.toUpdate[y] = True
    self.toRender[y] = True
    groups = [text[i:i+2] for i in range(0, len(text), 2)]
    if len(groups[-1]) < 2:
      groups[-1]+=" "
      self.texts[id] = {"x":x,"y":y,"len":(len(text)+1)/2}
    else:
      self.texts[id] = {"x":x,"y":y,"len":len(text)/2}
    for _x in range(len(groups)):
      self.pixelMap[y][x+_x]["char"] = groups[_x]
  def deleteText(self,id):
    y = self.texts[id]["y"]
    _x = self.texts[id]["x"]
    finish = int(_x+self.texts[id]["len"])
    self.toUpdate[y] = True
    self.toRender[y] = True

    for x in self.pixelMap[y][_x:finish]:
      x["char"] = "  "
    del self.texts[id]

  def addObj(self,object):
    self.objects[object.id] = object
    for gO in object.rendObjs:
      for dot in gO.dots:
        self.plot(dot.x + object.x,dot.y + object.y,dot.color)
      for line in gO.lines:
        self.line(line.x1 + object.x,line.y1 + object.y,line.x2 + object.x,line.y2 + object.y,line.color)



class layer:
  def __init__(self,id,width,height):
    self.id = id
    self.width = width
    self.height = height

    self.objects = {}
    self.lookuptable = []
    self.pixelMap = []
    self.renderSteps = []
    self.toUpdate = {}
    self.toRender = {}
    #fill in lookup map and pixel map
    for y in range(height):
      self.pixelMap.append([])
      for x in range(width):
        self.pixelMap[y].append({
          "color" : [-10,-10,-10],
          "char" : "  ",
          "data" : []
        })

    for y in range(height):
      self.lookuptable.append([])
      for x in range(width):
        self.lookuptable[y].append((0,0))
    #pre update


  # this is about where i started to loose my mind
  # use see, since this is a layer, not a window, your not just allowed to store a huge pixelMap, update, render it, and call it a day
  # you cant do this because layers are not ment to color everything in a 10x10 area, there suposed to paint over only a few areas and preserve the window underneath it
  # so the slow arpoch would be to loop through all the obejcts and create a small string for each pixel each containing the move cursor command and bg color command
  # but this would create hundreds of strings and destroy performance at the time of rendering, so the optimised solution would be to have mini tables containing x,y and content,
  # the "content" would contain a single row of pixels folowing the y axis, of course preoptimised and precolored to make use of as little color commands as posible,
  # this table would then be taken in the render command to generate an escape sequence that would esentialy in sudo code do this, move_cursor(x,y) print(content) repeat
  # now this is all easy stuff, but, when it comes to further optimisation, using a table containing the y position of pixels that need to be updated, thats where it all breaks down, because
  # you now need to take into consideration all of the graphical objects and their x and y values, and whenever they are changed, you must update the mini tables of pixels that need to be updated
  # however, how would you know where the corrosponding mini tables are in the big table

  
  def render(self):
    for step in self.renderSteps:
      sys.stdout.write(step)
    sys.stdout.write("\033[" + str(self.height + 1) + ";0H")

  def addOBJ(self,object):
    self.objects[object.id] = object
    self.toUpdate[object.id] = True
    self.toRender[object.id] = True
  
  def updateOBJs(self):
    for id, needUpdate in self.toUpdate.items():
      if needUpdate:
        for GOBJ in self.objects[id].rendObjs:
          for i, NU in enumerate(GOBJ.dotUpdates):
            if NU:
              GOBJ._dots[i].toUpdate = False
              x = GOBJ._dots[i]._x
              y = GOBJ._dots[i]._y
              color = GOBJ._dots[i]._color
              self.pixelMap[y + self.objects[id].oy ][x + self.objects[id].ox ]["color"] = [-10,-10,-10]
              self.pixelMap[y + self.objects[id].y ][x + self.objects[id].x ]["color"] = color
          for i, NU in enumerate(GOBJ.lineUpdates):
            if NU:
              x1 = GOBJ._lines[i]._x1
              y1 = GOBJ._lines[i]._y1
              x2 = GOBJ._lines[i]._x2
              y2 = GOBJ._lines[i]._y2
              color = GOBJ._lines[i]._color

              dx = x2 - x1
              dy = y2 - y1
              isSteep = abs(dy) > abs(dx)
              if isSteep:
                x1, y1 = y1, x1
                x2, y2 = y2, x2
              if x2 < x1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
              dx = x2 - x1
              dy = y2 - y1
              error = int(dx / 2.0)
              ystep = 1 if y1 < y2 else -1
              y = y1
              for x in range(x1, x2 + 1):
                if isSteep:
                  self.pixelMap[x + self.objects[id].oy ][y + self.objects[id].ox ]["color"] = [-10,-10,-10]
                else:
                  self.pixelMap[y + self.objects[id].oy ][x + self.objects[id].ox ]["color"] = [-10,-10,-10]
                error -= abs(dy)
                if error < 0:
                  y += ystep
                  error += dx

              error = int(dx / 2.0)
              y = y1
              for x in range(x1, x2 + 1):
                if isSteep:
                  self.pixelMap[x + self.objects[id].y][y + self.objects[id].x]["color"] = color
                else:
                  self.pixelMap[y + self.objects[id].y][x + self.objects[id].x]["color"] = color
                error -= abs(dy)
                if error < 0:
                  y += ystep
                  error += dx

  def updatePXMAPtoInstructions(self):
    oldRGB = [0,0,0]
    rgb = [0,0,0]
    contents = []
    for _y, y in enumerate(self.pixelMap):
      content = ""
      haspos = False
      for _x, x in enumerate(y):
        if x["color"][0] >= 0:
          if not haspos:
            haspos = True
            content += f"\033[{_y + 1};{(_x*2)+1}H"
          oldRGB = rgb
          rgb = x["color"]
          if oldRGB == rgb:
            content += x["char"]
          else:
            content += f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m{x['char']}"
        else:
          haspos = False
      contents.append(content)
    self.renderSteps = contents
class graphicalObj:
  def __init__(self,id,dots=[],lines=[]):
    self.id = id
    self._dots = dots
    self._lines = lines
    self._mx = max(max(dot.x for dot in self._dots),max(max(line.x1 , line.x2) for line in self._lines))
    self._my = max(max(dot.y for dot in self._dots),max(max(line.y1 , line.y2) for line in self._lines))
    self.omx = self._mx
    self.omy = self._my
    
    self.renderSTR = []
    self.needPixMapUpdate = False
    self.pixmap = [[[] for i in range(self._mx)] for i in range(self._my)]
    self.needUpdates = []

  @property
  def mx(self):
    return self._mx
  @mx.setter
  def mx(self,value):
    self.omx = self._mx
    self._mx = value
    extraX = value - self.omx
    for y in self.pixmap:
      for i in range(extraX): y.append([])

  @property
  def my(self):
    return self._my
  @my.setter
  def my(self,value):
    self.omy = self._my
    self._my = value
    extraY = value - self.omy
    for i in range(extraY): self.pixmap.append([])
    
  
  
  @property
  def lines(self):
    return self._lines
  @lines.setter
  def lines(self,value):
    self._lines.append(value)
    mmx = max(value._x1, value._x2)
    mmy = max(value._y1, value._y2)
    if mmx > self._mx:
      self.mx = mmx
    if mmy > self._my:
      self.my = mmy

  @property
  def dots(self):
    return self._dots
  @dots.setter
  def dots(self,value):
    self._dots = value
    if value._x > self._mx:
      self.omx = self._mx
      self.mx = value._x
    if value._y > self._my:
      self.omy = self._my
      self.my = value._y

  
  @property
  def lineUpdates(self):
    return [True if i.toUpdate else False for i in self._lines]
  @property
  def dotUpdates(self):
    return [True if i.toUpdate else False for i in self._dots]
  
  class dot:
    def __init__(self,x,y,color):
      self._x = x
      self._y = y
      self._color = color
      self.toUpdate = True
    
    @property
    def x(self):
      return self._x
    @x.setter
    def x(self,value):
      self._x = value
      self.toUpdate = True

    @property
    def y(self):
      return self._y
    @y.setter
    def y(self,value):
      self._y = value
      self.toUpdate = True

    @property
    def color(self):
      return self._color
    @color.setter
    def color(self,value):
      self._color = value
      self.toUpdate = True
    
  class line:
    def __init__(self,x1,y1,x2,y2,color):
      self._x1 = x1
      self._x2 = x2
      self._y1 = y1
      self._y2 = y2
      self.toUpdate = True
      self._color = color

    @property
    def x1(self):
      return self._x1
    @x1.setter
    def x1(self,value):
      self._x1 = value
      self.toUpdate = True

    @property
    def x2(self):
      return self._x2
    @x2.setter
    def x2(self,value):
      self._x2 = value
      self.toUpdate = True

    @property
    def y1(self):
      return self._y1
    @y1.setter
    def y1(self,value):
      self._y1 = value
      self.toUpdate = True

    @property
    def y2(self):
      return self._y2
    @y2.setter
    def y2(self,value):
      self._y2 = value
      self.toUpdate = True

    @property
    def color(self):
      return self._color
    @color.setter
    def color(self,value):
      self._color = value
      self.toUpdate = True
class object:
  def __init__(self,id,x,y,graphicalObjects):
    self.id = id
    self._x = x
    self._y = y
    self.ox = x
    self.oy = y
    self.rendObjs = graphicalObjects
    self.renderSTR = []

  @property
  def x(self):
    return self._x
  @x.setter
  def x(self,value):
    self.ox = self._x
    for i in self.rendObjs:
      for v in i._dots: v.toUpdate = True

    for i in self.rendObjs:
      for v in i._lines: v.toUpdate = True
    
    self._x = value


  @property
  def y(self):
    return self._y
  @y.setter
  def y(self,value):
    self.oy = self._y
    for i in self.rendObjs:
      for v in i._dots: v.toUpdate = True

    for i in self.rendObjs:
      for v in i._lines: v.toUpdate = True
    self._y = value
