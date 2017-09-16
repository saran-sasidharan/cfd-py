from os import path
import node as nd
import face as fc
import cell as cl

def find_string_list(file_list, search_list, start_index=0):
  '''Return index of file_list where all strings in
     search_list are found. Optional start index of search
     can be specified by setting start_index'''
  for i, string in enumerate(file_list[start_index:]):
    if all(map(lambda s: s in string, search_list)):
      return start_index + i
  return None

def array_inside(string, left, right, type):
  '''Returns string inside left char and right char'''
  inside_string = string[string.find(left)+1:string.find(right)]
  return [type(i) for i in inside_string.split()]

def readOpenFoamMesh(directory):
  local_path = 'constant/polyMesh'

  points_file = path.join(directory, local_path, 'points')
  faces_file = path.join(directory, local_path, 'faces')
  owner_file = path.join(directory, local_path, 'owner')
  neighbour_file = path.join(directory, local_path, 'neighbour')

  data = None
  with open(points_file, 'r') as data_file:
    data = data_file.readlines()
  pointer = find_string_list(data, ['('])
  nNodes = int(data[pointer-1])
  nodes = []
  for i in range(nNodes):
    pointer += 1
    array = array_inside(data[pointer], '(', ')', float)
    nodes.append(nd.Node(i, array))

  with open(faces_file, 'r') as data_file:
    data = data_file.readlines()
  pointer = find_string_list(data, ['('])
  nFaces = int(data[pointer-1])
  faces = []
  for i in range(nFaces):
    pointer += 1
    array = array_inside(data[pointer], '(', ')', int)
    node_array = [nodes[j] for j in array]
    faces.append(fc.Face(i, node_array))

  with open(owner_file, 'r') as data_file:
    data = data_file.readlines()
  pointer = find_string_list(data, ['('])
  assert nFaces == int(data[pointer-1])
  # Finding total number of cells
  pointer2 = find_string_list(data, [')'], pointer)
  owner_cell_indexes = [int(i.strip())
                        for i in data[pointer+1:pointer2]]
  nCells = max(owner_cell_indexes) + 1
  cellfaces = [[] for i in range(nCells)]
  cellfacesigns = [[] for i in range(nCells)]
  for face_id, cell_id in enumerate(owner_cell_indexes):
    cellfaces[cell_id].append(faces[face_id])
    cellfacesigns[cell_id].append(1.0)

  with open(neighbour_file, 'r') as data_file:
    data = data_file.readlines()
  pointer = find_string_list(data, ['('])
  nIFaces = int(data[pointer-1])
  pointer2 = find_string_list(data, [')'], pointer)
  neighbour_cell_indexes = [int(i.strip())
                            for i in data[pointer + 1:pointer2]]
  for face_id, cell_id in enumerate(neighbour_cell_indexes):
    cellfaces[cell_id].append(faces[face_id])
    cellfacesigns[cell_id].append(-1.0)

  cells = []
  for i, face_list in enumerate(cellfaces):
    cells.append(cl.Cell(i, face_list, cellfacesigns[i]))

  return (nNodes, nodes, nFaces, nIFaces, faces, nCells, cells)

