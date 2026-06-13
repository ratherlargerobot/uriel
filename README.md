# Uriel

By Nathan Rosenquist

https://uriel.foo/

## Overview

A static site generator for the small web.

Named for the archangel Uriel in the novel Unsong, whose job was to perform
the fantastic and mundane work necessary to keep the world functioning.

## Installation

Uriel is a single, standalone Python script. You can just run the script from
any directory, as any user, without installing it or requiring root
privileges. You can even copy it into your project directory, so it stays
with the project.

If you want to install it in a centralized location for all users on a
machine:

```bash
sudo make install
```

## Usage

```bash
uriel <project-root>
```

If the project root is a directory that does not exist, it will be created and
initialized with new project files. Subsequent invocations of the uriel
command against the project root will regenerate the static files of the web
site from the project files.

## Documentation

https://documentation.uriel.foo/

Uriel comes with comprehensive documentation, which is itself in the form of a
Uriel project. You can also view the latest version online at the link above.

The documentation can be read directly. But in addition to that, the project
files that created the documentation also use most of the features of Uriel,
and can be examined to see how the documentation was generated.

The documentation project can be found in the **`documentation/`** directory
of this source code distribution.

Since the documentation is also a Uriel project, it is best viewed as a web
site, through a web server. Fortunately, if you can run Uriel, then you have
everything you need to run a web server to view the documentation.

To view the documentation locally, starting from the current directory:

```bash
cd documentation/public/
python3 -m http.server
```

If you have the `make` command installed, you can also use the `make preview`
target from inside the documentation directory.

Once the Python web server is running, then visit
<a href="http://localhost:8000/">http://localhost:8000/</a> in your web
browser to view the documentation.

## Project Links

[Uriel Web Site](https://uriel.foo/)

[Uriel Documentation](https://documentation.uriel.foo/)

