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
    Org.from_id(org_id=args.org, org_delegate=context.orgs).delete()
    sys.stdout.write("Successfully deleted!\n")


def delete_setup_parser(parser):
    parser.add_argument(
        "--org",
        type=str,
        required=True,
        help="The org_id for the org you're about to delete.",
    )


def get(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Org.from_id(org_id=args.org, org_delegate=context.orgs)
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def get_setup_parser(parser):
    parser.add_argument(
        "--org",
        type=str,
        required=True,
        help="The org_id for the org you want to see.",
    )


def list_orgs(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = Org.for_user(user_id=None, org_delegate=context.orgs)
    for record in records:
        sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def list_roles(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = OrgRole.for_user(user_id=None, org_delegate=context.orgs)
    for record in records:
        sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def list_org_members(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = OrgRole.for_org(org_id=args.org, org_delegate=context.orgs)
    for record in records:
        sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def list_org_members_setup_parser(parser):
    parser.add_argument(
        "--org",
        type=str,
        required=True,
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
        type=str,
        help="The org_id of the org to invite a user to. "
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


get_command = RobotoCommand(
    name="get",
    logic=get,
    setup_parser=get_setup_parser,
    command_kwargs={"help": "Gets metadata for a single organization"},
)


list_orgs_command = RobotoCommand(
    name="list-orgs",
    logic=list_orgs,
    command_kwargs={"help": "Lists the orgs that you're a member of"},
)


list_roles_command = RobotoCommand(
    name="list-roles",
    logic=list_roles,
    command_kwargs={
        "help": "Lists the roles that you have in orgs that you're a member of"
    },
)

list_org_members_command = RobotoCommand(
    name="list-org-members",
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
    get_command,
    invite_command,
    list_org_members_command,
    list_orgs_command,
    list_roles_command,
    remove_role_command,
    remove_user_command,
]

command_set = RobotoCommandSet(
    name="orgs",
    help="Commands for interacting with orgs.",
    commands=commands,
)
