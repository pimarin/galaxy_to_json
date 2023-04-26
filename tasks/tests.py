from invoke import task


@task
def unit(c):
    """Run the unit tests."""
    c.run("pytest tests/")



@task
def cov(c):
    """Run the unit tests and the test coverage."""
    c.run("pytest --cov-report term-missing --cov=abromics_galaxy_json_extractor/ test/")

