import readOpenFoam as rof

class Mesh(object):

  def __init__(self, directory):
    self.directory = directory
    # Properties
    self.nNodes = None
    self.nodes = None
    self.nFaces = None
    self.nIFaces = None
    self.faces = None
    self.nCells = None
    self.cells = None
    # Initializing functions
    self._update_mesh()

  def _update_mesh(self):
    ( self.nNodes,
      self.nodes,
      self.nFaces,
      self.nIFaces,
      self.faces,
      self.nCells,
      self.cells ) = rof.readOpenFoamMesh(self.directory)

mesh = Mesh('/home/numguy/Projects/cfd-py/cavity')
