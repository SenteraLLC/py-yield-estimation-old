import os
from sys import argv

if __name__ == "__main__":
    repo_full_path = os.path.dirname(os.path.realpath(__file__))

    rename_files = ['environment.yml',
                    'README_template.md',
                    'pyproject.toml',
                    '.travis.yml',
                    'docs/conf.py',
                    'docs/index.rst',
                    'pkg_name/__init__.py',
                    'pkg_name/cli.py']

    REPO_NAME = os.path.split(repo_full_path)[1]
    PACKAGE_NAME = input("Enter desired name of the python package: ")
    VENV_NAME = input("Enter desired name of the conda venv: ")
    PKG_DESCRIPTION = input("Enter short description of python package: ")

    for file in [os.path.join(repo_full_path, file) for file in rename_files]:
        with open(file) as f:
            newText = f.read()
            newText = newText.replace('<repo_name>', REPO_NAME)
            newText = newText.replace('<pkg_name>', PACKAGE_NAME)
            newText = newText.replace('<venv_name>', VENV_NAME)
            newText = newText.replace('<pkg_description>', PKG_DESCRIPTION)

        with open(file, "w") as f:
            f.write(newText)

    os.rename("pkg_name", PACKAGE_NAME)
    os.remove("README.md")
    os.rename("README_template.md", "README.md")
    os.remove(argv[0])
