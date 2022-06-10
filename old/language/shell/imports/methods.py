import typing

import website.console
import website.language.constants
import website.language.base.processing
import website.language.manager
import website.language.shell.lang.engine
from website.language.base.decorators import *
from website.language.shell.lang.models import *


@__method__
def get_list(self: TargetListGR, repo: str) -> list[str]:
    if isinstance(self, TargetList):
        return [item.content for item in self.items]

    elif isinstance(self, All):
        return list(website.language.manager.get_all(repo=repo))

    elif isinstance(self, Variable):
        return [self.content]

    else:
        raise NotImplementedError


@__method__
def execute(self: Command, ctx: dict) -> None:
    raise NotImplementedError


@__method__
def execute(self: Quit, ctx: dict) -> None:
    ctx['credits'] = 0


@__method__
def execute(self: Help, ctx: dict) -> None:
    ctx['credits'] += 1
    website.console.info('list of available commands :')
    website.console.info('-->', 'quit', ':', 'Quit the shell.')
    website.console.info('-->', 'help', ':', 'Display the shell commands.')
    website.console.info('-->', 'open', ':', 'Select a lang repository.')
    website.console.info('-->', 'scan', ':', website.language.manager.scan.__doc__)
    website.console.info('-->', 'create', ':', 'Create a new lang package.')
    website.console.info('-->', 'update', ':', 'Update the specified lang(s) package.')
    website.console.info('-->', 'test', ':', 'Test the specified lang(s).')
    website.console.info('-->', '&', ':', 'Use `&` between commands to chain them.')


@__method__
def execute(self: Open, ctx: dict) -> None:
    ctx['credits'] += 1
    ctx['repo'] = str(self.repo)


@__method__
def execute(self: Scan, ctx: dict) -> None:
    ctx['credits'] += 1
    website.language.manager.scan(
        repo=ctx.get('repo', 'langs'),
        debug=bool(self.debug)
    )


@__method__
def execute(self: Test, ctx: dict) -> None:
    repo = ctx.get('repo', 'langs')
    for lang in self.target.get_list(repo):
        website.console.info('testing ' + repo + '/' + lang)
        try:
            website.language.manager.test(repo, lang=lang)
            website.console.success('test success')

        except Exception as error:
            website.console.failure('test failure : ' + str(error))


@__method__
def execute(self: Create, ctx: dict) -> None:
    repo = ctx.get('repo', 'langs')
    try:
        website.language.manager.create(
            repo=repo,
            lang=str(self.target),
            create_imports=bool(self.create_imports)
        )
        website.console.success('create success : ' + repo + '/' + str(self.target))

    except Exception as error:
        website.console.failure('create failure : ' + str(error))


@__method__
def execute(self: Update, ctx: dict) -> None:
    repo = ctx.get('repo', 'langs')
    if self.repeat_:
        website.console.info("repeat mode active (type `stop` to exit.)")

    while True:
        for lang in self.target.get_list(repo):
            try:
                website.language.manager.update(repo, lang)

            except (FileNotFoundError, website.language.base.processing.ParsingError):
                continue

        if self.repeat_:
            website.console.info("press enter to update again.")
            r = input(len(repo) * ' ' + '  > ')
            if r == 'stop':
                break
        else:
            break


@__method__
def execute(self: CommandList, ctx: dict) -> None:
    for index, command in enumerate(self.commands):
        if index:
            ctx['credits'] -= 1
        command.execute(ctx)


@__class_method__
def _run(cls: Command.__class__, ctx: dict = None) -> None:
    while ctx['credits'] > 0:
        ctx['credits'] -= 1

        repo = ctx.get('repo', 'langs')
        prefix = len(repo) * ' ' + '  | '

        text = input('@' + repo + " > ")
        try:
            command = website.language.shell.engine(text)
            command.execute(ctx)

        except website.language.base.processing.ParsingError as err:
            website.console.failure('[0] invalid command (type `quit` to exit the shell). reason : ' + str(err))
            ctx['credits'] = 1
            continue

        except StopIteration:
            website.console.success('[1] exiting the shell.')
            break

        except Exception as err:
            website.console.failure('[0] ' + repr(err))
            continue


@__class_method__
def run_once(cls: Command.__class__, ctx: dict = None) -> None:
    """Ask for user command once."""
    if ctx is None:
        ctx = {}
    ctx['credits'] = 1
    return cls._run(ctx)


@__class_method__
def run_loop(cls: Command.__class__, ctx: dict = None) -> None:
    """Ask for user command until `quit`."""
    if ctx is None:
        ctx = {}
    ctx['credits'] = float('inf')
    return cls._run(ctx)
