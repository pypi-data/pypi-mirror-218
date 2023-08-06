"""Fastapi-mvc generators - generator generator.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.
    epilog (str): Like the help string, but it’s printed at the end of the help page
        after everything else.

"""
from typing import Dict, Any
from datetime import datetime

import click
import copier
from fastapi_mvc.cli import GeneratorCommand
from fastapi_mvc.utils import require_fastapi_mvc_project
from fastapi_mvc.constants import COPIER_GENERATOR


cmd_short_help = "Run fastapi-mvc generator generator."
cmd_help = """\
Creates a new generator at lib/generators. Pass the generator name
under_scored.

Generator template used: https://github.com/fastapi-mvc/copier-generator
"""
epilog = """\
Example:
    `fastapi-mvc generate generator awesome`

    Or using short-cut alias:
    `fm g gen awesome`

    creates a standard awesome generator:
        lib/generators/awesome/.github
        lib/generators/awesome/.github/dependabot.yml
        lib/generators/awesome/.github/workflows/update-flake.yml
        lib/generators/awesome/.envrc
        lib/generators/awesome/.gitignore
        lib/generators/awesome/CHANGELOG.md
        lib/generators/awesome/LICENSE
        lib/generators/awesome/README.md
        lib/generators/awesome/__init__.py
        lib/generators/awesome/template
        lib/generators/awesome/template/{{package_name}}
        lib/generators/awesome/template/{{package_name}}/hello_world.py
        lib/generators/awesome/update.sh
        lib/generators/awesome/flake.nix
        lib/generators/awesome/flake.lock
        lib/generators/awesome/.generator.yml
        lib/generators/awesome/awesome.py
"""


@click.command(
    cls=GeneratorCommand,
    category="Builtins",
    help=cmd_help,
    short_help=cmd_short_help,
    epilog=epilog,
    alias="gen",
)
@click.argument(
    "NAME",
    required=True,
    nargs=1,
)
@click.option(
    "-N",
    "--skip-nix",
    help="Skip nix expression files.",
    is_flag=True,
)
@click.option(
    "-G",
    "--skip-actions",
    help="Skip GitHub actions files.",
    is_flag=True,
)
@click.option(
    "--license",
    help="Choose license.",
    type=click.Choice(
        [
            "MIT",
            "BSD2",
            "BSD3",
            "ISC",
            "Apache2.0",
            "LGPLv3+",
            "LGPLv3",
            "LGPLv2+",
            "LGPLv2",
            "no",
        ]
    ),
    default="MIT",
    show_default=True,
)
@click.option(
    "--repo-url",
    help="New project repository url.",
    type=click.STRING,
    envvar="REPO_URL",
    default="https://your.repo.url.here",
)
def generator(name: str, **options: Dict[str, Any]) -> None:
    """Define generator generator command-line interface.

    Args:
        name (str): Given generator name.
        options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

    """
    require_fastapi_mvc_project()
    name = name.lower().replace("-", "_").replace(" ", "_")
    data = {
        "generator": name,
        "nix": not options["skip_nix"],
        "repo_url": options["repo_url"],
        "github_actions": not options["skip_actions"],
        "license": options["license"],
        "copyright_date": datetime.today().year,
    }

    copier.run_copy(
        src_path=COPIER_GENERATOR.template,
        vcs_ref=COPIER_GENERATOR.vcs_ref,
        dst_path=f"./lib/generators/{name}",
        data=data,
        answers_file=".generator.yml",
    )
