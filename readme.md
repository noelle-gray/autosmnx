# autosmnx:

`autosmnx` is a CLI application to automate the the graphing capabilities of the package `osmnx`. It is testing form only in CLI application form. It currently supports four arguments:

- `--distance, -d` is used to determine the distance used in the Overpass Query.

- `--file, -f` is used to parse the input file path.

- `--output, -o` is used to determine the output file path.

-  `--log, -L` is used to toggle the log mode. Log mode is in strictly testing for branch development.

- `--coordinates, -c` is used to input coordinates manually. This mode is not currently supported and will be fully supported in 0.4.1.

This project hopes to create a CLI module approach to using the `osmnx` package with Overpass API and create a "modular" approach to a simple area topography street network representation.

The project is currently configured to 1km radius plotting. 
