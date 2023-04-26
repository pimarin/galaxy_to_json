from invoke import task


@task
def black_format(c):
    """Run black format."""
    c.run("black abromics_galaxy_json_extractor/ --exclude migrations --line-length 79")


@task
def black_check(c):
    """Run black check."""
    c.run("black abromics_galaxy_json_extractor/ --check --exclude migrations")


@task
def lint(c):
    """Run flake8."""
    c.run("flake8 abromics_galaxy_json_extractor/")


@task(lint)
def all(c):
    """Run all quality tests."""
    pass
