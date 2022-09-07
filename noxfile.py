import typing

import nox


def poetry_session(
    callback: typing.Callable[[nox.Session], None]
) -> typing.Callable[[nox.Session], None]:
    @nox.session(name=callback.__name__)
    def inner(session: nox.Session) -> None:
        session.install("poetry")
        session.run("poetry", "shell")
        session.run("poetry", "install")
        callback(session)

    return inner


def pip_session(*args: str, name: str | None = None) -> typing.Callable[[nox.Session], None]:
    def inner(callback: typing.Callable[[nox.Session], None]):
        @nox.session(name=name or callback.__name__)
        def inner(session: nox.Session):
            for arg in args:
                session.install(arg)
            callback(session)

        return inner

    return inner


@pip_session("black", name="apply-lint")
def apply_lint(session: nox.Session) -> None:
    session.run("black", "sigparse")


@pip_session("flake8")
def flake8(session: nox.Session) -> None:
    session.run("flake8", "sigparse")


@poetry_session
def mypy(session: nox.Session) -> None:
    session.run("poetry", "run", "mypy", "sigparse")


@poetry_session
def pytest(session: nox.Session) -> None:
    session.run("poetry", "run", "pytest", "tests")
