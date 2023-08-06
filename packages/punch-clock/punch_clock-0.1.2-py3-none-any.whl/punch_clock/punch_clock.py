import git
import os
from . import utils
import click


def get_repo() -> git.Repo:
    return git.Repo(".")


def get_name(git_config: git.GitConfigParser) -> str:
    name = git_config.get_value("user", "name")
    name = name.replace(" ", "-")
    name = "".join([c if c.isalnum() else "-" for c in name])
    name = "_".join(name.split("-"))
    name = name.lower()
    return name


def get_email(git_config: git.GitConfigParser) -> str:
    return git_config.get_value("user", "email")


def push_repo(repo: git.Repo, m: str, dir: str, name: str) -> None:
    filename = f"{dir}/{name}.md"
    repo.index.add(filename)
    repo.index.commit(m)
    repo.remotes.origin.push()
    pass


def entry_in(name: str, dir: str) -> None:
    try:
        with open(f"{dir}/{name}.md", "r+") as f:
            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - 1, os.SEEK_SET)
            if f.read(1) == "\n":
                f.write(f"| {utils.get_time()} |")
            else:
                raise Exception("!!! already punched in !!!")
    except Exception as e:
        raise e


def entry_out(name: str, dir: str) -> None:
    try:
        with open(f"{dir}/{name}.md", "r+") as f:
            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - 1, os.SEEK_SET)
            if f.read(1) != "\n":
                content = click.prompt(">> what did you do?", type=str)
                f.write(f" {utils.get_time()} | {content} |\n")
            else:
                raise Exception("!!! already punched out !!!")
    except Exception as e:
        raise e
