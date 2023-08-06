"""Generate a tex file from a CSV file using a Jinja template."""

import re
from pathlib import Path
from typing import Optional, Any

import click
import jinja2
import pandas as pd

ExistingFile = click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path)
File = click.Path(exists=False, file_okay=True, dir_okay=False, path_type=Path)


def get_default_ifname(tfname: Path) -> Path:
    """Get input filename from template filename."""
    name = tfname.name
    name = name.rsplit(".", maxsplit=3)
    match name:
        case [p1, _, _] | [p1, _] | [p1]:
            return tfname.parent / f"{p1}.csv"
        case _:
            raise ValueError("Unexpected filename")


def get_default_ofname(tfname: Path) -> Path:
    """Get output filename from template filename."""
    name = tfname.name
    name = name.rsplit(".", maxsplit=3)
    match name:
        case [p1, _, _] | [p1, _] | [p1]:
            return tfname.parent / f"{p1}.tex"
        case _:
            raise ValueError("Unexpected filename")


# https://stackoverflow.com/questions/16259923/how-can-i-escape-latex-special-characters-inside-django-templates
def escape_tex(text: Any) -> str:
    text = str(text)
    conv = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }
    regex = re.compile(
        "|".join(
            re.escape(str(key))
            for key in sorted(conv.keys(), key=lambda item: -len(item))
        )
    )
    return regex.sub(lambda match: conv[match.group()], text)


@click.command()
@click.option("-i", "--input", "ifname", type=File, help="Input csv file")
@click.option("-o", "--output", "ofname", type=File, help="Output file")
@click.argument("tfname", metavar="FILE", type=ExistingFile)
def csv2tex(ifname: Optional[Path], ofname: Optional[Path], tfname: Path):
    if ifname is None:
        ifname = get_default_ifname(tfname)
    if ofname is None:
        ofname = get_default_ofname(tfname)

    df = pd.read_csv(ifname)

    env = jinja2.Environment(
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
        trim_blocks=True,
        undefined=jinja2.StrictUndefined,
    )
    env.filters["escape"] = escape_tex

    template = tfname.read_text()
    template = env.from_string(template)

    output = template.render(data=df)
    ofname.write_text(output)


if __name__ == "__main__":
    csv2tex()
