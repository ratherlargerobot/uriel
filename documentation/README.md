# Uriel Documentation

[https://documentation.uriel.foo/](https://documentation.uriel.foo/)

## Overview

This is the documentation for Uriel, a static site generator for the small
web.

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
cd public/
python3 -m http.server
```

If you have the `make` command installed, you can also use the `make preview`
target from inside this documentation directory.

Once the Python web server is running, then visit
<a href="http://localhost:8000/">http://localhost:8000/</a> in your web
browser to view the documentation.

