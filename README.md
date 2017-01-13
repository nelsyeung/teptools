# TEP Tools

[![Build Status](https://travis-ci.org/nelsyeung/teptools.svg?branch=master)](https://travis-ci.org/nelsyeung/teptools)
[![Coverage
Status](https://coveralls.io/repos/github/nelsyeung/teptools/badge.svg?branch=master)](https://coveralls.io/github/nelsyeung/teptools?branch=master)

Quick and easy to use tools for [ONETEP](http://www.onetep.org), in a single package.

## Table of Contents
1. [Features](#features)
1. [Why was this made?](#why-was-this-made)
1. [Installation](#installation)
1. [Basic Usage](#basic-usage)
1. [Tab Completion](#tab-completion)
1. [Fuzzy Search](#fuzzy-search)
1. [Modules](#create)
    1. [Create](#create)
    1. [Run](#run)
    1. [Watch](#watch)
    1. [Summarise](#summarise)
    1. [Geomconv](#geomconv)
    1. [Enerconv](#enerconv)
    1. [Check](#check)
    1. [Error](#error)
    1. [Update](#update)
1. [Configurations](#configurations)
1. [Tips and Tricks](#tips-and-tricks)
1. [Contributing](#contributing)
1. [Todo](#todo)
1. [License](#license)

## Features
- [Create](#create) - Create input files from templates with automatic potfiles detection. It can also
  generate convergence tests.
- [Run](#run) - Run ONETEP from a configured path. This module includes automatic reading of input file
  and can automatically redirect output to a file with an appropriate name. It can also help with
  running different versions of ONETEP easily, if they are set up in your configuration file.
- [Watch](#watch) - Watches ONETEP jobs and write out a simple log or notify job status via email when
  there's a change of state in the job. (Still require testing)
- [Summarise](#summarise) - Based on the original
  [summarise](http://www.onetep.org/onetep/pmwiki/uploads/Main/Utilities/summarise) script which
  extracts the results of the NGWF CG optimisation steps. This is faster with automatic output file
  detection, automatic vimdiff for multiple output files and side-by-side view for two output files.
- [Geomconv](#geomconv) - Based on the original
  [geomconv](http://www.onetep.org/onetep/pmwiki/uploads/Main/Utilities/geomconv) script which
  extracts the convergence indicators of a ONETEP BFGS geometry optimisation calculation. This is
  faster with automatic output file detection, automatic vimdiff for multiple output files and
  side-by-side view for two output files.
- [Enerconv](#enerconv) - Extracts the final converged energy from an output file. This is especially useful
  for getting all the energies from convergence tests.
- [Check](#check) - Check input files for potential errors.
- [Error](#error) - Nothing special, just read error files without typing in a path.
- [Update](#update) - Update TEP Tools.

**[⬆ back to top](#table-of-contents)**

## Why was this made?
There are already many scripts available for ONETEP, so what's the point of this?

- No longer need to *discover* different useful tools then install them separately.
- Testability - Most of the modules have tests with a coverage of over 95% overall.
- Extensibility - This was made with developers in mind. Any extra modules can be added by simply
placing the script in the teptools directory and everything will just work.
- Flexibility - You can configure how you want the modules to behave.
- Avoid any script name clashes.
- This is open sourced so that everyone can share their tools for ONETEP easily.
- All the modules come with its own documentation.
- Easy to update.

**[⬆ back to top](#table-of-contents)**

## Installation
This tool requires Python 3, although you may find that it works with Python 2.7, but it will not be
supported fully.

1. Download this package using `git`:

    ```sh
    $ git clone https://github.com/nelsyeung/teptools.git
    ```

    or you can just download it as a zip file and extract it.

2. Change to the teptools directory then run the install script:

    ```sh
    $ cd teptools
    $ ./install.py
    ```

    You will get a confirmation message, just enter `y` to proceed.

    The default install location is `$HOME/.teptools`. If you want to change this, you can use the
    `--prefix` option with the install script.

    ```sh
    $ ./install --prefix /some/other/location
    ```

    This will install teptools to `/some/other/location/.teptools`.

    If this is a first time installation, a configuration file will also be installed to
    `$HOME/.teptoolsrc`.

**[⬆ back to top](#table-of-contents)**

## Basic Usage
There are two ways to use this tool, please use only one of the below methods.

### 1. Source the `tep.sh` script (recommended)
This enables the full teptools features including [tab completion](#tab-completion) and [fuzzy
search](#fuzzy-search). It also prevents any name clash with other executables.

```sh
$ source $HOME/.teptools/tep.sh
```

It is recommended that you add this to your `.bashrc` or `.bash_profile`.

Now you can run `tep` to execute different modules.

```sh
$ tep  # Run the default action
$ tep create  # Run the create module
$ tep summarise  # Run the summarise module
$ tep update  # Update teptools
```

### 2. Add teptools to `$PATH` (not recommended)
You can simply add the installed directory to your `$PATH` variable to make the individual module
executable anywhere without typing in the full path. This is not recommended as it can introduce
name clash with other scripts.

Add this to your `.bashrc` or `.bash_profile`:

```sh
$ export PATH="$PATH:$HOME/.teptools"
```

Now you can execute the individual scripts:

```sh
$ create  # Run the create module
$ summarise  # Run the summarise module
```

**[⬆ back to top](#table-of-contents)**

## Tab Completion
If you are using this tool with the [Source the `tep.sh`
script](#1-source-the-tepsh-script-recommended) option, you can perform tab completion for the
individual tool and their available options.

```sh
# Typing this:
$ tep sum<Tab>
# will turn into summarise (provided that no other scripts start with the same characters):
$ tep summarise
```

Once the script is completed you can also tab complete the available options.

```sh
# Typing this:
$ tep summarise --<Tab>
# will give the summarise script's available options.
# or you can tab complete the option for you:
$ tep summarise --vi<Tab>
# will give
$ tep summarise --vimdiff
```

**[⬆ back to top](#table-of-contents)**

## Fuzzy Search
If you are using this tool with the [Source the `tep.sh`
script](#1-source-the-tepsh-script-recommended) option, you can use this fuzzy search feature to
shorten typing and tab completion.

This feature allows you to type in any number of letters in the right order to execute a script or
to perform tab completion.

```sh
# Typing this:
$ tep gc<Tab>
# will turn into (provided that no other scripts have roughly the same name):
$ tep geomconv
# or you can simply execute the script without tab completion:
$ tep gc<Enter>
```

**[⬆ back to top](#table-of-contents)**

## Create
> Create a ONETEP input file from a template with the correct potential files. It can also generate
convergence tests.

**Usage**
```sh
create [options] [-e element [element ...]] [name]

# Example:
create -e Mo S foo # Create foo.dat file with the element Mo and S.
```

**Available options**
```sh
-h, --help          show the help message and exit
-t index, --template index
                    Template index from your config file templates (default: 1)
-e element [element ...], --elements element [element ...]
                    All the elements in the system
-c CELL, --cell CELL  Cell file for automatically inputting the lattice_cart block
                    and the positions_abs block
--conv-tests {cutoff,radius} [{cutoff,radius} ...]
                    Generate energy cutoff and NGWF radius convergence tests

# Examples:
create MoS2 -t 2 -e Mo S                       # Create MoS2.dat file using your second template.
create MoS2 -e Mo S -c MoS2.cell               # Create MoS2.dat file with the all the information filled in.
create MoS2 -e Mo S --conv-tests cutoff radius # Create both cutoff and NGWF convergence tests.
```

**Notes**

- Template file must have empty block statements for automatic filling from cell file or pot file.

    Your template file should look like this:
    
    ```sh
    task: singlepoint
    # Other ONETEP options ...

    %block lattice_cart
    %endblock lattice_cart

    %block species
    %endblock species

    %block species_pot
    %endblock species_pot
    ```

**[⬆ back to top](#table-of-contents)**

## Run
> Run ONETEP from the configured path. This module includes automatic reading of input file and can
redirect output to a file with an appropriate name. It can also help with running different
versions of ONETEP easily, if they are set up in your configuration file.

**Usage**
```sh
run [options] [inpfile [inpfile ...]]

# Example:
run         # Run ONETEP with all the .dat files within the current directory.
run foo.dat # Run ONETEP with foo.dat.
```

**Available options**
```sh
-h, --help            show the help message and exit
-o, --output          Write the output into a new file
--no-output           Prevent writing the output into a new file
-a ARGS [ARGS ...], --args ARGS [ARGS ...]
                      A dash argument to be passed to ONETEP (e.g., --help all).
                      Whatever the first word is will be prefixed by either
                      a single dash, for a single letter, or a double dash, otherwise.
                      Example: "tep run -a h all" will turn into "onetep -h all"
-v VERSION, --version VERSION
                      The version of ONETEP you want to execute.
                      This is not the version number of ONETEP but the index of the
                      paths within your configuration file. The index starts from 1,
                      so if you would like to run the first path set, use "-v 1".

# Examples:
run -o # Run and write output to ${inpfile_name}.out.
run -o foo # Run ONETEP with foo.dat and output to foo.out.
run -a help all # Print ONETEP help message.
run -v 2 # Run ONETEP from the second path inside your config file.
```

**[⬆ back to top](#table-of-contents)**

## Watch
**This module still require more tests and it will, by default, not have email notifications. If you
would like to help test this and activate email notifications, please email Nelson Yeung**

> Watch the specified ONETEP jobs and write out a simple log or notify the user via email with
relevant information.

**Usage**
```sh
watch [options] [dir [dir ...]]

# Example:
watch         # Watch the current directory.
watch foo bar # Watch the foo and bar directory.
watch *       # Watch all the directories within the current directory.
```

**Available options**
```sh
-h, --help   show the help message and exit
-e, --email  Send an email to the user once a job is completed or errored.
--no-email   Prevent sending an email.

# Examples:
watch -e # Watch the current directory and send email to the user's email set in the config file.
```

**[⬆ back to top](#table-of-contents)**

## Summarise
> Extracts the results of the NGWF CG optimisation steps from an output file (which may still be
running) and output them in a format as if you were running with output_detail=BRIEF or looking at
the calculation summary.

**Usage**
```sh
summarise [options] [outfile [outfile ...]]

# Examples:
summarise                 # Print summary for all the .out files within the current directory.
summarise foodir          # Print summary for all the .out files within the foodir directory.
summarise foo.out         # Print summary for foo.out.
summarise foo.out bar.out # Print two summaries side-by-side.
```

**Available options**
```sh
-h, --help      show the help message and exit
-vd, --vimdiff  Open multiple outputs in vimdiff
--no-vimdiff    Prevent opening multiple outputs in vimdiff
-o, --output    Write each output into its own file
--no-output     Prevent writing each output into its own file

# Examples:
summarise -vd foo.out bar.out # Print two summaries in vimdiff mode.
summaries -o foo.out bar.out  # Print and output .summary files for foo.out and bar.out.
```

**[⬆ back to top](#table-of-contents)**

## Geomconv
> Extracts the convergence indicators of a ONETEP BFGS geometry optimisation calculation from the
output file, and compares them to the convergence tolerances. The results are coloured to indicate
which parameters are converged and which are not.

**Usage**
```sh
geomconv [options] [outfile [outfile ...]]

# Examples:
geomconv                 # Print geomconv for all the .out files within the current directory.
geomconv foodir          # Print geomconv for all the .out files within the foodir directory.
geomconv foo.out         # Print geomconv for foo.out.
geomconv foo.out bar.out # Print two geomconv side-by-side.
```

**Available options**
```sh
-h, --help      show the help message and exit
```

## Enerconv
> Extracts the final converged energy from an output file and detects whether it's actually
converged. This is especially useful for getting all the energies from convergence tests.

**Usage**
```sh
enerconv [options] [outfile [outfile ...]]

# Examples:
enerconv         # Print converged energy for all the .out files within the current directory.
enerconv foodir  # Print enerconv for all the .out files within the foodir directory.
enerconv foo.out # Print enerconv for foo.out.
enerconv *       # Print the converged energy from all the subdirectories.
```

**Available options**
```sh
-h, --help      show the help message and exit
```

**[⬆ back to top](#table-of-contents)**

## check
> Check input file for potential errors.

**Usage**
```sh
check [options] [outfile [outfile ...]]

# Examples:
enerconv         # Check all the input files within the current directory.
enerconv foodir  # Check all the .dat files within the foodir directory.
enerconv foo.dat # Check the foo.dat file within the current directory.
enerconv *       # Check the input files from all the subdirectories.
```

**Available options**
```sh
-h, --help      show the help message and exit
```

**[⬆ back to top](#table-of-contents)**

## Error
> Absolutely nothing special, I just find myself reading the error file quite a bit and thus wanting
to simplify the command. This simply performs `more *.error_message`.

**[⬆ back to top](#table-of-contents)**

## Update
> Update teptools if necessary.

**Usage**
```sh
update [options]
```

**Available options**
```sh
-h, --help   show this help message and exit
-f, --force  Ignore version checking and update from GitHub directly.

# Example:
update -f # If version is messed up, you can update with this.
```

**[⬆ back to top](#table-of-contents)**

## Configurations
You can configure how each module behaves using a `.teptoolsrc` file. When you first install
teptools, this file should've been created in your home directory. If not, you can just create one.
This file must be inside your home directory `$HOME`.

**Example configuration file**
```ini
[DEFAULT]
# Default action when running the `tep` command.
action =
# Input file extension for automatic file detection.
inpfile_ext = dat
# Ouput file extension for automatic file detection.
outfile_ext = out

[create]
# Command line arguments to be parsed into the individual module.
options =
# Input file templates.
templates = /path/to/input/file/template1,
            /path/to/input/file/template2
# Pot files directory for automatically filling in pot files for the elements.
potdir = /path/to/potfiles/dir
# Default NGWF radius.
ngwf_radius = 10.0

[run]
options =
# ONETEP execution paths.
paths = /path/to/onetep/executable1,
        /path/to/onetep/executable2

[watch]
options =
# Email address for email notifications. Leave empty if you want to disable it.
email =
# How often you want the directories to be checked in seconds.
interval = 3600

[summarise]
options =

[geomconv]

[enerconv]
```

**Some notes:**

- You cannot add inline comments (i.e., you can't have `email = # comment`).

- Each module has its own section denoted as `[module]`.

- Any options can be placed inside the `[DEFAULT]` section.
    Example:

    ```ini
    [DEFAULT]
    email = foo@bar.com

    [watch]
    interval = 3600
    ```

    The watch module will now read the email address in `[DEFAULT]`.

- Placing options inside a `[module]` section will override the ones in the `[DEFAULT]` section.
    Example:

    ```ini
    [DEFAULT]
    inpfile_ext = dat

    [summarise]
    inpfile_ext = inp
    ```

    When running summarise, `inpfile_ext` will read as `inp`.

**[⬆ back to top](#table-of-contents)**

## Tips and Tricks
1. Set up default action for your most used module.

    For example, if you use `summarise` more often than other modules you should set `action =
    summarise`, so now you can simply run `tep` to execute the `summarise` script.

1. Take advantage of [fuzzy search](#fuzzy-search).

    For example, you might want to run the following commands to execute different scripts:
    ```
    tep c   # create
    tep r   # run
    tep err # error
    tep s   # summarise
    tep w   # watch
    tep gc  # geomconv
    tep ec  # enerconv
    ```

1. You can use your environment variable for all the paths. For example, you can set `templates =
   $FOO/bar.dat` or `potdir = ~/pot`.

1. You can supply directories instead of files for all the modules that have file detection.

    For example you can run the following commands:
    
    ```sh
    tep s foodir bardir foobardir # Read all the .out files within those directories.
    tep s * # Read all the .out files inside all the sub directories and the current directory.
    # Similarly for other modules:
    tep gc foodir bardir foobardir
    tep gc *
    tep ec foodir bardir
    ```



**[⬆ back to top](#table-of-contents)**

## Contributing

I love contributions. I mean that's the reason why I've created this the first place, to make it
easy and allow more people to make ONETEP tooling better. Found a bug, a spelling mistake, got a
new tool, or just want to add a cat to the readme? Submit a pull request!

If you find yourself doing the same thing over and over again, just write a script and add it to
teptools so that everyone can use it!

Found a bug? Just submit it through [issues](https://github.com/nelsyeung/teptools/issues). If you
don't have a GitHub account and don't want one (why?!), you can just email the author of the module.

### Developers
1. Fork this repository to your own GitHub.
1. Clone your newly forked repository.
1. Install necessary developers packages `pip install -r requirements.txt`.
1. You may want to add your fork to [Travis CI](https://travis-ci.org/) for automated testing.
1. Create a new branch following the [feature branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow):
    - New module - `feature/modulename`
    - Bug fix - `fix/issuename`
    - Update docs - Just use the master branch
1. Get hacking. You will find that you just need to add your new and exciting tool to the `teptools`
directory and everything will just work. No need to edit `install.sh` or `tep.sh`
1. Submit a pull request.

**Each pull request must:**

- Pass the automated tests ([Travis CI](https://travis-ci.org/)). You can run tests locally using
`./runtests`.
- Conform to the `.editorconfig` settings. Get yourself an [editorconfig](http://editorconfig.org/)
plugin for your favourite editor to make sure of this.
- Conform to the [Flake8](http://flake8.pycqa.org/en/latest/) style guide for Python modules.
- If you are adding a module, you must add a documentation to this file.
- If you are adding a module, you must write tests with at least 95% coverage to your code.
- New modules must be inside the `teptools` directory.

**[⬆ back to top](#table-of-contents)**

## Todo
- **Check** - Check input files for defects without using ONETEP.
- Organise the docs better.
- Move to Go for complete cross platform support?
- Refactor.
- Write integration tests.

**[⬆ back to top](#table-of-contents)**

## License

[MIT license](http://opensource.org/licenses/MIT.php)
