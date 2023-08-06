#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse
import json
import sys

from ...domain.orgs import (
    Org,
    OrgInvite,
    OrgRole,
    OrgRoleName,
    OrgType,
)
from ..command import (
    RobotoCommand,
    RobotoCommandSet,
)
from ..context import CLIContext


def create(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Org.create(
        creator_user_id=None,
        name=args.name,
        org_type=args.type,
        org_delegate=context.orgs,
        bind_email_domain=args.bind_email_domain,
    )
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def create_setup_parser(parser):
    parser.add_argument(
        "--name", type=str, required=True, help="A human readable name for this org"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=OrgType._member_names_,
        help="The type of org you're creating",
    )

    parser.add_argument(
        "--bind-email-domain",
        action="store_true",
        help="Automatically add new users with your email domain to this org",
    )


def delete(args, context: CLIContext, parser: argparse.ArgumentParser):
    if not args.ignore_prompt:
        sys.stdout.write("Are you absolutely sure you want to delete your org? [y/n]: ")

        choice = input().lower()
        if choice not in ["y", "yes"]:
            return

    Org.from_id(org_id=args.org, org_delegate=context.orgs).delete()
    sys.stdout.write("Successfully deleted!\n")


def delete_setup_parser(parser):
    parser.add_argument(
        "--org",
        type=str,
        required=True,
        help="The org_id for the org you're about to delete.",
    )

    parser.add_argument(
        "--ignore-prompt",
        action="store_true",
        help="Ignore the prompt which asks you to confirm that you'd like to delete your org.",
    )


def show(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Org.from_id(org_id=args.org, org_delegate=context.orgs)
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def show_setup_parser(parser):
    parser.add_argument(
        "--org",
        type=str,
        help="The org_id for the org you want to see.",
    )


def list_org_members(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = OrgRole.for_org(org_id=args.org, org_delegate=context.orgs)
    for record in records:
        sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def list_org_members_setup_parser(parser):
    parser.add_argument(
        "--org",
        type=str,
        help="The org_id for the org you want to see.",
    )


def remove_user(args, context: CLIContext, parser: argparse.ArgumentParser):
    org = Org.from_id(org_id=args.org, org_delegate=context.orgs)
    org.remove_user(user_id=args.user)
    sys.stdout.write("Successfully removed!\n")


def remove_user_setup_parser(parser):
    parser.add_argument(
        "--user",
        type=str,
        required=True,
        help="The user_id of the user to remove.",
    )
    parser.add_argument(
        "--org",
        type=str,
        help="The org_id of the org to remove a user from. "
        + "Required only if the caller is a member of more than one org.",
    )


def invite_user(args, context: CLIContext, parser: argparse.ArgumentParser):
    OrgInvite.create(
        invited_user_id=args.user,
        org_id=args.org,
        inviting_user_id=None,
        org_delegate=context.orgs,
    )
    sys.stdout.write("Invite sent!\n")


def invite_user_setup_parser(parser):
    parser.add_argument(
        "--user",
        type=str,
        required=True,
        help="The user_id of the user to invite.",
    )
    parser.add_argument(
        "--org",
        help="The org_id of the org to invite a user to. "
        + "Required only if the caller is a member of more than one org.",
    )


def list_invites(args, context: CLIContext, parser: argparse.ArgumentParser):
    invites = OrgInvite.for_org(org_id=args.org, org_delegate=context.orgs)
    for invite in invites:
        sys.stdout.write(json.dumps(invite.to_dict()) + "\n")


def list_invites_setup_parser(parser):
    parser.add_argument(
        "--org",
        help="The org_id of the org to view invites for. "
        + "Required only if the caller is a member of more than one org.",
    )


def add_role(args, context: CLIContext, parser: argparse.ArgumentParser):
    Org.from_id(org_id=args.org, org_delegate=context.orgs).add_role_for_user(
        user_id=args.user, role_name=args.role
    )
    sys.stdout.write("Added!\n")


def add_role_setup_parser(parser):
    parser.add_argument(
        "--user",
        type=str,
        required=True,
        help="The user_id of the user to add a role for.",
    )
    parser.add_argument(
        "--role",
        type=OrgRoleName,
        choices=[OrgRoleName.admin, OrgRoleName.owner],
        help="The role to grant to the specified user",
    )
    parser.add_argument(
        "--org",
        type=str,
        help="The org_id of the org for which to add permissions for the specified user. "
        + "Required only if the caller is a member of more than one org.",
    )


def remove_role(args, context: CLIContext, parser: argparse.ArgumentParser):
    Org.from_id(org_id=args.org, org_delegate=context.orgs).remove_role_from_user(
        user_id=args.user, role_name=args.role
    )
    sys.stdout.write("Removed!\n")


def remove_role_setup_parser(parser):
    parser.add_argument(
        "--user",
        type=str,
        required=True,
        help="The user_id of the user to add a role for. "
        + "This can be your own user_id if you would like to step down as an admin or owner.",
    )
    parser.add_argument(
        "--role",
        type=OrgRoleName,
        choices=[OrgRoleName.admin, OrgRoleName.owner],
        help="The role to remove for the specified user",
    )
    parser.add_argument(
        "--org",
        type=str,
        help="The org_id of the org for which to remove permissions for the specified user. "
        + "Required only if the caller is a member of more than one org.",
    )


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_setup_parser,
    command_kwargs={"help": "Creates a new organization"},
)


delete_command = RobotoCommand(
    name="delete",
    logic=delete,
    setup_parser=delete_setup_parser,
    command_kwargs={"help": "Deletes an existing organization"},
)


show_command = RobotoCommand(
    name="show",
    logic=show,
    setup_parser=show_setup_parser,
    command_kwargs={"help": "Gets metadata for a single organization"},
)


list_org_members_command = RobotoCommand(
    name="members",
    logic=list_org_members,
    setup_parser=list_org_members_setup_parser,
    command_kwargs={"help": "Lists the members of an organization"},
)

remove_user_command = RobotoCommand(
    name="remove-user",
    logic=remove_user,
    setup_parser=remove_user_setup_parser,
    command_kwargs={"help": "Removes a user from an organization"},
)

invite_command = RobotoCommand(
    name="invite-user",
    logic=invite_user,
    setup_parser=invite_user_setup_parser,
    command_kwargs={"help": "Invites a user to join an org."},
)

list_invites_command = RobotoCommand(
    name="list-invites",
    logic=list_invites,
    setup_parser=list_invites_setup_parser,
    command_kwargs={"help": "Lists the current pending invites for a specified org"},
)

add_role_command = RobotoCommand(
    name="add-role",
    logic=add_role,
    setup_parser=add_role_setup_parser,
    command_kwargs={"help": "Promotes a user to a more permissive org access level."},
)

remove_role_command = RobotoCommand(
    name="remove-role",
    logic=remove_role,
    setup_parser=remove_role_setup_parser,
    command_kwargs={"help": "Demotes a user to a less permissive org access level."},
)

commands = [
    add_role_command,
    create_command,
    delete_command,
    invite_command,
    list_invites_command,
    list_org_members_command,
    remove_role_command,
    remove_user_command,
    show_command,
]

command_set = RobotoCommandSet(
    name="orgs",
    help="Commands for interacting with orgs.",
    commands=commands,
)
