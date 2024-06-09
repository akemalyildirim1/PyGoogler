# `pygoogler`

Google search CLI.

**Usage**:

```console
$ pygoogler [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `configure`: Update the configuration file.
* `init`: Create an initial configuration file.
* `reset`: Reset the configuration file.
* `search`: Search for the given query.
* `start`: Create an initial configuration file.

## `pygoogler configure`

Update the configuration file.

This will update the configuration file with your custom search
API key and the programmable search engine ID.

**Usage**:

```console
$ pygoogler configure [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `pygoogler init`

Create an initial configuration file.

This will create an initial configuration file with the default values.

**Usage**:

```console
$ pygoogler init [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `pygoogler reset`

Reset the configuration file.

This will reset the configuration file to the initial state.

**Usage**:

```console
$ pygoogler reset [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `pygoogler search`

Search for the given query.

This will search for the given query and display the results.

**Usage**:

```console
$ pygoogler search [OPTIONS] QUERY...
```

**Arguments**:

* `QUERY...`: [required]

**Options**:

* `--detail / --no-detail`: Show the details of the search results.

By default, it will show the details of the
search results.  [default: detail]
* `--help`: Show this message and exit.

## `pygoogler start`

Create an initial configuration file.

This will create an initial configuration file with the default values.

**Usage**:

```console
$ pygoogler start [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
