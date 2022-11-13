#!/usr/bin/env python3
from solid2 import *
import numpy

# shape display
width = 80
height = 80
x_resolution = 8  # must be even
y_resolution = 8  # must be even

# multiplexer
multiplexer_cell_width = width / x_resolution
multiplexer_layer_width = width - multiplexer_cell_width
multiplexer_layer_height = height
multiplexer_layer_depth = 1
multiplexer_inverted_layers_vectors = {'row': [4, 2, 1], 'column': [4, 2, 1]}
multiplexer_hole_radius = multiplexer_cell_width / 5
multiplexer_secondary_hole_offset = 2 * multiplexer_hole_radius + multiplexer_cell_width


class ShapeDisplay:
    @staticmethod
    def export():
        items = Multiplexer().elements
        for item in items:
            item.to_scad().save_as_scad(f'{item.name()}.scad')


class Multiplexer:
    def __init__(self) -> None:
        self._elements = [MultiplexerLayer(name, state_matrix) for (name, state_matrix) in
                          self.layers_state_matrices().items()]

    def layers_state_matrices(self) -> dict:
        step_counts = list(range_by_division(x_resolution // 2, 1, 2))
        vectors = {}
        for step_count in step_counts:
            vectors[step_count] = []
            for start in list(range(x_resolution))[::step_count * 2]:
                for el in list(range(x_resolution))[start:start + step_count]:
                    vectors[step_count].append(el)
        matrices = {}
        for (dimension, inverted_vector_names) in multiplexer_inverted_layers_vectors.items():
            for (step_count, vector) in vectors.items():
                matrix_name = f'multiplexer-{dimension}_layer-step_count_{step_count}'
                matrix = numpy.zeros((x_resolution, x_resolution), dtype=bool)
                if dimension == 'row':
                    matrix[vector, :] = True
                else:
                    matrix[:, vector] = True
                matrices[matrix_name] = matrix
                if step_count in inverted_vector_names:
                    matrices[f'{matrix_name}-inverted'] = numpy.invert(matrix)
        return matrices

    @property
    def elements(self):
        return self._elements


class MultiplexerLayer:
    def __init__(self, name, state_matrix) -> None:
        self._name = name
        self._state_matrix = state_matrix

    def name(self):
        return self._name

    def to_scad(self) -> OpenSCADObject:
        solid_layer = square(multiplexer_layer_width, center=True)
        holes = EmptyOpenSCADObject()
        for (row_nr, row) in enumerate(self._state_matrix):
            for (column_nr, is_always_open) in enumerate(row):
                primary_hole = circle(multiplexer_hole_radius)
                secondary_hole = EmptyOpenSCADObject() if not is_always_open \
                    else circle(multiplexer_hole_radius).back(multiplexer_secondary_hole_offset)
                holes += (primary_hole + secondary_hole) \
                    .back(row_nr * multiplexer_cell_width) \
                    .right(column_nr * multiplexer_cell_width)
        holes = holes \
            .left((x_resolution - 1) * multiplexer_cell_width / 2) \
            .forward((x_resolution - 1) * multiplexer_cell_width / 2 + multiplexer_secondary_hole_offset / 2)
        return solid_layer - holes


class Enclosure:
    def __init__(self):
        pass


class EmptyOpenSCADObject(circle):
    def __init__(self):
        super().__init__(0)


def range_by_division(start, end, denominator):
    value = start
    while value >= end:
        yield value
        value = value // denominator


# Run.
ShapeDisplay().export()
