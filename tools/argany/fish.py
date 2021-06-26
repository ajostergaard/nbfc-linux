#!/usr/bin/python3

import sys, shell, utils

class FishCompleter(shell.ShellCompleter):
    def none(self):
        return ''

    def choices(self, choices):
        return '-f -a ' + shell.escape(' '.join(shell.escape(str(c)) for c in choices))

    def file(self, glob_pattern=None):
        if glob_pattern:
            print("Warning, glob_pattern `%s' ignored\n" % glob_pattern, file=sys.stderr)
        return '-F'

    def directory(self, glob_pattern=None):
        if glob_pattern:
            return "-f -a '(__fish_complete_directories %s)'" % shell.escape(glob_pattern)
        return "-f -a '(__fish_complete_directories)'"

    def hostname(self):
        return "-f -a '(__fish_print_hostnames)'"

    def process(self):
        return "-f -a '(__fish_complete_proc)'"

    def command(self):
        return "-f -a '(__fish_complete_command)'"

    def service(self):
        return "-f -a '(__fish_systemctl_services)'"

    def variable(self):
        return "-f -a '(set -n)'"

    def user(self):
        return "-f -a '(__fish_complete_users)'"

    def pid(self):
        return "-f -a '(__fish_complete_pids)'"

    def group(self):
        return "-f -a '(__fish_complete_groups)'"

    def range(self, range):
        if range.step == 1:
            return f"-f -a '(seq {range.start} {range.stop})'"
        else:
            return f"-f -a '(seq {range.start} {range.step} {range.stop})'"


_fish_complete = FishCompleter().complete

def _fish_join(l):
    return ' '.join(shell.escape(word) for word in l)

def _fish_make_complete(
        program_name,            # Name of program beeing completed
        short_options=[],        # List of short options
        long_options=[],         # List of long options
        seen_words=[],           # Only show if these words are given on commandline
        not_seen_words=[],       # Only show if these words are not given on commandline
        conflicting_options=[],  # Only show if these options are not given on commandline
        description=None,        # Description
        positional=None,         # Only show if current word number is `positional`
        requires_argument=False, # Option requires an argument
        no_files=False,          # Don't use file completion
        choices=[]               # Add those words for completion
    ):
    # =========================================================================
    # Helper function for creating a `complete` command in fish
    # =========================================================================

    r = ''
    flags = set()

    if no_files:           flags.add('f')
    if requires_argument:  flags.add('r')

    if len(seen_words):
        r += " -n '__fish_seen_subcommand_from %s'" % _fish_join(sorted(seen_words))

    if len(not_seen_words):
        r += " -n 'not __fish_seen_subcommand_from %s'" % _fish_join(sorted(not_seen_words))

    if conflicting_options:
        r += " -n 'not __fish_contains_opt %s'" % ' '.join(o.lstrip('-') for o in sorted(conflicting_options))

    if positional is not None:
        r += " -n 'test (__fish_number_of_cmd_args_wo_opts) = %d'" % positional

    for o in sorted(short_options): r += ' -s ' + shell.escape(o.lstrip('-'))
    for o in sorted(long_options):  r += ' -l ' + shell.escape(o.lstrip('-'))
    if description:                 r += ' -d ' + shell.escape(description)

    for s in choices:
        r += ' -a ' + shell.escape(s)

    if 'r' in flags and 'f' in flags:
        flags.remove('r')
        flags.remove('f')
        flags.add('x')

    if len(flags):
        flags = ' -' + ''.join(flags)
    else:
        flags = ''

    return 'complete -c ' + shell.escape(program_name) + flags + r

def _fish_complete_action(info, parser, action, program_name, subcommands=[]):
    short_options       = []
    long_options        = []
    positional          = None
    conflicting_options = set()

    if not action.option_strings:
        positional = 1 + info.get_positional_index(action)
    else:
        for opt in sorted(action.option_strings):
            if opt.startswith('--'): long_options.append(opt)
            else:                    short_options.append(opt)

    for option in info.get_conflicting_options(action):
        conflicting_options.update(option.option_strings)

    r = _fish_make_complete(
        program_name,
        requires_argument   = action.requires_args(),
        description         = action.help,
        seen_words          = subcommands,
        short_options       = short_options,
        positional          = positional,
        long_options        = long_options,
        conflicting_options = conflicting_options
    )

    r += ' ' + _fish_complete(*shell.action_get_completer(action))
    return r.rstrip()

def _fish_complete_subcommands(info, parser, program_name, current_subcommands):
    r = ''

    for name, sub in parser.get_subparsers().items():
        r += _fish_make_complete(
            program_name,
            no_files       = True,
            description    = sub.get_help(),
            choices        = [name],
            seen_words     = current_subcommands,
            not_seen_words = sorted(parser.get_subparsers().keys())
            # we only want to complete a subparsers `name` if it is not yet given on commandline
        ) + '\n'

    return r

def _fish_complete_parser(info, parser, program_name, current_subcommands=[]):
    # `current_subcommands` is used to ensure that a commands option is only
    #  shown if it is present on the commmandline. we use a list to support multiple subcommands.

    r = ''

    for action in parser._actions:
        r += '%s\n' % _fish_complete_action(info, parser, action, program_name, current_subcommands)

    subparsers = parser.get_subparsers()
    if len(subparsers):
        r += _fish_complete_subcommands(info, parser, program_name, current_subcommands)

        for name, subparser in subparsers.items():
            r += _fish_complete_parser(info, subparser, program_name, current_subcommands + [name])

    return r

def generate_completion(p, prog=None):
    if prog is None:
        prog = p.prog

    info = utils.ArgparseInfo.create(p)
    return _fish_complete_parser(info, p, prog)
