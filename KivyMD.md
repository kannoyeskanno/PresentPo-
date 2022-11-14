# KivyMD [1.1.1](https://kivymd.readthedocs.io/en/latest/changelog/index.html)

<img align="right" height="256" src="https://github.com/kivymd/internal/raw/main/logo/kivymd_logo_blue.png"/>

KivyMD is a collection of Material Design compliant widgets for use with
[Kivy](http://kivy.org), a framework for cross-platform, touch-enabled
graphical applications.

## Installation

```bash
pip install kivymd==1.1.1
```

### Dependencies:

- [Kivy](https://github.com/kivy/kivy) >= 2.0.0 ([Installation](https://kivy.org/doc/stable/gettingstarted/installation.html))
- [Python 3.7+](https://www.python.org/)
- [Pillow](https://github.com/python-pillow/Pillow/) (for [MDColorPicker](https://kivymd.readthedocs.io/en/latest/components/colorpicker/) class)

### How to install

Command [above](#installation) will install latest release version of KivyMD from 
[PyPI](https://pypi.org/project/kivymd).

If you want to install development version from 
[master](https://github.com/kivymd/KivyMD/tree/master/)
branch, you should specify link to zip archive:

```bash
pip install https://github.com/kivymd/KivyMD/archive/master.zip
```

**_Tip_**: Replace `master.zip` with `<commit hash>.zip` (eg `51b8ef0.zip`) to
download KivyMD from specific commit.

Also you can install manually from sources. Just clone the project and run pip:

```bash
git clone https://github.com/kivymd/KivyMD.git --depth 1
cd KivyMD
pip install .
```

**_Speed Tip_**: If you don't need full commit history (about 1.14 GiB), you can
use a shallow clone (`git clone https://github.com/kivymd/KivyMD.git --depth 1`)
to save time. If you need full commit history, then remove `--depth 1`.
