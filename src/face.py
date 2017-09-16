import numpy as np

class Face(object):

  def __init__(self, id, nodes):
    # Properties
    self.id = id
    self.centroid = np.zeros(3, dtype=float)
    self.area_vector = np.zeros(3, dtype=float)
    self.area = 0.0
    self.nNodes = len(nodes)
    self.nodes = nodes
    # Updated later
    self.cells = [None, None]
    # Initializing functions
    self._set_properties()
    self._update_node()
    return None

  def _set_properties(self):
    # Finding initial guess of face centroid
    centre = np.zeros(3, dtype=float)
    for node in self.nodes:
      centre += node.centroid
    centre /= self.nNodes

    for i, node in enumerate(self.nodes):
      # Cycle through nodes
      j = np.mod(i+1, self.nNodes)

      point1 = node.centroid
      point2 = self.nodes[j].centroid

      centroid = (centre + point1 + point2) / 3.0
      area_vector = 0.5 * np.cross(point1-centre, point2-centre)
      area = np.linalg.norm(area_vector)

      self.centroid += area * centroid
      self.area_vector += area_vector
      self.area += area

    self.centroid /= self.area
    return None

  def _update_node(self):
    # Appending this face to nodes which make this face
    [node.faces.append(self) for node in self.nodes] 
    return None

def test_face_quad():
  from node import Node
    
  points = [[0.,0.,0.], [1.,0.,0.], [1.,1.,0.], [0.,1.,0.]]
  nodes = [Node(i, np.array(point, dtype=float)) 
                for i, point in enumerate(points)]

  f = Face(1, nodes)
  assert abs(f.area - 1.0) < 1e-10
  assert np.linalg.norm(f.area_vector - [0.,0.,1.]) < 1e-10
  assert np.linalg.norm(f.centroid - [0.5,0.5,0.]) < 1e-10
  return None

def test_face_tri():
  from node import Node
    
  points = [[0.,0.,0.], [1.,0.,0.], [1.,1.,0.]]
  nodes = [Node(i, np.array(point, dtype=float)) 
                for i, point in enumerate(points)]

  f = Face(1, nodes)
  assert abs(f.area - 0.5) < 1e-10
  assert np.linalg.norm(f.area_vector - [0.,0.,0.5]) < 1e-10
  assert np.linalg.norm(f.centroid - [2./3.,1./3.,0.]) < 1e-10
  return None