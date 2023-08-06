import os # --STRIP DURING BUILD
import sys # --STRIP DURING BUILD
from typing import Optional # --STRIP DURING BUILD
from subprocess_helper import run_command # --STRIP DURING BUILD

def do_vcs_install(versionfile_source: str, ipy: Optional[str]) -> None:
    """Git-specific installation logic for Versioneer.

    For Git, this means creating/changing .gitattributes to mark _version.py
    for export-subst keyword substitution.
    """
    GITS = ["git"]
    if sys.platform == "win32":
        GITS = ["git.cmd", "git.exe"]
    files = [versionfile_source]
    if ipy:
        files.append(ipy)
    if "VERSIONEER_PEP518" not in globals():
        try:
            my_path = __file__
            if my_path.endswith((".pyc", ".pyo")):
                my_path = os.path.splitext(my_path)[0] + ".py"
            versioneer_file = os.path.relpath(my_path)
        except NameError:
            versioneer_file = "versioneer.py"
        files.append(versioneer_file)
    present = False
    try:
        with open(".gitattributes", "r") as fobj:
            for line in fobj:
                if line.strip().startswith(versionfile_source):
                    if "export-subst" in line.strip().split()[1:]:
                        present = True
                        break
    except OSError:
        pass
    if not present:
        with open(".gitattributes", "a+") as fobj:
            fobj.write(f"{versionfile_source} export-subst\n")
        files.append(".gitattributes")
    run_command(GITS, ["add", "--"] + files)


