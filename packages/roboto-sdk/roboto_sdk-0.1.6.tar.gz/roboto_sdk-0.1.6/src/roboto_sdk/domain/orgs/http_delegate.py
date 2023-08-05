#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Optional

from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    headers_for_org_and_user,
)
from ...serde import pydantic_jsonable_dict
from .delegate import OrgDelegate
from .http_resources import (
    BindEmailDomainRequest,
    CreateOrgRequest,
    InviteUserRequest,
    ModifyRoleForUserRequest,
    RemoveUserFromOrgRequest,
)
from .record import (
    OrgInviteRecord,
    OrgRecord,
    OrgRoleName,
    OrgRoleRecord,
    OrgType,
)


class OrgHttpDelegate(OrgDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        super().__init__()
        self.__http_client = http_client

    def create_org(
        self,
        creator_user_id: Optional[str],
        name: str,
        org_type: OrgType,
        bind_email_domain: bool = False,
    ) -> OrgRecord:
        url = self.__http_client.url("v1/orgs")
        headers = headers_for_org_and_user(user_id=creator_user_id)
        headers["Content-Type"] = "application/json"

        request_body = CreateOrgRequest(
            name=name, org_type=org_type, bind_email_domain=bind_email_domain
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

        return OrgRecord.parse_obj(response.from_json(json_path=["data"]))

    def orgs_for_user(self, user_id: Optional[str]) -> list[OrgRecord]:
        url = self.__http_client.url("v1/orgs/list")

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)

        return [
            OrgRecord.parse_obj(record)
            for record in response.from_json(json_path=["data"])
        ]

    def org_roles_for_user(self, user_id: Optional[str]) -> list[OrgRoleRecord]:
        url = self.__http_client.url("v1/orgs/roles/user")

        headers = headers_for_org_and_user(user_id=user_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url, headers=headers)

        return [
            OrgRoleRecord.parse_obj(record)
            for record in response.from_json(json_path=["data"])
        ]

    def add_role_for_user(
        self, user_id: str, role_name: OrgRoleName, org_id: Optional[str] = None
    ):
        url = self.__http_client.url("v1/orgs/roles/user")
        headers = headers_for_org_and_user(org_id=org_id)
        request_body = ModifyRoleForUserRequest(user_id=user_id, role_name=role_name)

        with RobotoHttpExceptionParse():
            self.__http_client.put(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

    def remove_role_from_user(
        self, user_id: str, role_name: OrgRoleName, org_id: Optional[str] = None
    ):
        url = self.__http_client.url("v1/orgs/roles/user")
        headers = headers_for_org_and_user(org_id=org_id)
        request_body = ModifyRoleForUserRequest(user_id=user_id, role_name=role_name)

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

    def org_roles_for_org(self, org_id: Optional[str]) -> list[OrgRoleRecord]:
        url = self.__http_client.url("v1/orgs/roles")

        headers = headers_for_org_and_user(org_id=org_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url, headers=headers)

        return [
            OrgRoleRecord.parse_obj(record)
            for record in response.from_json(json_path=["data"])
        ]

    def remove_user_from_org(self, user_id: str, org_id: Optional[str] = None) -> None:
        url = self.__http_client.url("v1/orgs/users")

        headers = headers_for_org_and_user(org_id=org_id)

        request_body = RemoveUserFromOrgRequest(user_id=user_id)

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

    def get_org_by_id(self, org_id: str) -> OrgRecord:
        url = self.__http_client.url("v1/orgs")
        headers = headers_for_org_and_user(org_id=org_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url, headers=headers)

        return OrgRecord.parse_obj(response.from_json(json_path=["data"]))

    def delete_org(self, org_id: str) -> None:
        url = self.__http_client.url("v1/orgs")
        headers = headers_for_org_and_user(org_id=org_id)

        with RobotoHttpExceptionParse():
            self.__http_client.delete(url=url, headers=headers)

    def bind_email_domain(self, org_id: str, email_domain: str):
        url = self.__http_client.url("v1/orgs/subdomains")
        headers = headers_for_org_and_user(org_id=org_id)
        request_body = BindEmailDomainRequest(email_domain=email_domain)

        with RobotoHttpExceptionParse():
            self.__http_client.put(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

    def invite_user_to_org(
        self, invited_user_id: str, org_id: str, inviting_user_id: Optional[str] = None
    ) -> OrgInviteRecord:
        url = self.__http_client.url("v1/orgs/invites")
        headers = headers_for_org_and_user(org_id=org_id)
        request_body = InviteUserRequest(invited_user_id=invited_user_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

        return OrgInviteRecord.parse_obj(response.from_json(json_path=["data"]))

    def accept_org_invite(self, invite_id: str, user_id: Optional[str] = None):
        url = self.__http_client.url(f"v1/orgs/invites/accept/{invite_id}")

        with RobotoHttpExceptionParse():
            self.__http_client.post(url=url)

    def decline_org_invite(self, invite_id: str, user_id: Optional[str] = None):
        url = self.__http_client.url(f"v1/orgs/invites/decline/{invite_id}")

        with RobotoHttpExceptionParse():
            self.__http_client.post(url=url)

    def get_org_invite(
        self, invite_id: str, user_id: Optional[str] = None
    ) -> OrgInviteRecord:
        url = self.__http_client.url(f"v1/orgs/invites/id/{invite_id}")

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)
        return OrgInviteRecord.parse_obj(response.from_json(json_path=["data"]))

    def org_role_for_user_in_org(
        self, user_id: Optional[str] = None, org_id: Optional[str] = None
    ) -> OrgRoleRecord:
        raise NotImplementedError("No HTTP endpoint exists for this operation!")
