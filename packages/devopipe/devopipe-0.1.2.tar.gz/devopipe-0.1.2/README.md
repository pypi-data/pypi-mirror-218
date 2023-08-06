# `devopipe`

**Usage**:

```console
$ devopipe [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `goodbye`
* `hello`
* `init`: Prompts the user with a series of...
* `template`
* `version`

## `devopipe goodbye`

**Usage**:

```console
$ devopipe goodbye [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `devopipe hello`

**Usage**:

```console
$ devopipe hello [OPTIONS] NAME IQ
```

**Arguments**:

* `NAME`: [required]
* `IQ`: [required]

**Options**:

* `--display-iq / --no-display-iq`: [default: display-iq]
* `--age INTEGER`
* `--help`: Show this message and exit.

## `devopipe init`

Prompts the user with a series of questions about setting up a CI/CD pipeline.

**Usage**:

```console
$ devopipe init [OPTIONS]
```

**Options**:

* `--file TEXT`
* `--help`: Show this message and exit.

## `devopipe template`

**Usage**:

```console
$ devopipe template [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `devopipe version`

**Usage**:

```console
$ devopipe version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
