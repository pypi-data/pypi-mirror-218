#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...domain.actions import Action
from ..command import RobotoCommand
from ..context import CLIContext
from ..help import ORG_ARG_HELP


def show(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    action = Action.from_name(
        name=args.name,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    print(json.dumps(action.to_dict(), indent=4))


def show_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=True,
        action="store",
        help="Exact name of action.",
    )
    parser.add_argument("--org", required=False, type=str, help=ORG_ARG_HELP)


show_command = RobotoCommand(
    name="show",
    logic=show,
    setup_parser=show_parser,
    command_kwargs={"help": "Get action by name."},
)
