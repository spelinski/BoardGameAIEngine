Running the Tests
-----------------

This project includes a makefile which automates most developer tasks. To run the tests, simply setup your virtual environment (see above) and:

    > make unit_test
    
To generate a coverage report, simply run the coverage task:

    > make coverage
    
To format the project according to [pep8](https://www.python.org/dev/peps/pep-0008/) standards, use the format ask:

    > make format
    
All of the tasks are run by default if no task is specified:

    > make

Setting up the Git Pre-commit Hooks
-----------------------------------

Some pre-commit hooks are included with the project to ensure that committed code conforms to the standards of the project. To enable those hooks simply copy (or symlink) the gitHooks folder to .git/hooks/.

