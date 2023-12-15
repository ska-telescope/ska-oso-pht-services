==========
Quickstart
==========

This project uses Docker containers for development and testing, and
``make`` to provide a consistent UI.

Build a new Docker image and execute the test suite with:

::

    make test

Launch an interactive shell inside a container, with your workspace
visible inside the container, with:

::

  make interactive

To list all available targets, execute make without any arguments, e.g.,

::

    tangodev:ska-oso-pdm $ make

    build                                       build the application image

    down                                        stop develop/test environment and any interactive session

    help                                        show this help.

    interactive                                 start an interactive session using the project image
                                                (caution: R/W mounts source directory to /app)

    lint                                        lint the application (static code analysis)

    test                                        test the application

    up                                          start develop/test environment
