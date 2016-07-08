# Usage
This section describes how to use *Structure_threader*.

These are the arguments the program currently takes:

* K (-K)
* Replicates (ignored for fastStructure; -R)
* Input file (-i)
* Output dir (-o)
* Number of threads (-t)
* Program location - you have to pass one and only of the following arguments:
    * Structure location (if you want to run "structure"; -st)
    * fastStructure location (if you want to run "fastStructure"; -fs)
* Logging (optional - useful when problems arise; --log)
* Minimum K (optional - use as a start value for "K" - by default the value is 1; --min_K)
* No-tests (optional - use this if you do not want to run the BestK tests; --no-tests)
* No-plots (optional - use this if you do not want to draw plots; --no-plots)
* Popfile (optional - use this if you want to name your populations in the plot. Should be a text file with 3 columns, one for population name, one for number of individuals represented in that population and one for the population position in the input file. This effectively allows the plot to be drawn in any chosen order.)

Example run:

```
structure_threader.py -K Ks -R replicates -i infile -o outpath -t num_of_threads -st path_to_structure
```

Where -K is the number of "Ks" to run, -R is the number of replicate runs for
each value of "K", -i is the input file for STRUCTURE, -o is the directory where the output results should be stored,
-t is the number of threads to use and -p the path for the STRUCTURE binary.

The program should be run in the same directory where the files "mainparams" and
"extraparams" for your STRUCTURE run are placed. Please see [Installation](install.md) for information on how to achieve this.


## Using a "popfile"
*Structure_threader* can build your structure plots with labels and in a specified order. For that you have to provide a "popfile" (--pop option). This file consists of the following 3 columns: "Population name", "Number of individuals in the population", "Order of the population in the input file".
Here is an example:

```
Location_1  20  1
Location_2  21  2
Location_3  11  3
```

This example file contains 3 populations, with 20, 21 and 11 individuals. The numbers "1", "2" and "3" are the order of the populations in the input file.
If you want to draw the plot in a different order than what was provided on the input file, you have to reorder the lines. For the sake of the example, let's say that you wish to plot your data, switching the place of Locations 3 and 2. The input file would look like this:

```
Location_1  20  1
Location_3  11  3
Location_2  21  2
```

You can use any order you like using this scheme. Also note that the "split bars" that split the populations in your plot will correspond to the number provided in column 2.


## fastStrucutre Warning:
If running fastStructure, keep in mind that this program requires your input
file to have each individual represented in two rows (one for each allele), and
six "bogus" columns before the actual data. **No Header is allowed**. Here is a short example:

```
Ind1    col1  col2  col3  col4  col5 1    3   1   4
Ind1    col1  col2  col3  col4  col5 1    3   2   4
Ind2    col1  col2  col3  col4  col5 1    2   1   4
Ind2    col1  col2  col3  col4  col5 1    2   1   3

```

Don't forget to look at the [Outputs section](output.md) for information on how the data is presented after a successful (or not) run.