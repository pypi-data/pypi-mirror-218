from matplotlib import collections, colors, cm, patches
import matplotlib.pyplot as plt
import numpy as np


class Utilities:
    """A class to perform maze-related utility functions.

    Attributes
    ----------
    figure : :class:`~matplotlib.figure.Figure`, optional
        A :class:`~matplotlib.figure.Figure` instance.
    axes : :class:`~matplotlib.axes.Axes`, optional
        A :class:`~matplotlib.axes.Axes` instance.
    """

    def __init__(self):
        self.figure: plt.Figure | None = None
        self.axes: plt.Axes | None = None

    def _plot_walls(self, grid):
        """Plot the walls of the maze with Matplotlib."""
        for row in range(len(grid)):
            for column, walls in enumerate(grid[row]):
                if walls[0]:
                    self.axes.plot(
                        [column, column + 1],
                        [-row, -row],
                        color="k",
                    )
                if walls[2]:
                    self.axes.plot(
                        [column + 1, column + 1],
                        [-row, -row - 1],
                        color="k",
                    )
                if walls[3]:
                    self.axes.plot(
                        [column, column],
                        [-row, -row - 1],
                        color="k",
                    )
                if walls[1]:
                    self.axes.plot(
                        [column, column + 1],
                        [-row - 1, -row - 1],
                        color="k",
                    )

    def _initiate_plot(self, size=(8, 8)):
        """Initiate a plot from Matplotlib."""
        self.figure = plt.figure(figsize=size)
        self.axes = plt.axes()
        self.axes.set_aspect("equal")
        self.axes.set_axis_off()

    def show_grid(self, grid: np.ndarray):
        """Display a plot of a rectangular, two-dimensional maze.

        Visualization is done with `Matplotlib <https://matplotlib.org/>`_.

        Parameters
        ----------
        grid : numpy.ndarray
            A two-dimensional array of cells representing a rectangular maze.
        """
        self._initiate_plot()
        self._plot_walls(grid)
        plt.show()

    def save_grid(
        self, grid: np.ndarray, file_name: str, cell_size: int = 15, line_width: int = 2
    ):
        """Save a maze as an SVG file.

        Parameters
        ----------
        grid : numpy.ndarray
            A two-dimensional array of cells representing a rectangular maze.
        file_name : str
            A path wherein the SVG file is saved.
        cell_size : int
            The size of each cell in pixels.
        line_width : int
            The width of the wall lines in pixels.
        """
        with open(file_name, "w") as file:
            file.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{cell_size * len(grid[0]) + line_width}" height="{cell_size * len(grid) + line_width}" fill="none" stroke="#000" stroke-width="{line_width}" stroke-linecap="square">\n'
            )
            for row in range(len(grid)):
                for column, walls in enumerate(grid[row]):
                    a = column * cell_size + line_width / 2
                    b = row * cell_size + line_width / 2
                    c = (column + 1) * cell_size + line_width / 2
                    d = (row + 1) * cell_size + line_width / 2
                    if row == 0 and walls[0]:
                        file.write(f'\t<line x1="{a}" y1="{b}" x2="{c}" y2="{b}" />\n')
                    if walls[1]:
                        file.write(f'\t<line x1="{a}" y1="{d}" x2="{c}" y2="{d}" />\n')
                    if walls[2]:
                        file.write(f'\t<line x1="{c}" y1="{b}" x2="{c}" y2="{d}" />\n')
                    if column == 0 and walls[3]:
                        file.write(f'\t<line x1="{a}" y1="{b}" x2="{a}" y2="{d}" />\n')
            file.write("</svg>")

    def show_solution(self, grid: np.ndarray, solution_path: list[tuple[int, int]]):
        """Display a plot of a rectangular, two-dimensional maze and its solution path.

        Visualization is done with `Matplotlib <https://matplotlib.org/>`_.

        Parameters
        ----------
        grid : numpy.ndarray
            A two-dimensional array of cells representing a rectangular maze.
        solution_path : list[tuple[int, int]]
            An ordered list of cell locations representing the solution path.
        """
        self._initiate_plot()
        self._plot_walls(grid)

        # Add an ordered list of rectangle patches.
        patch_list = []
        for row, column in solution_path:
            patch_list.append(patches.Rectangle((column, -row - 1), 1, 1))

        # Create a value array for the color map.
        values = [i for i in range(len(solution_path))]
        norm = colors.Normalize().autoscale(values)

        # Add the list of patches to a patch collection.
        collection = collections.PatchCollection(patch_list, norm=norm, cmap="RdYlGn")

        # Set the value array of the patches.
        collection.set_array(values)

        # Add the collection to the axes.
        self.axes.add_collection(collection)
        plt.show()

    def save_solution(
        self,
        grid: np.ndarray,
        solution_path: list[tuple[int, int]],
        file_name: str,
        cell_size: int = 15,
        line_width: int = 2,
        colormap: str = "RdYlGn",
    ):
        """Save a maze and its solution as an SVG file.

        For more colormap selection, click `here <https://matplotlib.org/stable/tutorials/colors/colormaps.html>`_.

        Parameters
        ----------
        grid : numpy.ndarray
            A two-dimensional array of cells representing a rectangular maze.
        solution_path : list[tuple[int, int]]
            An ordered list of cell locations representing the solution path.
        file_name : str
            A path wherein the SVG file is saved.
        cell_size : int
            The size of each cell in pixels.
        line_width : int
            The width of the wall lines in pixels.
        colormap : str
            A colormap included with Matplotlib.
        """

        colormap_ = cm.get_cmap(colormap)
        array = np.linspace(0, 1, len(solution_path))
        color_list = list()

        for value in array:
            rgba = colormap_(value)
            color_list.append(colors.to_hex(rgba))

        with open(file_name, "w") as file:
            file.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{cell_size * len(grid[0]) + line_width}" height="{cell_size * len(grid) + line_width}">\n'
            )
            for i, cell in enumerate(solution_path):
                file.write(
                    f'\t<path fill="{color_list[i]}" d="M{cell[1] * cell_size + line_width / 2} {cell[0] * cell_size + line_width / 2}h{cell_size}v{cell_size}h-{cell_size}z" />\n'
                )
            file.write(f'\t<g fill="none" stroke="#000" stroke-width="{line_width}" stroke-linecap="square">')
            for row in range(len(grid)):
                for column, walls in enumerate(grid[row]):
                    a = column * cell_size + line_width / 2
                    b = row * cell_size + line_width / 2
                    c = (column + 1) * cell_size + line_width / 2
                    d = (row + 1) * cell_size + line_width / 2
                    if row == 0 and walls[0]:
                        file.write(
                            f'\t\t<line x1="{a}" y1="{b}" x2="{c}" y2="{b}" />\n'
                        )
                    if walls[1]:
                        file.write(
                            f'\t\t<line x1="{a}" y1="{d}" x2="{c}" y2="{d}" />\n'
                        )
                    if walls[2]:
                        file.write(
                            f'\t\t<line x1="{c}" y1="{b}" x2="{c}" y2="{d}" />\n'
                        )
                    if column == 0 and walls[3]:
                        file.write(
                            f'\t\t<line x1="{a}" y1="{b}" x2="{a}" y2="{d}" />\n'
                        )
            file.write("</g>")
            file.write("</svg>")