import PIL.Image
import PIL.ImageTk
import argparse
import numpy as np
import scipy.signal as sp
import tkinter as tk


def update_board(field):
    neighbourhoods = sp.convolve2d(field, mask, mode='same')
    for x in range(width):
        for y in range(height):
            n_neighbours = neighbourhoods[x][y]
            if field[x][y] == 0:
                if n_neighbours in cell_born:
                    field[x][y] = 1
            else:
                if n_neighbours not in cell_survives:
                    field[x][y] = 0
    return field


def place_seeds(field):
    with np.nditer(field, op_flags=['readwrite']) as it:
        for x in it:
            if np.random.uniform(0.0, 1.0) < soup_density:
                x[...] = True
    return field


class GolField(tk.Canvas):

    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.board = place_seeds(np.zeros((width, height), dtype=bool))
        temp = PIL.Image.fromarray(self.board).resize(display_size)
        temp = PIL.ImageTk.PhotoImage(temp)
        self.create_image((0, 0), anchor='nw', image=temp)
        self.photo = temp

    def update_image(self):
        self.board = update_board(self.board)
        temp = PIL.Image.fromarray(self.board).resize(display_size)
        temp = PIL.ImageTk.PhotoImage(temp)
        self.create_image((0, 0), anchor='nw', image=temp)
        self.photo = temp

        self.after(delay, self.update_image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculates and displays cellular automata')

    parser.add_argument('-fs', '--fieldsize', action='store', default=200, type=int,
                        help='the size of the field to be simulated')

    parser.add_argument('-ds', '--displaysize', action='store', default=900, type=int,
                        help='the size of the display window')

    parser.add_argument('-d', '--delay', default=45, type=int,
                        help='the delay of the simulations iterations (in ms)')

    parser.add_argument('-sd', '--soup_density', default=0.4, type=float,
                        help='the initial soup density for the simulation')

    parser.add_argument('-b', '--born', nargs='+', type=int, default=[3],
                        help='an array of integers indicating, how many surrounding cells need to be alive for a cell '
                             'to be born.')

    parser.add_argument('-s', '--survives', nargs='+', type=int, default=[2, 3],
                        help='an array of integers indicating, how many surrounding cells need to be alive for a cell '
                             'to survive.')

    args = parser.parse_args()
    print(args)

    width, height = (args.fieldsize, args.fieldsize)

    display_size = (args.displaysize, args.displaysize)
    delay = args.delay

    mask = np.ones((3, 3), dtype=int)
    mask[1][1] = 0

    cell_born = args.born
    cell_survives = args.survives

    soup_density = args.soup_density

    window = tk.Tk()
    window.title('Game of life')

    foo = GolField(window, width=display_size[0], height=display_size[1])
    foo.pack()

    foo.after(delay, foo.update_image)

    window.mainloop()

