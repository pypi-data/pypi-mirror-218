#  Copyright (c) 2023 Roboto Technologies, Inc.
from ..command import RobotoCommandSet
from .status import status_command

commands = [
    status_command,
]

command_set = RobotoCommandSet(
    name="invocations",
    help=("Show details of action invocations, their status history, and logs."),
    commands=commands,
)
