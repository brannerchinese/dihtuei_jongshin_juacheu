## README for Ghost.py
 
Among the various possible dependencies for `ghost.py`, found only `PyQtX` available via `pip` and it is not accepted by `ghost.py`; `pyside` does not yet support Python v. 3.5 and there appear to be other unresolved issues porting the code to Python 3 (https://wiki.qt.io/PySide_Python_3_Issues).

### Pyside

Trying Python 2.7; dependencies:

```bash
brew install qt             # for qmake
pip install pyside          # long installation process — 20 min on 2.7 Ghz i7
pip install ghost.py --pre  # errors out?
```

However, running both as user and as root, pip could not install `ghost` — there were `clang` errors. It may be that `ghost` is a different library; also tried `Ghost.py`, but there are still errors. However, installation actually seems to be successful!

Also tried installing a fresh copy of Python v. 3.4. Used:

```bash
./configure --prefix=/Users/dpb/.python34
make
make install
virtualenv v_env34 --python=/Users/dpb/.python34/bin/python3.4
```

### PyQt4

A competing dependency to `pyside` is `PyQt`, but not found by `pip`.

[end]