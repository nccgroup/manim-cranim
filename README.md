# cranim

Manim plugin focused on animating cryptographic scenes.

Currently dev install is required, since I haven't released cranim to pip yet.

Dev install: clone the repo locally and run `pip install -e .` from the repo's
root directory (or `pip install .` if you don't plan on making local changes).

In lieu of documentation (for now), please see the code samples and associated
renders in the [example gallery](examples/index.md).

Please note that Manim requires plugins to be explicitly enabled using a
command-line flag or `manim.cfg` file. See e.g. the example in
[tests/manim.cfg](tests/manim.cfg), or the official
[Manim docs](https://docs.manim.community/en/stable/plugins.html#using-plugins-in-projects)
for more info.
