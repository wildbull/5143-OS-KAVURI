
MADDY_SHELL
A command prompt similar to shell,  implemented completely in Python.

############## Usage Instructions ###############
```
For development comfort, we have put some constraints regarding command syntax
    1. Only out-ward redirects are supported , that is , ">" and ">>". In-ward redirects are not supported.
    2. Only one redirect is expected per command
    3. Multiple pipes can requested in any command, but pipes should never succed redirects.

    A command with pipes and redirects can look like one of these ::

        1. Only redirect :
            cat some_file > some_other_file

        2. Only pipes :
            cat some_file | grep some_string | wc -l

        3. Pipes with redirects :
            cat some_file | grep some_string | wc -l >> some_other_file
```
##################################################

intorduction :
```
    1. Commads are fetched and loaded from maddy_commands dir.
    2. Whenever you want to add a new command, please copy the command's implementation into maddy_commands dir 
    3. "ldcmds" command with trigger maddy_shell to fetch newly added commands from maddy_commands dir
    4. History is maintained in user home. ie, ~/.maddy_history
```
#################################################

Project structure :: 
```
.
├── README.md
├── commands.py
├── globals.py
├── history.py
├── mad_os.py
├── maddy.py
├── maddy.py_backup
├── maddy_commands
│   ├── Commands.py
│   ├── cat.py
│   ├── cd.py
│   ├── chmod.py
│   ├── cp.py
│   ├── grep.py
│   ├── head.py
│   ├── history.py
│   ├── less.py
│   ├── ls.py
│   ├── mkdir.py
│   ├── mv.py
│   ├── pwd.py
│   ├── rm.py
│   ├── tail.py
│   ├── test.txt
│   ├── test_dir
│   │   └── test_file
│   ├── test_file
│   └── wc.py
├── my_commands.py
├── redirect_test
├── replit_example.py
├── setup.py
├── test_file
└── utilities.py

2 directories, 32 files
```
