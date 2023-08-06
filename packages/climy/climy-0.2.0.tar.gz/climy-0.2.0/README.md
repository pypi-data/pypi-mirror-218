# climy
Do CLI applications easily.


## Instalation
```shell
$ pip install climy
```

### Basic Usage
```python
from climy import Application, Option, Command


def env_handler(comm: Command):
    print('do every thing with env')
    print(comm)
    print(comm.vars)

    
env_command = Command(
    name='env',
    description='Create a perfect environ to application',
    handler=env_handler
)

app = Application(
    name='acme',
    title='ACME App',
    description='A teste application',
    version='0.1.0',
    option_default_separator=Option.Separators.EQUAL
)
app.add_command(env_command)
app.add_option('host', 'The server allow host IP number.', short='t', var_type='str')
app.add_option('port', 'Service port.', short='p', var_type='int')
app.add_option('path', 'Execution code path.', var_type='str', var_name='path')
app.run()
```
```shell
$ acmesrv --help
ACME App (version 0.1.0)

Usage:
  acme <command> [options] [arguments]

Options:
  -h, --help                Print this help.
  -t, --host=[HOST]         The server allow host IP number.
  -p, --port=[PORT]         Service port.
  --path=[PATH]             Execution code path.

Commands:
  env                       Create a perfect environ to application
```

## Components

### Tables
To print tables quickly, you just need to define a column list with the column title, size and align. 
Then, preparate a data tuple list with the values in the same columns orders. 
Below, an example how to print tables.
```python
from climy.console import ctable


columns = ['ID:10>', 'Name:50', 'Birth:15^', 'Weight:10>', 'Hight:10']
data = [
    (1, 'Mark White', '26/12/1977', 1.75, 80.0),
    (2, 'Eva Wood', '30/11/1983', 1.59, 50.0),
    (3, 'John Apple', '26/06/1917', 1.20, 30.0),
    (4, 'Linda Jansen', '09/05/1961', 1.63, 61.0)
]
ctable(data, columns=columns)
```
And the results:
```
┌──────────┬──────────────────────────────────────────────────┬───────────────┬──────────┬──────────┐
│       ID │ Name                                             │     Birth     │   Weight │ Hight    │
├──────────┼──────────────────────────────────────────────────┼───────────────┼──────────┼──────────┤
│        1 │ Mark White                                       │   26/12/1977  │     1.75 │ 80.0     │
│        2 │ Eva Wood                                         │   30/11/1983  │     1.59 │ 50.0     │
│        3 │ John Apple                                       │   26/06/1917  │      1.2 │ 30.0     │
│        4 │ Linda Jansen                                     │   09/05/1961  │     1.63 │ 61.0     │
└──────────┴──────────────────────────────────────────────────┴───────────────┴──────────┴──────────┘
```

### Progress Bar
You can print progresses bars by using `cprogress` function.

```python
from climy.console import cprogress


cprogress(size=50, max=300.0, value=20.0, color='green')

# ━━━───────────────────────────────────────────────
```
