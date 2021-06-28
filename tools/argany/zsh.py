#!/usr/bin/python3

import argparse, shell, utils, sys

class ZshCompleter(shell.ShellCompleter):
    def none(self):
        return "'()'"

    def file(self, glob_pattern=None):
        if not glob_pattern:
            return '_files'
        else:
            return shell.escape('_files -G '+glob_pattern)

    def directory(self, glob_pattern=None):
        if not glob_pattern:
            return '_directories'
        else:
            return shell.escape('_directories -G '+glob_pattern)

    def variable(self):
        return '_vars'

    def command(self):
        return '_command_names'

    def user(self):
        return '_users'

    def group(self):
        return '_groups'

    def hostname(self):
        return '_hosts'

    def process(self):
        return '_process_names'

    def pid(self):
        return '_pids'

    def choices(self, choices):
        if hasattr(choices, 'items'):
            return shell.escape('((%s))' % ' '.join(
                shell.escape('%s\\:%s' % (str(val), desc)) for val, desc in choices.items()
            ))
        else:
            return shell.escape("(%s)" % (' '.join(shell.escape(str(c)) for c in choices)))

    def range(self, range):
        if range.step == 1:
            return f"'({{{range.start}..{range.stop}}})'"
        else:
            return f"'({{{range.start}..{range.stop}..{range.step}}})'"


_zsh_complete = ZshCompleter().complete

escape_colon = lambda s: s.replace(':', '\\:')

def _zsh_make_argument_option_spec(
        option_strings,
        conflicting_arguments=[],
        description = '',
        takes_args=False,
        metavar = '',
        action = ''
    ):
    # '(--option -o)'{--option=,-o+}'[Option description]':Metavar:'action'

    # Any literal colon in an optname, message, or action must be preceded by a backslash, `\:'.
    conflicting_arguments = [escape_colon(s) for s in sorted(conflicting_arguments)]
    option_strings        = [escape_colon(s) for s in sorted(option_strings)]
    description           = escape_colon('['+description+']') if description else ''
    metavar               = escape_colon(metavar)

    if conflicting_arguments:
        conflicting_arguments = shell.escape("(%s)" % ' '.join(escape_colon(s) for s in conflicting_arguments))

    if takes_args:
        option_strings = [o+'+' if len(o) == 2 else o+'=' for o in option_strings]

    if len(option_strings) == 1:
        option_strings = option_strings[0]
    else:
        option_strings = '{%s}' % ','.join(option_strings)

    #conflicting_arguments = shell.escape(conflicting_arguments)
    description = shell.escape(description, escape_empty_string=False)
    metavar = shell.escape(metavar, escape_empty_string=False)

    return f'{conflicting_arguments}{option_strings}{description}:{metavar}:{action}'

def _zsh_complete_action(info, parser, action):
    if action.option_strings:
        metavar = ''
        if action.takes_args():
            if action.metavar:
                metavar = action.metavar
            elif action.type is not None:
                metavar = utils.type2str(action.type)
            else:
                metavar = action.dest

        # Exclusive options
        exclusive_options = set(action.option_strings)
        for a in info.get_conflicting_options(action):
            exclusive_options.update(a.option_strings)

        return _zsh_make_argument_option_spec(
            action.option_strings,
            conflicting_arguments = exclusive_options,
            description = action.help,
            takes_args = action.takes_args(),
            metavar = metavar,
            action = _zsh_complete(*shell.action_get_completer(action)))

    elif isinstance(action, argparse._SubParsersAction):
        return "':command:%s'" % shell.make_subparser_identifier(parser.prog)
    else:
        return ":%s:%s" % (
            shell.escape(escape_colon(action.help)) if action.help else '',
            _zsh_complete(*shell.action_get_completer(action)))

def _zsh_generate_subcommands_complete(info, parser):
    commands = '\n    '.join(f"'{name}:{sub.get_help()}'" for name, sub in parser.get_subparsers().items())

    return f'''\
{shell.make_subparser_identifier(parser.prog)}() {{
  local commands=(
    {commands}
  )
  _describe -t commands '{parser.prog} command' commands "$@"
}}\n\n'''

def _zsh_generate_arguments(info, parser, funcname):
    args = []

    for action in parser._actions:
        args.append(_zsh_complete_action(info, parser, action))
    if len(parser.get_subparsers()):
        args.append("'*::arg:->args'")

    if len(args):
        return '  _arguments \\\n    %s\n' % '\\\n    '.join(args)

    return ''

def _zsh_generate_completion_func(info, parser, funcname):
    PS = '' # P.S. I love you

    r =  f'{funcname}() {{\n'
    r += _zsh_generate_arguments(info, parser, funcname)

    subparsers = parser.get_subparsers()
    if len(subparsers):
        PS += _zsh_generate_subcommands_complete(info, parser)

        r += '  for w in $line; do\n'
        r += '    case $w in\n'
        for name, subparser in subparsers.items():
            sub_funcname = shell.make_identifier(f'_{funcname}_{name}')
            PS += _zsh_generate_completion_func(info, subparser, sub_funcname)
            r += f'      ({name}) {sub_funcname}; break;;\n'
        r += '    esac\n'
        r += '  done\n'
    r += '}\n\n'

    return r + PS

def generate_completion(parser, prog=None):
    if prog is None:
        prog = parser.prog

    info = utils.ArgparseInfo.create(parser)
    r  = f'#compdef {prog}\n\n'
    r += _zsh_generate_completion_func(info, parser, '_'+shell.make_identifier(prog)).rstrip()
    r += f'\n\n_%s "$@"' % shell.make_identifier(prog)
    return r

