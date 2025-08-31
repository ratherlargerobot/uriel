# uriel

By Nathan Rosenquist

[https://nathanrosenquist.com/uriel/](https://nathanrosenquist.com/uriel/)

## Overview

Yet another static site generator.

Named for the archangel Uriel in the novel Unsong, whose job was to perform
the fantastic and mundane work necessary to keep the world functioning.

## Installation

uriel is a single, standalone Python script. You can just run the script from
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

## Organization and Structure

The project root has the following top-level directories:

- **`templates/`** - templates to merge with dynamic content
- **`nodes/`** - dynamic content nodes to merge with templates
- **`lib/`** - user-defined Python code
- **`static/`** - static content to copy to the web site unmodified
- **`public/`** - rendered web site

## Templates

Templates support substitution parameters:

### `include`

_Syntax:_
```
{{ include : <template> }}
```

_Example:_
```
{{include:some_template_name.html}}
```

The template name is a file in the templates directory. Includes are recursive.

### `value`

_Syntax:_
```
{{ value : <parameter-name> }}
```

_Example:_
```
{{value:title}}
```

The named parameter is pulled out of the Node headers. For example, if a
dynamic node has a "Title: Foo" header, then the example above resolves to
"Foo".

You can make up any parameter name you want, set it in the node headers, and
reference it in the templates or nodes as a substitution parameter.

The value is HTML escaped.

### `value-unescaped`

_Syntax:_
```
{{ value-unescaped : <parameter-name> }}
```

_Example:_
```
{{value-unescaped:title}}
```

Identical to the `{{value:foo}}` substitution parameter, but the value is not
HTML escaped.

### `breadcrumbs`

_Syntax:_
```
{{ breadcrumbs : * }}
```

_Example:_
```
{{breadcrumbs:*}}
```

Prints out HTML breadcrumb navigation links for the node.

### `created`

_Syntax:_
```
{{ created : <strftime-format-string> }}
```

_Example:_
```
{{created:%B %d, %Y}}
```

Prints out the node creation date using the format string.

### `modified`

_Syntax:_
```
{{ modified : <strftime-format-string> }}
```

_Example:_
```
{{modified:%B %d, %Y}}
```

Prints out the node modification date using the format string.

### `static-url`

_Syntax:_
```
{{ static-url : <target-url-path> }}
```

_Examples:_
```
{{static-url:foo.jpg}}
{{static-url:/favicon.ico}}
{{static-url:/foo/bar/quux.jpg}}
```

Prints out the URL for the target file.

If a path is specified without a leading slash, it is relative to the location
of the URL of the node on the site.

If a path is specified with a leading slash, it is specified relative to the
public root of the site.

Note that directory traversal via `../` is not allowed. However, specifying a
file in a subdirectory via `foo/bar.jpg` is allowed.

The benefit of referring to a static URL using this approach is that, if the
target path is not found on the filesystem, this will generate a visible error
when you try to build the site.

### `static-hash-url`

_Syntax:_
```
{{ static-hash-url : <target-url-path> }}
```

**Examples:**
```
{{static-hash-url:foo.css}}
{{static-hash-url:/css/main.css}}
{{static-hash-url:/css/photos/gallery.css}}
```

Causes the target file to be copied to a dynamically generated copy of the
file in the same directory, using a hash of the file contents as the file
name. For example, if `/css/main.css` is the target path, and
`md5sum css/main.css` hashes to `"d41d8cd98f00b204e9800998ecf8427e"`, then a
file named `css/d41d8cd98f00b204e9800998ecf8427e.css` will be generated the
first time this parameter is referenced, and the URL path returned will be to
`/css/d41d8cd98f00b204e9800998ecf8427e.css`.

The point of this is to force web browsers to load a new version of the file
when the content changes. Recommended for CSS and JavaScript files to avoid
browser caching issues.

### `rss`

_Syntax:_
```
{{ rss : url }}
```

_Example:_
```
{{rss:url}}
```

Prints out the canonical RSS URL.

### `node:body`

_Syntax:_
```
{{ node : body }}
```

_Example:_
```
{{node:body}}
```

Includes the body portion of a node in the template.

### `node:url`

_Syntax:_
```
{{ node : url }}
```

_Example:_
```
{{node:url}}
```

Prints out the URL for the current node.

### `node:name`

_Syntax:_
```
{{ node : name }}
```

_Example:_
```
{{node:name}}
```

Prints out the name of the current node, e.g. (index, foo).

### `node:title`

_Syntax:_
```
{{ node : title }}
```

_Example:_
```
{{node:title}}
```

Prints out the value of the "Title" header for the current node, or a display
formatted version of the node name if the title is not set.

### `node:link`

_Syntax:_
```
{{ node : link }}
```

_Example:_
```
{{node:link}}
```

Prints out an HTML text link to the current node, using its title.

### `node-url`

_Syntax:_
```
{{ node-url : <target-node-path> }}
```

_Example:_
```
{{node-url:foo/bar}}
```

Prints out the URL for the target node.

### `node-name`

_Syntax:_
```
{{ node-name : <target-node-title> }}
```

_Example:_
```
{{node-name:foo/bar}}
```

Prints out the name for the target node (e.g. bar).

### `node-title`

_Syntax:_
```
{{ node-title : <target-node-title> }}
```

_Example:_
```
{{node-title:foo/bar}}
```

Prints out the value of the "Title" header for the target node, or the node
name if title is not set.

### `node-link`

_Syntax:_
```
{{ node-link : <target-node-path> }}
```

_Example:_
```
{{node-link:foo/bar}}
```

Prints out an HTML text link to the target node, using its title.

### `node-list`

_Syntax:_
```
{{ node-list : * }}
```

_Example:_
```
{{node-list:*}}
```

List all of the child nodes underneath the current node, with links to their
URLs, using the node titles.

Nodes are sorted so that the newest nodes are listed first.

More precisely, the sort order is:
- created time descending
- modified time descending
- title ascending
- url ascending

All nodes have modified times, but nodes only have created times if the
Created header is explicitly set. If nodes are compared and some of them have
created times and others don't, the sort ordering will preferentially try
created times, but compare them to modified times if that's all that is
available.

### `tag-list`

_Syntax:_
```
{{ tag-list : * }}
```

_Example:_
```
{{tag-list:*}}
```

A value of `*` lists all of the tags that are relevant to the node or
template. This is context sensitive.

In the Tag-Node (e.g. the root of the tag index), this parameter will list all
of the tags in alphabetical order, with links to virtual nodes for each tag
that exists.

In the virtual nodes under the tag node, this parameter will list all of the
pages associated with that tag, in descending order by date.

On a regular node that is not the Tag-Node or one of its virtual children,
this parameter will list all of the tags that the given node references in the
Tags header.

### `soju`

_Syntax:_
```
{{ soju : <python-code-in-soju-module> }}
```

_Example:_
```
{{soju:hello(node)}}
```

`lib/soju.py` is a Python module that allows user-defined handlers to run
during parameter substitution.

The rvalue for this parameter will be executed as a function in the soju
module. The user-defined function is expected to return a string, which will
be included in the output in place of the substitution parameter.

For example, this substitution parameter:
```
{{soju:foo()}}
```

Gets turned into this when it is called:
```python
soju.foo()
```

The following symbols are exported into the soju module at runtime:

- **`uriel`** - The uriel module
- **`SojuError`** - Exception class that soju functions can raise if you want
  to cause an error, but don't need a stack trace.
- **`log(s)`** - log method. Logs the string to stderr, and prepends it with
  "soju: " to help identify the source of the error during troubleshooting.
- **`escape(s)`** - Accepts an unescaped string, and returns an HTML escaped
  string.

The following symbols are available to pass into soju functions as arguments
from within nodes and templates:

- **`page`** - A reference to the uriel Page instance calling this code.
- **`node`** - A reference to the uriel Node instance being rendered.
- **`project_root`** - Path to the project root directory.
- **`use_canonical_url`** - Boolean indicating whether canonical URLs are
  enabled in the current context. Generally canonical URLs are not enabled
  when rendering the main pages on the site, but are enabled when rendering
  the RSS feed.

The return value from a soju function is not HTML escaped. Any content that
needs to be HTML escaped should be run through the `escape()` function.

## Nodes

Nodes contain dynamic content to merge with templates.

This is the content of your site, that gets merged with the templates.

The format of a node file is similar to HTTP or email. It optionally contains
headers of the form "Key: value", one per line, followed by a blank line,
followed by the body contents of the node.

Headers are converted to lowercase internally, and can be referenced in
templates using the `{{ value : <header-name> }}` substitution parameter. You
can make up your own headers, and reference them in nodes and templates. For
example, if you set this header on a node:

```
Foo: bar
```

Then you can reference that value later in a node or template like so:

```
{{value:foo}}
```

In the example above, the `{{value:foo}}` substitution parameter would
evaluate to "bar" when the site is generated.

All headers are inherited by child nodes, unless overridden by the child
nodes. For example, setting a "Foo: bar" header in the index node will cause
`{{value:foo}}` to evaluate to "bar" in every node on the site, unless
overridden at a lower level.

There are also some headers that are treated specially. While they can also
be used as values, other parts of the system recognize them.

### Special Headers

| Header | Purpose |
|--------|---------|
| **Title** | Sets the title of the node, as returned by the `{{node:title}}` and `{{node-title:<node-path>}}` parameters.<br><br>As a special case, the "Title" is not inherited by child nodes, because titles should not all be identical by default.<br><br>If the title is not set, a default title is created based on the node name. |
| **Created** | Explicitly sets the time a node was created. If set, must be in ISO 8601 format. There is no default value.<br><br>The GNU `date` command has an ISO 8601 formatting option (`date -Iseconds` or `date -Is`).<br><br>The BSD `date` command does not have an ISO 8601 formatting option. You can get the date and time (without the time zone) in ISO 8601 format using `date +%FT%T`. |
| **Modified** | Explicitly sets the time a node was modified. If set, must be in ISO 8601 format. If not set, the mtime on the node file will be used instead.<br><br>See documentation for the "Created" header for additional hints about formatting the date. |
| **Escape-Title** | If set, this header controls whether the value of the Title header should be automatically escaped. "true" and "false" are the only valid settings (without quotes). The default value is true. |
| **Template** | Specifies the template to use to render the node.<br><br>If not specified, the default.html template is used.<br><br>If the value of template is set to "null", then no template will be used (unless a template called "null" is created under the templates directory). |
| **Format** | If set to "text", node page body will have `<br>` tags appended to the end of each line. |
| **Breadcrumb-Separator** | If set, this value will be used as a separator in HTML breadcrumbs. The default value is "&raquo;" (without quotes). |
| **Breadcrumb-Separator-Spaces** | If set, this header controls whether spaces are included between breadcrumbs and breadcrumb separators. "true" and "false" are the only valid settings (without quotes). The default value is true. |
| **Flat-URL** | If set, this header controls whether the URL for a node is flat (at the top level of the site), or whether it is placed in a directory matching its node path. "true" and "false" are the only valid settings. The default value is false. |
| **Link-Prefix** | HTML to include before every link in an automatically generated list of tags or nodes. The default is "`<p>`". |
| **Link-Suffix** | HTML to include after every link in an automatically generated list of tags or nodes. The default is "`</p>`". |
| **Tags** | Optional comma-separated list of tags for a node. The node will be included in an auto-generated tag index for each tag it is associated with. |
| **Tag-Node** | Defines the file-based node which will serve as the root of the dynamically generated tag links.<br><br>This only has an effect when it is set on the root node. If this is not set, the tag index will not be created. |
| **Canonical-URL** | The canonical URL for the web site, without the path portion, e.g. https://www.example.com |
| **RSS-URL** | The relative URL path to use when generating the RSS feed, relative to the root of the site, e.g. /rss.xml<br><br>If this is not set, the RSS feed will not be generated.<br><br>This must be set on the root node. |
| **RSS-Title** | Title to use in the RSS feed. If not set, the "Title" header from the root node will be used instead. |
| **RSS-Add-Node-Title-Header** | If set, the node title will be included as an HTML `<h1>` header before the node body in the RSS description. "true" and "false" are the only valid settings. The default value is true. |
| **RSS-Description** | Description text to include in the RSS feed. |
| **RSS-Image-URL** | The relative or absolute URL to use for the RSS image to present as the icon for this site.<br><br>Optional. |
| **RSS-Image-Width** | The width of the RSS image. |
| **RSS-Image-Height** | The height of the RSS image. |
| **RSS-Include** | If set, this header controls whether a node is eligible for inclusion in the RSS feed. "true" and "false" are the only valid settings. The default value is false. |
| **Sitemap-URL** | The relative URL path to use when generating the sitemap XML file, relative to the root of the site, e.g. /sitemap.xml<br><br>A sitemap can only list URL paths that are at or below its level, so it is recommended to put it in the root directory. |
| **Sitemap-Include** | If set, this header controls whether a node is eligible for inclusion in the sitemap. "true" and "false" are the only valid settings. The default value is true. |

### Header Inheritance and Modification

If you want to remove a header that was inherited from a parent node, simply
include the header on the current node, prefixed with a "-", with a value of
"*". For example, if the parent node had a header of the form:

```
Foo: bar
```

you could remove this header in the child node by setting it as follows:

```
-Foo: *
```

You can also set a header so that it doesn't take effect in the current node,
but will take effect in child nodes. For example, imagine you had a node
called `articles/index`, and then a bunch of nodes under `articles/` that had
content (e.g. `articles/some-article`, `articles/some-other-thing`). You might
want to have the `articles/index` page use one template, but have all of the
individual articles use a different template, without having to set it on
every single article.

To set a header not in the current node, but only in its child nodes, prepend
a "+" sign to the name of the template. For example:

```
+Template: template-for-child-nodes.html
```

It is also possible to stack layers of + and - prefixes, where each one will
get processed in turn as the node tree is created. It is also possible to use
too much magic and create a situation that is hard to reason about. If this
sounds like you, experiment with it and see.

### URL Generation

Each node gets a unique URL path. If a unique URL path does not exist
unambiguously, one of the conflicting nodes must be renamed. See the Flat-URL
parameter to influence whether the node gets a straight mapping into a URL
path hierarchy, or is promoted up to the top level of the site.

A node named "index" takes on the URL of its containing directory. A node
named anything else has its name mapped to a URL path.

The resulting URLs are all directories, each containing an "index.html" file
that can be served up as the default document by a web server.

## Static Content

Static content to merge into the rendered web site, without modification.

When uriel runs, the public directory is initialized to only contain the
static content, completely overwriting and deleting whatever was in the public
directory before.

Next, the dynamic content is written. The rendered pages, RSS feed, sitemap,
etc.

Finally, the static content is copied over again, but this time it will only
overwrite any conflicting content in the public directory.

## Public

The public directory contains the rendered web site, ready to be hosted on a
web server. Each dynamic node is rendered into an index.html file in its own
directory. This makes the URLs a bit nicer and more abstract.

After the dynamic nodes are generated in the public website directory, the
static content is copied over, without modification.

## User-Defined Python Code

The uriel program provides a basic, stable platform for hacking. It is
entirely possible to build a complete website without any user-defined code.
However, if you want to go deeper, there are numerous opportunities for
site-specific customization.

When a project is created, the following files are created under the project
root:

- `lib/soju.py`
- `lib/handlers.py`

Soju is where you can define arbitrary Python functions that can be
interpreted in substitution parameters in nodes and templates.

The handlers allow you to tap into various points during execution of the
program, to insert your own code at several critical moments. You can add
dynamically-generated pages that will be included in the generated site,
overwrite built-in uriel functions with your own replacements, and all sorts
of things.

If you want to heavily customize your site, hacking on these files is the way
to go. You can import arbitrary Python modules, run arbitrary code, and
basically improve the system beyond recognition.

The core of uriel is not likely to change much. It does not have any external
dependencies beyond python3. Goals for the core program include minimalism,
simplicity, stability, and longevity. I want this to still work 20 years from
now.

By providing these extension mechanisms, an individual site can customize
virtually everything about the system. Think of the core program as being a
stable platform for modding, or a jazz standard that is begging to be
reinterpreted.

This is also another way of saying that the feature set for the core uriel
program is more or less set in stone, modulo any bug fixes. If you write your
own Python code that replaces the built-in method to generate the RSS feed,
for example, my fervent hope is that it will continue to work indefinitely,
without any surprises.
