#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...domain.actions import Invocation
from ..command import RobotoCommand
from ..context import CLIContext
from ..help import ORG_ARG_HELP


def list_invocations(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    matching_invocations = Invocation.query(
        {"action_name": args.name},
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    print(
        json.dumps(
            [invocation.to_dict() for invocation in matching_invocations], indent=4
        )
    )


def list_invocations_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=False,
        action="store",
        help="If querying by action name, must provide an exact match; patterns are not accepted.",
    )
    parser.add_argument("--org", required=False, type=str, help=ORG_ARG_HELP)


list_invocations_command = RobotoCommand(
    name="list-invocations",
    logic=list_invocations,
    setup_parser=list_invocations_parser,
    command_kwargs={"help": "List invocations for action."},
)
