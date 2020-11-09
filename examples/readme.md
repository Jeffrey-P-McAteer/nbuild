
# Navy Build Examples

This directory holds files which use the `nbuild` library to describe projects
as python code. Assuming `nbuild` is installed (`python -m pip install --user nbuild`)
any of the scripts in this directory may be run like:

```bash
python review_proj01.py
```

All of the example review scripts write project completion reports
to the `reports/` directory.

To install a development copy of the library (the contents of your local `nbuild/` directory)
simply copy the `nbuild/` directory to `%LocalAppData%\programs\python\python38\lib\site-packages\nbuild` or `$HOME/.local/lib/python3.8/site-packages/nbuild` (windows or \*nix directories)

```powershell
# windows
Copy-Item -Path nbuild -Destination "%LocalAppData%\programs\python\python38\lib\site-packages\nbuild" -Recurse
```

```bash
# macos, unix, and linux
cp -r nbuild $HOME/.local/lib/python3.8/site-packages/
```

