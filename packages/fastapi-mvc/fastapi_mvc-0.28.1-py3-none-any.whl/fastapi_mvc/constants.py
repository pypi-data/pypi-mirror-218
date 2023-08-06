"""Fastapi-mvc constants.

Attributes:
    VERSION (str): Fastapi-mvc version.
    ANSWERS_FILE (str): Relative path to copier answers file.

"""
from collections import namedtuple


Template = namedtuple("Template", "template vcs_ref")
VERSION = "0.28.1"
ANSWERS_FILE = ".fastapi-mvc.yml"
COPIER_PROJECT = Template("https://github.com/fastapi-mvc/copier-project.git", "0.6.1")
COPIER_CONTROLLER = Template(
    "https://github.com/fastapi-mvc/copier-controller.git", "0.2.2"
)
COPIER_GENERATOR = Template(
    "https://github.com/fastapi-mvc/copier-generator.git", "0.4.1"
)
COPIER_SCRIPT = Template("https://github.com/fastapi-mvc/copier-script.git", "0.1.2")
