import numpy as np

class Node(object):
  ''' Node of mesh '''  
  def __init__(self, id, centroid):
    # Properties
    self.id = id
    self.centroid = np.array(centroid, dtype=float)
    # Updated later
    self.faces = []
    self.cells = []
