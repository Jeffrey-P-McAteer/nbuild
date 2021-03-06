
# Navy Build

_A modern project-as-code specification, build, testing, and report generation library._

`nbuild` is a library providing the following capabilities:

 - Describe a software project from artifacts (source or binary redistributables) to artifacts (usually programs as `.exe` files)
 - Using these descriptions of the project test and report the following:
    - Correctness
    - Completeness
 - Finally using the software project description and the tests, produce a formal documentation
   describing how to use each tested capability.

This directory holds the `nbuild/` source directory as well as an `examples/` directory showing
how one might use `nbuild` to generate reports about projects.

This library is also available from pypi/`pip`: https://pypi.org/project/nbuild/

Documentation, examples, and a usage gallery is slowly moving from the readme file to https://jeffrey-p-mcateer.github.io/nbuild/site/

# Example Processes

## Process 01

1. A tester uses the `nbuild` library to write `review_proj01.py`,
   which is a formal description of the project deliverables and what the deliverables must do.

2. A contractor submits a project as source code on a USB drive. The code resides in a folder "proj01".

3. The tester runs `python review_proj01.py` and their browser opens to the following report:

![screenshots/proj01-report01.jpg](screenshots/proj01-report01.jpg)

## Process 02

1. A tester uses the `nbuild` library to write `review_nasa_worldwind.py`,
   which is a formal description of a [public mapping library written by NASA](https://worldwind.arc.nasa.gov/).

2. The tester runs `python review_nasa_worldwind.py` and their browser opens to the following report:
  
![screenshots/nasa_worldwind-report01.jpg](screenshots/nasa_worldwind-report01.jpg)

## Process 03

1. A tester uses the `nbuild` library to describe a physical process for testing
   a new artillery loading mechanism in `review_artillery_loading.py`. This requires a person to perform the tests
   and `nbuild` will issue instructions textually. The person doing
   the test will respond to simple "yes or no" questions.

2. The tester runs `python review_artillery_loading.py` and follows the instructions given.
   When completed a report like the following will be generated:
  
![screenshots/artillery_loading-report01.jpg](screenshots/artillery_loading-report01.jpg)


# Plans

 - [ ] Self-service HTTP server (upload `.exe` files, get reports back)
 - [ ] Workflow flowchart generation from project definition
 - [ ] Record runtime
 - [ ] Predict runtime 
 - [ ] Support Maven builds (java)
 - [ ] Support Gradle builds (java)
 - [ ] Support DotNet builds (C\#)
 - [ ] Support partial automation (eg move seamlessly from an automated step to a manual step + vice versa)

# Project Hygiene

You will need [pylint](https://www.pylint.org/) installed to run code analysis below.

You will need [pylint](https://www.pylint.org/) installed to run code analysis below.

One-liners for dependencies:

```bash
python -m pip install --user pylint
python -m pip install --user pdoc3
```

## Code Quality

Run `python do_quality_checks.py` to check the `nbuild` library code quality.

Pass your favorite editor (`subl3` for Sublime 3, `idea` for the IntelliJ IDE)
to the command to have it open at the first line that failed the linter:

```bash
python do_quality_checks.py
# or if you have subl3 installed:
python do_quality_checks.py edit-with subl3
# for IntelliJ customers:
python do_quality_checks.py edit-with idea.exe
```

# Code Documentation

The code is annotated with docstrings, so most python documentation generators
will produce something useful. We use [pdoc](https://pdoc3.github.io/pdoc/) for our
own copies of documentation, which places `.html` files under a `./html/` directory.

```bash
python -m pdoc --html nbuild
# one-liner to open ./html/nbuild/index.html for documentation
python -m pdoc --html --force nbuild && xdg-open ./html/nbuild/index.html
```

# Code license

See [license.txt](license.txt) for details, it contains a copy of the [MIT license](https://en.wikipedia.org/wiki/MIT_License).



