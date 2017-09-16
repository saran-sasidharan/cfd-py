import numpy as np

class Cell(object):
  
  def __init__(self, id, faces, facesigns):
    # Properties
    self.id = id
    self.centroid = np.zeros(3, dtype=float)
    self.volume = 0.0 
    self.nFaces = len(faces)
    self.faces = faces
    self.facesigns = np.array(facesigns, dtype=float)
    self.nodes = []
    # Updated later
    # Initializing functions
    self._set_properties()
    self._update_faces()
    self._update_nodes()

  def _set_properties(self):
    # Initial guess of cell centroid
    centre = np.zeros(3, dtype=float)
    for face in self.faces:
      centre += face.centroid
    centre /= self.nFaces

    for i, face in enumerate(self.faces):
      area_out_vector = face.area_vector * self.facesigns[i] 
      distance_vector = face.centroid - self.centroid
      volume = np.dot(distance_vector, area_out_vector) / 3.0

      centroid = 0.25*centre + 0.75*face.centroid

      self.centroid += volume * centroid
      self.volume += volume

    self.centroid /= self.volume
    return None

  def _update_faces(self):
    for sign, face in zip(self.facesigns, self.faces):
      if sign > 0:
        face.cells[0] = self
      else:
        face.cells[1] = self
    return None

  def _update_nodes(self):
    for face in self.faces:
      for node in face.nodes:
        if node not in self.nodes:
          self.nodes.append(node)
          node.cells.append(self)
    return None