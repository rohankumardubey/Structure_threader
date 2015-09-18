#!/usr/bin/python3

# Copyright 2015 Francisco Pina Martins <f.pinamartins@gmail.com>
# This file is part of structure_threader.
# structure_threader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# structure_threader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with structure_threader. If not, see <http://www.gnu.org/licenses/>.

# Usage: python3 structplot.py infile outfile

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import os


def dataminer(indfile_name, fmt, popfile=None):
    """Parse the output files of structure and faststructure and return a
    numpy array with the individual clustering values and a list with the
    population names and number of individuals.

    :param indfile_name: path to structure/fastStructure output file
    :param fmt: string, format of the indfile_name. Can be either structure of
    faststructure
    :param popfile: string. path to file with population list
    """

    poplist = []

    # Parse popfile if provided
    if popfile:
        # Assuming popfile has 2 columns with pop name in 1st column and number
        # of samples in the 2nd column
        poparray = np.genfromtxt(popfile, dtype=None)
        # Final pop list
        poplist = [(x, y.decode("utf-8")) for x, y in
                   zip(np.cumsum([x[1] for x in poparray]),
                       [x[0] for x in poparray])]

    # Parse structure/faststructure output file
    if fmt == "fastStructure":
        qvalues = np.genfromtxt(indfile_name)

    else:
        qvalues = np.array([])

        # Start file parsing
        parse = False
        with open(indfile_name) as file_handle:
            for line in file_handle:
                if line.strip().lower().startswith("inferred ancestry of "
                                                   "individuals:"):
                    # Enter parse mode ON
                    parse = True
                    # Skip subheader
                    next(file_handle)
                elif line.strip().lower().startswith("estimated allele "
                                                     "frequencies in each "
                                                     "cluster"):
                    # parse mode OFF
                    parse = False
                elif parse:
                    if line.strip() != "":
                        fields = line.strip().split()
                        # Get cluster values
                        cl = [float(x) for x in fields[5:]]
                        try:
                            qvalues = np.vstack((qvalues, cl))
                        except ValueError:
                            qvalues = np.array(cl)
                        if not popfile:
                            # Get population
                            poplist.append(int(fields[3]))

        if not popfile:
            # Transform poplist in convenient format, in which each element
            # is the boundary of a population in the x-axis
            poplist = Counter(poplist)
            poplist = [(x, None) for x in np.cumsum(list(poplist.values()))]


    return qvalues, poplist


def plotter(qvalues, poplist, outfile):
    """
    Plot the qvalues histogram.

    :param qvalues: numpy array with variable shape containing the inferred
    ancestry values for each sample
    :param poplist: list, contains information on the sample's population.
    Must be a list of tuples, in which each element consists of
    (x-axys position int, population label str). Example:
    [(2, "Angola"), (5, "Kenya")...]
    """

    colors = ('#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c',
              '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928')

    plt.style.use("ggplot")

    numinds = qvalues.shape[0]

    # Update plot width according to the number of samples
    plt.rcParams["figure.figsize"] = (8 * numinds * .01, 2.64)

    fig = plt.figure()
    ax = fig.add_subplot(111, xlim=(0, numinds), ylim=(0, 1))

    for i in range(qvalues.shape[1]):
        # Get bar color. If K exceeds the 12 colors in colors, generate random
        # color
        try:
            clr = colors[i]
        except IndexError:
            clr = np.random.rand(3, 1)

        if i == 0:
            ax.bar(range(numinds), qvalues[:, i], facecolor=clr,
                   edgecolor="none", width=1)
            former_q = qvalues[:, i]
        else:
            ax.bar(range(numinds), qvalues[:, i], bottom=former_q,
                   facecolor=clr, edgecolor="none", width=1)
            former_q = former_q + qvalues[:, i]

    # Annotate population info
    if poplist:
        count = 1
        for ppl, vals in enumerate(poplist):
            # Add population delimiting lines
            plt.axvline(x=vals[0], linewidth=1.5, color='black')
            # Add population labels
            # Determine x pos
            xpos = vals[0] - ((vals[0] - poplist[ppl - 1][0]) / 2) if ppl > 0 \
                else vals[0] / 2
            # Draw text
            ax.text(xpos, -0.05, vals[1] if vals[1] else "Pop{}".format(count),
                    rotation=45, va="top", ha="right", fontsize=14,
                    weight="bold")
            count += 1

    for axis in ["top", "bottom", "left", "right"]:
        ax.spines[axis].set_linewidth(2)
        ax.spines[axis].set_color("black")

    plt.yticks([])
    plt.xticks([])

    plt.savefig("{}.svg".format(outfile), bbox_inches="tight")


def main(result_files, fmt, outdir, popfile=None):
    """
    Wrapper function that generates one plot for each K value.
    :return:
    """

    for files in result_files:
        data, pops = dataminer(files, fmt, popfile)
        # Get output file name from input file name
        outfile = os.path.join(outdir, files.split(os.sep)[-1])
        # Create plots
        plotter(data, pops, outfile)

if __name__ == "__main__":
    from sys import argv
    # Usage: structplot.py results_files format outdir
    datafile = []
    datafile.append(argv[1])
    main(datafile, argv[2], argv[3])
