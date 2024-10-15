class interval:
  def __init__(self,min:float=999999999999999999999,max:float=-999999999999999999999):
    self.min = min
    self.max = max

  def conatains(self,x:float):
    return self.min <= x and x <= self.max

  def surrounds(self,x:float):
    return self.min < x and x < self.max

  def clamp(self,x:float):
    if x < self.min:
      return self.min
    if x > self.max:
      return self.max
    return x


class empty(interval):
  def __init__(self):
    return interval(999999999999999999999,-999999999999999999999)

class universe(interval):
  def __init__(self):
    return interval(-999999999999999999999,999999999999999999999)