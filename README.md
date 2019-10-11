# Command Help

    usage: harvest.py [-h] [-d | -s] [-v] [-e EXTENSION] [-p] source [source ...]

    Harvests files in one or more directory trees and writes all the content to
    stdout.

    positional arguments:
      source                path to harvest content

    optional arguments:
      -h, --help            show this help message and exit
      -d, --depth-first     sorts the files so the deeper paths comes before the
                            shallow ones, and directories comes before the files
                            (following the pattern used by most file managers and
                            IDEs)
      -s, --shallow-first   sorts the files so the shallow paths comes before the
                            deep ones (the opposite of --depth-first
      -v, --verbose         display errors (errors are written to stderr)
      -e EXTENSION, --extension EXTENSION
                            set a file extension to consider
      -p, --paths-only      write only the file paths to stdout

    Multiple extensions can be provided by repeating the '-e' extension argument
    (eg. '-e .txt -e .readme'). By default the files are sorted using alphabetial
    order. To sort them by depth use --depth-first or --shallow-first arguments.
