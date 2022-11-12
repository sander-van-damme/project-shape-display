#!/usr/bin/env python3
import itertools
import numpy
from solid2 import OpenSCADObject, circle, square


class EmptyOpenSCADObject(circle):
    def __init__(self):
        super().__init__(0)


class ShapeDisplay:
    def __init__(self, width=80, row_count=8):
        self.width = width
        self.row_count = row_count
        self.row_width = self.width / self.row_count

    def hole_grid(self, cell_filter_states) -> OpenSCADObject:
        ''' Return a grid of holes that forms the basis of a filter layer. '''
        hole_radius = self.row_width / 5
        secondary_hole_offset = 2 * hole_radius + self.row_width / self.row_count

        grid = EmptyOpenSCADObject()
        for (row_number, row) in enumerate(cell_filter_states):
            for (column_number, cell_is_always_open) in enumerate(row):
                cell = circle(hole_radius) # primary hole
                if cell_is_always_open: # secondary hole
                    cell += circle(hole_radius).back(secondary_hole_offset)
                grid += cell \
                    .back(row_number * self.row_width) \
                    .right(column_number * self.row_width)
                    
        # Center the grid.
        grid = grid \
            .left((self.row_count - 1) * self.row_width / 2) \
            .forward((self.row_count - 1) * self.row_width / 2) \
            .forward(secondary_hole_offset / 2)
        return grid

    def filter_layer(self, open_rows=[], open_columns=[], filter_layer_height=1) -> OpenSCADObject:
        ''' Return a single filter layer. '''

        # Create solid layer.
        layer = square(self.width, center=True).linear_extrude(
            filter_layer_height, center=True)

        # Create hole grid.
        cell_filter_states = numpy.zeros(
            (self.row_count, self.row_count), dtype=bool)
        cell_filter_states[open_rows, :] = True
        cell_filter_states[:, open_columns] = True
        hole_grid = self.hole_grid(cell_filter_states) \
            .linear_extrude(filter_layer_height + 0.002, center=True)
        return layer - hole_grid

    def filter_layer_pair(self, open_rows, open_columns) -> tuple[OpenSCADObject]:
        '''
            Return a pair of filter layers that aim to filter a set of rows and/or columns.
            A filter layer pair can open all its cells when not in use.
            This might improve actuation time in some situations but this also doubles the amount of actuators required.
        '''
        main_filter_layer = self.filter_layer(open_rows, open_columns)
        base = numpy.array(range(self.row_count))
        inverted_filter_layer = self.filter_layer(
            base ^ open_rows, base ^ open_columns)
        return (main_filter_layer, inverted_filter_layer)

    def filter_layers(self):
        ''' Return all filter layers of the shape display. '''
        # Determine the increments for the row and column filters.
        increments = set()

        def divide_by_2(x):
            if x >= 1 and x < self.row_count:
                increments.add(x)
            if x > 1:
                divide_by_2(x // 2)
                divide_by_2(x - (x // 2))
        divide_by_2(self.row_count)

        # Translate the increments to filter configurations.
        filter_configs = [
            
            list(itertools.chain.from_iterable(
            numpy.arange(self.row_count)[start:start+range] for start in numpy.arange(self.row_count)[::range*2])) for range in increments]

        # Store the filter layers.
        for filter_config in filter_configs:
            self.filter_layer(open_rows=filter_config).save_as_scad(
                f'filter-layer-rows_{"-".join(str(num) for num in filter_config)}.scad')
            self.filter_layer(open_columns=filter_config).save_as_scad(
                f'filter-layer-columns_{"-".join(str(num) for num in filter_config)}.scad')
