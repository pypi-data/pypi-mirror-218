#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any, Optional

from ...serde import pydantic_jsonable_dict
from .delegate import OrgDelegate
from .org import Org
from .record import OrgInviteRecord


class OrgInvite:
    __org_delegate: OrgDelegate
    __org: Org
    __record: OrgInviteRecord

    @classmethod
    def create(
        cls,
        invited_user_id: str,
        org_id: str,
        org_delegate: OrgDelegate,
        inviting_user_id: Optional[str] = None,
    ) -> "OrgInvite":
        record = org_delegate.invite_user_to_org(
            invited_user_id=invited_user_id,
            inviting_user_id=inviting_user_id,
            org_id=org_id,
        )
        return cls(record=record, org_delegate=org_delegate)

    @classmethod
    def from_id(
        cls, invite_id: str, org_delegate: OrgDelegate, user_id: Optional[str] = None
    ):
        record = org_delegate.get_org_invite(invite_id=invite_id, user_id=user_id)
        return cls(record=record, org_delegate=org_delegate)

    def accept(self, user_id: Optional[str]):
        self.__org_delegate.accept_org_invite(
            invite_id=self.__record.invite_id, user_id=user_id
        )

    def decline(self, user_id: Optional[str]):
        self.__org_delegate.decline_org_invite(
            invite_id=self.__record.invite_id, user_id=user_id
        )

    @property
    def invite_id(self) -> str:
        return self.__record.invite_id

    def __init__(self, record: OrgInviteRecord, org_delegate: OrgDelegate):
        self.__record = record
        self.__org_delegate = org_delegate
        self.__org = Org(record=record.org, org_delegate=org_delegate)

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)
