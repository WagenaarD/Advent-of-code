"""
Overengineered solution that works for both example and input. Does the folding itself.

Advent of code challenge 2022
>> python3 main.py < in
Part 1  - 67390 (ex 6032)
Part 2  - 95291 (ex 5031)
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, namedtuple
import re
import numpy as np
from pprint import pprint
from functools import cache


AXES = 'xyz'
VECTOR_NAME = {
    ( 1, 0, 0): '+x',
    (-1, 0, 0): '-x',
    (0,  1, 0): '+y',
    (0, -1, 0): '-y',
    (0, 0,  1): '+z',
    (0, 0, -1): '-z',
}
DIR_SCORE = {
    ( 0,  1): 0, # 0 for right
    ( 1,  0): 1, # 1 for down
    ( 0, -1): 2, # 2 for left
    (-1,  0): 3, # 3 for up
}


class Vector:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    @classmethod
    def by_name(cls, name: str):
        return Vector(*([key for key, key_name in VECTOR_NAME.items() if key_name == name][0]))

    def __str__(self):
        vector_tuple = tuple(getattr(self, axis) for axis in AXES)
        if vector_tuple in VECTOR_NAME:
            return VECTOR_NAME[vector_tuple]
        else:
            return '<Vector({},{},{})>'.format(self.x, self.y, self.z)
        
    def __eq__(self, other) -> bool:
        if type(other) != Vector:
            return False
        return all(getattr(self, axis) == getattr(other, axis) for axis in AXES)
    
    def __add__(self, other):
        return Vector(*(getattr(self, axis) + getattr(other, axis) for axis in AXES))

    def __sub__(self, other):
        return Vector(*(getattr(self, axis) - getattr(other, axis) for axis in AXES))

    def __mul__(self, other):
        if type(other) == int:
            return Vector(*(getattr(self, axis) * other for axis in AXES))
        elif type(other) == Vector:
            return sum(getattr(self, axis) * getattr(other, axis) for axis in AXES)

    def __neg__(self):
        return Vector(*(-getattr(self, axis) for axis in AXES))
        
    def outer_product(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


class Face:
    def __init__(self, face_row, face_col, size, row_axis = None, col_axis = None, out_axis = None):
        self.face_row, self.face_col = face_row, face_col
        self.size = size
        self.row_axis, self.col_axis, self.out_axis = row_axis, col_axis, out_axis
    
    @property
    def origin(self):
        origin = Vector(0,0,0)
        if str(self.row_axis)[0] == '-':
            origin += -self.row_axis * (self.size - 1)
        if str(self.col_axis)[0] == '-':
            origin += -self.col_axis * (self.size - 1)
        if str(self.out_axis)[0] == '-':
            origin += self.out_axis * 1
        else:
            origin += self.out_axis * self.size
        return origin

    def row_col_to_vector(self, row, col):
        return self.origin + \
            self.row_axis * (row - self.face_row * self.size)+ \
            self.col_axis * (col - self.face_col * self.size)
        
    def vector_to_row_col(self, vector):
        vector = vector - self.origin
        row = self.row_axis * vector + self.face_row * self.size
        col = self.col_axis * vector + self.face_col * self.size
        return (row, col)

    def __str__(self):
        return '<Face "{}">'.format(str(self.out_axis))
    

class Cube:
    def __init__(self, lines):
        self.lines = lines
        no_fields = sum([line.count('.') + line.count('#') for line in lines])
        self.size = int((no_fields / 6) ** 0.5)
        # Determine where the faces are located in the input file
        self.faces = []
        for face_row in range(len(lines) // self.size):
            for face_col in range(len(lines[0]) // self.size):
                if self.lines[face_row * self.size][face_col * self.size] != ' ':
                    self.faces.append(Face(face_row, face_col, self.size))
        # Set the axis direction for the first face
        self.faces[0].col_axis = Vector.by_name('+x')
        self.faces[0].row_axis = Vector.by_name('+y')
        self.faces[0].out_axis = Vector.by_name('+z')
        # Derive the axis directions for other faces
        while len([face for face in self.faces if face.out_axis != None]) < 6:
            for face in self.faces:
                if face.out_axis:
                    continue
                # List neighboring faces
                for drow, dcol in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nbor = self.get_face(face.face_row + drow, face.face_col + dcol)
                    if nbor:
                        if nbor.out_axis:
                            # Derive an axes system
                            if dcol == -1: # face to right of nbor
                                face.col_axis = -nbor.out_axis
                                face.row_axis = nbor.row_axis
                                face.out_axis = nbor.col_axis
                            elif dcol == 1: # face to left of nbor
                                face.row_axis = nbor.row_axis
                                face.col_axis = nbor.out_axis
                                face.out_axis = -nbor.col_axis
                            elif drow == -1: # face below nbor
                                face.row_axis = -nbor.out_axis
                                face.col_axis = nbor.col_axis
                                face.out_axis = nbor.row_axis
                            elif drow == 1: # face above nbor (will never happen)
                                face.row_axis = nbor.out_axis
                                face.col_axis = nbor.col_axis
                                face.out_axis = -nbor.row_axis
        print(self)
        self.reset_position()
    
    def reset_position(self):
        self.pos = (0, self.lines[0].index('.'))
        self.dir = (0, 1)

    def process_input(self, input, folded = True):
        print(input)
        for _, command in enumerate(re.findall('[0-9]+|[LR]', input)):
            print('(_, pos, dir, command) =', (_, self.pos, self.dir, command))
            if command == 'L':
                self.dir = (-self.dir[1], self.dir[0])
            elif command == 'R':
                self.dir = (self.dir[1], -self.dir[0])
            else:
                self.move_forward(int(command), folded)

    def move_forward(self, steps, folded):
        for _ in range(steps):
            dr, dc = self.dir
            ndir = self.dir
            row, col = self.pos
            nrow, ncol = row + dr, col + dc
            if self.out_of_bounds(nrow, ncol):
                if not folded:
                    # Manage wrapping around (Part 1)
                    while self.lines[nrow % len(self.lines)][ncol % len(self.lines[0])] == ' ':
                        nrow, ncol = (nrow + dr) % len(self.lines), (ncol + dc) % len(self.lines[0])
                else:
                    # Manage folds in space (Part 2)
                    print('  OOB. (row, col, dr, dc)', (row, col, dr, dc))
                    print('    (row, col)', (row, col))
                    print('    (nrow, ncol)', (nrow, ncol))
                    # Find axes of current face
                    old_face = self.get_face(row // self.size, col // self.size)
                    edge_position = old_face.row_col_to_vector(nrow, ncol)
                    if dr == 1:
                        old_vector = old_face.row_axis
                    elif dr == -1:
                        old_vector = -old_face.row_axis
                    elif dc == 1:
                        old_vector = old_face.col_axis
                    elif dc == -1:
                        old_vector = -old_face.col_axis
                    # Get new face(old direction == out_axis of new face)
                    next_face = [face for face in self.faces if face.out_axis == old_vector][0]
                    # Find the new direction in the row, col grid
                    new_vector = -old_face.out_axis
                    if new_vector == next_face.row_axis:
                        ndir = (1, 0)
                    elif new_vector == -next_face.row_axis:
                        ndir = (-1, 0)
                    elif new_vector == next_face.col_axis:
                        ndir = (0, 1)
                    elif new_vector == -next_face.col_axis:
                        ndir = (0, -1)
                    # Process one cell from the edge of the cube onto the face
                    row, col = next_face.vector_to_row_col(edge_position)
                    dr, dc = ndir
                    nrow, ncol = row + dr, col + dc
                    print('    (edge_position)', edge_position)
                    print('    (row, col)', (row, col))
                    print('    (nrow, ncol)', (nrow, ncol))
            if self.lines[nrow][ncol] == '#':
                break
            self.pos, self.dir = (nrow, ncol), ndir

    @property
    def score(self):
        return (self.pos[0] + 1) * 1000 + (self.pos[1] + 1) * 4 + DIR_SCORE[self.dir]

    def out_of_bounds(self, row, col):
        if not (0 <= row < len(self.lines) and 0 <= col < len(self.lines[0])):
            return True
        return self.lines[row][col] == ' '

    def get_face(self, face_row, face_col):
        try:
            return [face for face in self.faces if face.face_row == face_row and face.face_col == face_col][0]
        except:
            return None
    
    def __str__(self):
        output = ' ' * 8
        for face_col in range(max([face.face_col for face in self.faces]) + 2):
            output += (' ' if face_col * self.size < 100 else str((face_col * self.size // 100) % 10)) + ' ' * 12
        output += '\n' + ' ' * 8
        for face_col in range(max([face.face_col for face in self.faces]) + 2):
            output += (' ' if face_col * self.size < 10 else str((face_col * self.size // 10) % 10)) + ' ' * 12
        output += '\n' + ' ' * 8
        for face_col in range(max([face.face_col for face in self.faces]) + 2):
            output += str((face_col * self.size) % 10) + ' ' * 12
        output += '\n' + ' ' * 8
        for face_col in range(max([face.face_col for face in self.faces]) + 2):
            output += '|' + ' ' * 12
        output += '\n'
        for face_row in range(max([face.face_row for face in self.faces]) + 1):
            output += '{:4} -  '.format(face_row * self.size)
            for face_col in range(max([face.face_col for face in self.faces]) + 1):
                output += '.-----------.' if self.get_face(face_row, face_col) else ' ' * 13
            output += '\n' + ' ' * 8
            for face_col in range(max([face.face_col for face in self.faces]) + 1):
                face = self.get_face(face_row, face_col)
                output += '|  ---> {}  |'.format(face.col_axis) if face else ' ' * 13
            output += '\n' + ' ' * 8
            for face_col in range(max([face.face_col for face in self.faces]) + 1):
                face = self.get_face(face_row, face_col)
                output += '| |         |' if face else ' ' * 13
            output += '\n' + ' ' * 8
            for face_col in range(max([face.face_col for face in self.faces]) + 1):
                face = self.get_face(face_row, face_col)
                output += '| |   {}     |'.format(self.faces.index(face)) if face else ' ' * 13
            output += '\n' + ' ' * 8
            for face_col in range(max([face.face_col for face in self.faces]) + 1):
                face = self.get_face(face_row, face_col)
                output += '| V     {}  |'.format(face.out_axis) if face else ' ' * 13
            output += '\n' + ' ' * 8
            for face_col in range(max([face.face_col for face in self.faces]) + 1):
                face = self.get_face(face_row, face_col)
                output += '| {}        |'.format(face.row_axis) if face else ' ' * 13
            output += '\n' + ' ' * 8
            for face_col in range(max([face.face_col for face in self.faces]) + 1):
                face = self.get_face(face_row, face_col)
                output += '.-----------.' if face else ' ' * 13
            output += '\n'
        output += '{:4} -  '.format((max([face.face_row for face in self.faces]) + 1) * self.size)
        return output


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    
    lines, input = sys.stdin.read().split('\n\n')
    lines = lines.split('\n')
    width = max([len(line) for line in lines])
    lines = [line + ' ' * (width - len(line)) for line in lines]

    cube = Cube(lines)
    cube.process_input(input, False)
    part_1 = cube.score
    cube.reset_position()
    cube.process_input(input, True)
    part_2 = cube.score

    print('Part 1:', part_1)
    print('Part 1:', part_2)

