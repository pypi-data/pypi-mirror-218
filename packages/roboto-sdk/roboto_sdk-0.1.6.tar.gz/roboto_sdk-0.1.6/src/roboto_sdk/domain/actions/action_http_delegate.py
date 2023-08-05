import http
import json
from typing import Any, Optional

from ...exceptions import RobotoDomainException
from ...http import (
    ORG_OVERRIDE_HEADER,
    USER_OVERRIDE_HEADER,
    ClientError,
    HttpClient,
)
from ...logging import default_logger
from ...pagination import PaginatedList
from ...serde import pydantic_jsonable_dict
from .action_container_resources import (
    ComputeRequirements,
    ContainerCredentials,
    ContainerParameters,
)
from .action_delegate import (
    ActionDelegate,
    UpdateCondition,
)
from .action_http_resources import (
    CreateActionRequest,
    UpdateActionRequest,
)
from .action_record import ActionRecord
from .error import (
    ActionUpdateConditionCheckFailure,
)

logger = default_logger()


class ActionHttpDelegate(ActionDelegate):
    """
    Use in any context that does not have direct database access.
    """

    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def headers(
        self, org_id: Optional[str] = None, user_id: Optional[str] = None
    ) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if org_id:
            headers[ORG_OVERRIDE_HEADER] = org_id
        if user_id:
            headers[USER_OVERRIDE_HEADER] = user_id
        return headers

    def create_action(
        self,
        name: str,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        compute_requirements: Optional[ComputeRequirements] = None,
        container_parameters: Optional[ContainerParameters] = None,
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions"
        request_body = CreateActionRequest(
            name=name,
            description=description,
            metadata=metadata,
            tags=tags,
            compute_requirements=compute_requirements,
            container_parameters=container_parameters,
        )
        response = self.__http_client.post(
            url,
            data=pydantic_jsonable_dict(request_body, exclude_none=True),
            headers=self.headers(org_id, created_by),
        )
        return ActionRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_action_by_primary_key(
        self, name: str, org_id: Optional[str] = None
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{name}"
        try:
            res = self.__http_client.get(url, headers=self.headers(org_id))
            return ActionRecord.parse_obj(res.from_json(json_path=["data"]))
        except ClientError as exc:
            raise RobotoDomainException.from_client_error(exc)

    def register_container(
        self,
        record: ActionRecord,
        image_name: str,
        image_tag: str,
        caller: Optional[str] = None,
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}/container"
        data = {
            "image_name": image_name,
            "image_tag": image_tag,
        }

        response = self.__http_client.put(
            url, data=data, headers=self.headers(user_id=caller)
        )
        return ActionRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_temp_container_credentials(
        self,
        record: ActionRecord,
        caller: Optional[str] = None,
    ) -> ContainerCredentials:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}/container/credentials"
        res = self.__http_client.get(url, headers=self.headers(user_id=caller))
        return ContainerCredentials.parse_obj(res.from_json(json_path=["data"]))

    def query_actions(
        self,
        filters: dict[str, Any],
        org_id: Optional[str] = None,
        page_token: Optional[dict[str, str]] = None,
    ) -> PaginatedList[ActionRecord]:
        if page_token:
            filters["page_token"] = page_token

        safe_filters = json.loads(json.dumps(filters))
        url = f"{self.__roboto_service_base_url}/v1/actions/query"
        res = self.__http_client.post(
            url, data=safe_filters, headers=self.headers(org_id)
        )
        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                ActionRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

    def update(
        self,
        record: ActionRecord,
        updates: dict[str, Any],
        conditions: Optional[list[UpdateCondition]],
        org_id: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}"
        payload = UpdateActionRequest(
            updates=updates,
            conditions=conditions if conditions is not None else [],
        )
        try:
            res = self.__http_client.patch(
                url, data=payload.dict(), headers=self.headers(org_id, updated_by)
            )
            return ActionRecord.parse_obj(res.from_json(json_path=["data"]))
        except ClientError as exc:
            if exc.status == http.HTTPStatus.CONFLICT:
                raise ActionUpdateConditionCheckFailure(exc.msg) from None
            raise
