from invoke import task


@task
def black_format(c):
    """Run black format."""
    c.run("black ABRomicsonization/ --exclude migrations --line-length 80")


@task
def black_check(c):
    """Run black check."""
    c.run("black ABRomicsonization/ --check --exclude migrations")


@task
def lint(c):
    """Run flake8."""
    c.run("flake8 ABRomicsonization/")


@task(black_format, lint)
def all(c):
    """Run all quality tests."""
    pass
