#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Treesync 'show' subcommand
"""
from argparse import ArgumentParser, Namespace

from .base import TreesyncCommand


class Show(TreesyncCommand):
    """
    Show configured target
    """
    name = 'show'

    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Register only common base arguments
        """
        return super().register_common_arguments(parser)

    def print_target_details(self, target: ArgumentParser) -> ArgumentParser:
        """
        Print details for target
        """
        pull_command = ' '.join(target.get_pull_command_args())
        push_command = ' '.join(target.get_push_command_args())
        self.message(f'name:          {target.name}')
        self.message(f'source:        {target.source}')
        self.message(f'destitination: {target.destination}')
        self.message(f'pull command:  {pull_command}')
        self.message(f'push command:  {push_command}')

    def run(self, args: Namespace) -> None:
        """
        Show details for named targets
        """
        targets = self.filter_targets(args.targets)
        if not targets:
            self.exit(1, 'No targets to show')
        for target in targets:
            self.print_target_details(target)
