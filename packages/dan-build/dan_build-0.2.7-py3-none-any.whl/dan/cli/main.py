import os
import sys
from dan import logging
import asyncio

from dan.core.find import find_file
from dan.core.pathlib import Path
from dan.cli import click

from dan.core import diagnostics
from dan.core.cache import Cache
from dan.core.settings import Settings
from dan.cxx.targets import Executable


from dan.make import InstallMode, Make
from dan.cli.vscode import Code


_minimal_options = [
    click.option('--build-path', '-B', help='Path where dan has been initialized.',
                 type=click.Path(resolve_path=True, path_type=Path), required=True, default='build', envvar='DAN_BUILD_PATH'),
]

_common_opts = [
    *_minimal_options,
    click.option('--quiet', '-q', is_flag=True,
                 help='Dont print informations (errors only).', envvar='DAN_QUIET'),
    click.option('--verbose', '-v', is_flag=True,
                 help='Pring debug informations.', envvar='DAN_VERBOSE'),
    click.option('--jobs', '-j',
                 help='Maximum jobs.', default=None, type=int, envvar='DAN_JOBS'),
    click.option('--no-progress', is_flag=True,
                 help='Disable progress bars', envvar='DAN_NOPROGRESS'),
]
_base_help_ = '''
  PATH          Either build or source directory.
  [TARGETS...]  Targets to process.
'''


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


common_opts = add_options(_common_opts)
minimal_options = add_options(_minimal_options)


class CommandsContext:
    def __init__(self, *args, **kwds) -> None:
        self._make_args = [*args]
        self._make_kwds = {**kwds}
        self._make = None

    def __call__(self, *args, **kwds):
        if len(args):
            self._make_args.extend(*args)
        self._make_kwds.update(**kwds)

    @property
    def make(self):
        if self._make is None:
            self._make = Make(*self._make_args, **self._make_kwds)
        return self._make


pass_context = click.make_pass_decorator(CommandsContext)

@pass_context
def show_diags(ctx: CommandsContext):
    if diagnostics.enabled:
        diags = ctx.make.diagnostics
        if diags:
            click.echo(f'DIAGNOSTICS: {diags.to_json()}')

@click.group()
@click.version_option(package_name='dan-build')
@click.option('--quiet', '-q', is_flag=True,
              help='Dont print informations (errors only)')
@click.option('--verbose', '-v', is_flag=True,
              help='Pring debug informations')
@click.option('--jobs', '-j',
              help='Maximum jobs', default=None, type=int)
@click.pass_context
def cli(ctx: click.AsyncContext, **kwds):
    ctx.obj = CommandsContext(**kwds)
    ctx.call_on_close(show_diags)


@cli.command()
@click.option('--verbose', '-v', is_flag=True,
              help='Pring debug informations')
@click.option('--toolchain', '-t', help='The toolchain to use',
              type=click.ToolchainParamType(), envvar='DAN_TOOLCHAIN')
@click.option('--setting', '-s', 'settings', help='Set or change a setting', multiple=True, type=click.SettingsParamType(Settings))
@click.option('--option', '-o', 'options', help='Set or change an option', multiple=True, type=click.OptionsParamType())
@click.option('--build-path', '-B', help='Path where dan has been initialized.',
              type=click.Path(resolve_path=True, path_type=Path), required=True, default='build', envvar='DAN_BUILD_PATH')
@click.option('--source-path', '-S', help='Path where source is located.',
              type=click.Path(resolve_path=True, path_type=Path), required=True, default='.')
@pass_context
async def configure(ctx: CommandsContext, toolchain: str, settings: tuple[str], options: tuple[str], source_path: Path, **kwds):
    """Configure dan project"""
    ctx(**kwds)  # update kwds
    if toolchain is None and ctx.make.config.toolchain is None:
        from dan.cxx.detect import get_toolchains
        tp = click.Choice(get_toolchains(create=False)["toolchains"].keys())
        toolchain = click.prompt('Toolchain', type=tp, default='default')

    await ctx.make.configure(source_path, toolchain)

    if len(settings):
        await ctx.make.apply_settings(*settings)

    # NOTE: intializing make after applying setting
    #       to check settings are valid implicitly (cache save skipped)
    await ctx.make.initialize()

    if len(options):
        await ctx.make.apply_options(*options)


@cli.command()
@click.option('--for-install', is_flag=True, help='Build for install purpose (will update rpaths [posix only])')
@common_opts
@click.option('--force', '-f', is_flag=True,
              help='Clean before building')
@click.argument('TARGETS', nargs=-1, type=click.TargetParamType())
@pass_context
async def build(ctx: CommandsContext, force=False, **kwds):
    """Build targets"""
    ctx(**kwds)  # update kwds
    if force:
        await ctx.make.clean()
    await ctx.make.build()

@cli.command()
@common_opts
@click.argument('TARGETS', nargs=-1, type=click.TargetParamType())
@pass_context
async def install_dependencies(ctx: CommandsContext, **kwds):
    """Build targets"""
    ctx(**kwds)  # update kwds
    await ctx.make.install_dependencies()

@cli.command()
@common_opts
@click.argument('MODE', type=click.Choice([v.name for v in InstallMode]), default=InstallMode.user.name)
@click.argument('TARGETS', nargs=-1, type=click.TargetParamType())
@pass_context
async def install(ctx: CommandsContext, mode: str, **kwargs):
    """Install targets"""
    ctx(**kwargs)
    mode = InstallMode[mode]
    await ctx.make.install(mode)


@cli.command()
@click.option('--verbose', '-v', is_flag=True,
              help='Pring debug informations')
@click.option('--yes', '-y', is_flag=True, help='Proceed without asking')
@click.option('--root', '-r', help='Root path to search for installation manifest', type=click.Path(exists=True, file_okay=False))
@click.argument('NAME')
def uninstall(verbose: bool, yes: bool, root: str, name: str):
    """Uninstall previous installation"""
    logging.getLogger().setLevel(logging.DEBUG if verbose else logging.INFO)
    if root:
        paths = [root]
    else:
        paths = [
            '~/.local/share/dan',
            '/usr/local/share/dan',
            '/usr/share/dan',
        ]
    manifest = find_file(f'{name}-manifest.txt$', paths=paths)
    with open(manifest, 'r') as f:
        files = [(manifest.parent / mf.strip()).resolve()
                 for mf in f.readlines()]
    to_be_removed = '\n'.join([f" - {f}" for f in files])
    yes = yes or click.confirm(
        f'Following files will be removed:\n {to_be_removed}\nProceed ?')
    if yes:
        def rm_empty(dir: Path):
            if dir.is_empty:
                click.logger.debug(f'removing empty directory: {dir}')
                os.rmdir(dir)
                rm_empty(dir.parent)

        for f in files:
            click.logger.debug(f'removing: {f}')
            os.remove(f)
            rm_empty(f.parent)

        os.remove(manifest)
        rm_empty(manifest.parent)

@cli.group()
@pass_context
def ls(ctx: CommandsContext):
    """Inspect stuff"""
    pass

@ls.command()
@click.option('-a', '--all', 'all', is_flag=True, help='Show all targets (not only defaulted ones)')
@click.option('-t', '--type', 'show_type', is_flag=True, help='Show target\'s type')
@common_opts
@click.argument('TARGETS', nargs=-1)
@pass_context
async def targets(ctx: CommandsContext, all: bool, show_type: bool, **kwargs):
    """List targets"""
    kwargs['quiet'] = True
    ctx(**kwargs)
    await ctx.make.initialize()
    out = []
    for target in ctx.make.targets:
        if show_type:
            out.append(target.fullname + ' - ' + type(target).__name__)
        else:
            out.append(target.fullname)
    click.echo('\n'.join(out))


@ls.command()
@common_opts
@click.argument('TARGETS', nargs=-1)
@pass_context
async def tests(ctx: CommandsContext, **kwargs):
    """List tests"""
    kwargs['quiet'] = True
    ctx(**kwargs)
    await ctx.make.initialize()
    for t in ctx.make.tests:
        if len(t) > 1:
            for c in t.cases:
                click.echo(f'{t.fullname}:{c.name}')
        else:
            click.echo(t.fullname)

@ls.command()
@common_opts
@click.argument('TARGETS', nargs=-1)
@pass_context
async def options(ctx: CommandsContext, **kwargs):
    """List tests"""
    kwargs['quiet'] = True
    ctx(**kwargs)
    await ctx.make.initialize()
    for o in ctx.make.all_options:
        current = ''
        if o.value != o.default:
            current = f', current: {o.value}'
        click.echo(f'{o.fullname}: {o.help} (type: {o.type.__name__}, default: {o.default}{current})')

@ls.command()
def toolchains(**kwargs):
    """List toolchains"""
    kwargs['quiet'] = True
    for name, _ in Make.toolchains()['toolchains'].items():
        click.echo(name)


@cli.command()
@common_opts
@click.argument('TARGETS', nargs=-1, type=click.TargetParamType())
@pass_context
async def clean(ctx, **kwargs):
    """Clean generated stuff"""
    ctx(**kwargs)
    await ctx.make.clean()


@cli.command()
@common_opts
@click.argument('TARGETS', nargs=-1, type=click.TargetParamType())
@pass_context
async def run(ctx, **kwargs):
    """Run executable(s)"""
    ctx(**kwargs)
    rc = await ctx.make.run()
    sys.exit(rc)


@cli.command()
@common_opts
@click.argument('TARGETS', nargs=-1, type=click.TargetParamType())
@pass_context
async def test(ctx, **kwargs):
    """Run tests"""
    ctx(**kwargs)
    rc = await ctx.make.test()
    sys.exit(rc)


@cli.command()
@click.option('-s', '--script',
              help='Use a source script to resolve compilation environment')
@click.option('-p', '--path', 'paths',
              help='Use given path for compilers lookup', multiple=True, type=click.Path(exists=True, file_okay=False))
@click.option('--verbose', '-v', is_flag=True,
              help='Pring debug informations.', envvar='DAN_VERBOSE')
def scan_toolchains(script: str, paths: list[str], verbose, **kwargs):
    """Scan system toolchains"""
    logging.getLogger().setLevel(logging.DEBUG if verbose else logging.INFO)
    from dan.cxx.detect import create_toolchains, load_env_toolchain
    if script:
        load_env_toolchain(script)
    else:
        create_toolchains(paths if len(paths) else None)


@cli.group()
def code():
    """VS-Code specific commands"""
    pass


@code.command()
@common_opts
@click.argument('TARGETS', nargs=-1)
@pass_context
async def get_targets(ctx: CommandsContext, **kwargs):
    kwargs.update({'quiet': True, 'diags': True})
    ctx(**kwargs)
    await ctx.make.initialize()
    out = []
    targets = ctx.make.context.root.all_targets
    for target in targets:
        out.append({
            'name': target.name,
            'fullname': target.fullname,
            'buildPath': str(target.build_path),
            'output': str(target.output),
            'executable': isinstance(target, Executable),
            'type': type(target).__name__
        })
    import json
    click.echo(json.dumps(out))

@code.command()
@common_opts
@click.argument('TARGETS', nargs=-1)
@pass_context
async def get_tests(ctx: CommandsContext, **kwargs):
    kwargs.update({'quiet': True, 'diags': True})
    ctx(**kwargs)
    await ctx.make.initialize()
    import json
    out = list()
    for t in ctx.make.context.root.all_tests:
        out.append(t.fullname)
        if len(t) > 1:
            for c in t.cases:
                out.append(f'{t.fullname}:{c.name}')
    click.echo(json.dumps(out))


@code.command()
@common_opts
@click.option('--pretty', is_flag=True)
@click.argument('TARGETS', nargs=-1)
@pass_context
async def get_test_suites(ctx: CommandsContext, pretty, **kwargs):
    kwargs.update({'quiet': True, 'diags': True})
    ctx(**kwargs)
    await ctx.make.initialize()
    code = Code(ctx.make)
    click.echo(code.get_test_suites(pretty))


@code.command()
def get_toolchains(**kwargs):
    import json
    click.echo(json.dumps(list(Make.toolchains()['toolchains'].keys())))


@code.command()
@click.option('--for-install', is_flag=True, help='Build for install purpose (will update rpaths [posix only])')
@common_opts
@click.option('--force', '-f', is_flag=True,
              help='Clean before building')
@click.argument('TARGETS', nargs=-1)
@pass_context
async def build(ctx: CommandsContext, force=False, **kwds):
    """Build targets (vscode version)"""
    ctx(**kwds, diags=True)  # update kwds
    if force:
        await ctx.make.clean()
    await ctx.make.build()


@code.command()
@minimal_options
@click.argument('SOURCES', nargs=-1)
@pass_context
async def get_source_configuration(ctx: CommandsContext, sources, **kwargs):
    kwargs.update({'quiet': True, 'diags': True})
    ctx(**kwargs)
    await ctx.make.initialize()
    code = Code(ctx.make)
    click.echo(await code.get_sources_configuration(sources))


@code.command()
@minimal_options
@pass_context
async def get_workspace_browse_configuration(ctx: CommandsContext, **kwargs):
    kwargs.update({'quiet': True, 'diags': True})
    ctx(**kwargs)
    await ctx.make.initialize()
    code = Code(ctx.make)
    click.echo(await code.get_workspace_browse_configuration())

@cli.result_callback()
@pass_context
async def process_result(ctx, result, **kwargs):
    await Cache.save_all()


def main():
    import sys
    try:
        cli(auto_envvar_prefix='DAN')
    except Exception as err:
        click.logger.error(str(err))
        _ex_type, _ex, tb = sys.exc_info()
        import traceback
        click.logger.debug(' '.join(traceback.format_tb(tb)))
        try:
            # wait asyncio loop to terminate
            asyncio.get_running_loop().run_until_complete()
        except Exception:
            pass
        asyncio.run(Cache.save_all())
        return -1
