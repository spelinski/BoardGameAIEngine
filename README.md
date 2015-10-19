Battleline AI Engine
====================

This is a python engine for the board game BattleLine.

Setting up your Environment
---------------------------
To install all test dependencies and create a development environment, we recommend the usage of virtualenv.

To install virtualenv:

    > pip install virtualenv

Then to setup a virtualenv for the project which includes all test dependencies:

    > cd <projectdir>
    > virtualenv venv
    > source venv/bin/activate
    > pip install -r test_requirements.txt

Running the Tests
-----------------

This project includes a makefile which automates most developer tasks. To run the tests, simply setup your virtual environment (see above) and:

    > make unit_test

To run acceptance tests, run the acceptance task

    > make acceptance_test


To run all tests

    > make test

To generate a coverage report, simply run the coverage task:

    > make coverage

To format the project according to [pep8](https://www.python.org/dev/peps/pep-0008/) standards, use the format ask:

    > make format

All of the tasks are run by default if no task is specified:

    > make

Setting up the Git Pre-commit Hooks
-----------------------------------

Some pre-commit hooks are included with the project to ensure that committed code conforms to the standards of the project. To enable those hooks simply copy (or symlink) the gitHooks folder to .git/hooks/.
