
class Node(object):
  ''' Node of mesh '''  
  def __init__(self, id, centroid):
    self.id = id
    self.centroid = centroid
    self.faces = []
