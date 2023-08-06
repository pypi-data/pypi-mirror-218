# `fm91`

**Usage**:

```console
$ fm91 [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `add-dependency`: Add a dependency to the requirements.txt...
* `add-environment-variable`: Add an environment variable to the .env file.
* `add-subdirectory`: Add a subdirectory to the Python path.
* `create-handler`: Create a new handler file.
* `create-project`: Create a new project directory with the...
* `create-route`: Create a new route file.
* `create-structure`: Create a new structure file.
* `delete-handler`: Delete a handler file.
* `delete-project`: Delete the project directory with the...
* `delete-route`: Delete a route file.
* `delete-structure`: Delete a structure file.
* `remove-dependency`: Remove a dependency from the...
* `remove-environment-variable`: Remove an environment variable from the...
* `remove-subdirectory`: Remove a subdirectory from the Python path.
* `sync`: Impport the project's dependencies,...

## `fm91 add-dependency`

Add a dependency to the requirements.txt file.

**Usage**:

```console
$ fm91 add-dependency [OPTIONS] PROJECT_NAME DEPENDENCY
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `DEPENDENCY`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 add-environment-variable`

Add an environment variable to the .env file.

**Usage**:

```console
$ fm91 add-environment-variable [OPTIONS] PROJECT_NAME VARIABLE
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `VARIABLE`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 add-subdirectory`

Add a subdirectory to the Python path.

**Usage**:

```console
$ fm91 add-subdirectory [OPTIONS] PROJECT_NAME SUBDIRECTORY
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `SUBDIRECTORY`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 create-handler`

Create a new handler file.
    

**Usage**:

```console
$ fm91 create-handler [OPTIONS] PROJECT_NAME HANDLER_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `HANDLER_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 create-project`

Create a new project directory with the given name.

**Usage**:

```console
$ fm91 create-project [OPTIONS] PROJECT_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 create-route`

Create a new route file.

**Usage**:

```console
$ fm91 create-route [OPTIONS] PROJECT_NAME ROUTE_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `ROUTE_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 create-structure`

Create a new structure file.

**Usage**:

```console
$ fm91 create-structure [OPTIONS] PROJECT_NAME STRUCTURE_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `STRUCTURE_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 delete-handler`

Delete a handler file.
    

**Usage**:

```console
$ fm91 delete-handler [OPTIONS] PROJECT_NAME HANDLER_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `HANDLER_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 delete-project`

Delete the project directory with the given name.

**Usage**:

```console
$ fm91 delete-project [OPTIONS] PROJECT_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 delete-route`

Delete a route file.

**Usage**:

```console
$ fm91 delete-route [OPTIONS] PROJECT_NAME ROUTE_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `ROUTE_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 delete-structure`

Delete a structure file.

**Usage**:

```console
$ fm91 delete-structure [OPTIONS] PROJECT_NAME STRUCTURE_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `STRUCTURE_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 remove-dependency`

Remove a dependency from the requirements.txt file.

**Usage**:

```console
$ fm91 remove-dependency [OPTIONS] PROJECT_NAME DEPENDENCY
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `DEPENDENCY`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 remove-environment-variable`

Remove an environment variable from the .env file.

**Usage**:

```console
$ fm91 remove-environment-variable [OPTIONS] PROJECT_NAME VARIABLE
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `VARIABLE`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 remove-subdirectory`

Remove a subdirectory from the Python path.

**Usage**:

```console
$ fm91 remove-subdirectory [OPTIONS] PROJECT_NAME SUBDIRECTORY
```

**Arguments**:

* `PROJECT_NAME`: [required]
* `SUBDIRECTORY`: [required]

**Options**:

* `--help`: Show this message and exit.

## `fm91 sync`

Impport the project's dependencies, subdirectories, and environment variables into main.py.

**Usage**:

```console
$ fm91 sync [OPTIONS] PROJECT_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.
