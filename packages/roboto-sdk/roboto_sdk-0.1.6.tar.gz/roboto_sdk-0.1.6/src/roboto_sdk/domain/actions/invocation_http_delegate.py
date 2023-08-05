import json
from typing import Any, Optional

from ...http import (
    ORG_OVERRIDE_HEADER,
    USER_OVERRIDE_HEADER,
    HttpClient,
)
from ...logging import default_logger
from ...pagination import PaginatedList
from ...serde import pydantic_jsonable_dict
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_record import ActionRecord
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_http_resources import (
    CreateInvocationRequest,
    SetLogsLocationRequest,
)
from .invocation_record import (
    InvocationDataSourceType,
    InvocationRecord,
    InvocationSource,
    InvocationStatus,
)

logger = default_logger()


class InvocationHttpDelegate(InvocationDelegate):
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

    def create_invocation(
        self,
        action_record: ActionRecord,
        input_data: list[str],
        compute_requirements: ComputeRequirements,
        container_parameters: ContainerParameters,
        data_source_id: str,
        data_source_type: InvocationDataSourceType,
        invocation_source: InvocationSource,
        invocation_source_id: Optional[str] = None,
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{action_record.name}/invoke"
        request_body = CreateInvocationRequest(
            input_data=input_data,
            data_source_id=data_source_id,
            data_source_type=data_source_type,
            invocation_source=invocation_source,
            invocation_source_id=invocation_source_id,
            compute_requirements=compute_requirements,
            container_parameters=container_parameters,
        )
        response = self.__http_client.post(
            url,
            data=pydantic_jsonable_dict(request_body, exclude_none=True),
            headers=self.headers(
                org_id=action_record.org_id,
                user_id=invocation_source_id
                if invocation_source == InvocationSource.Manual
                else None,
            ),
        )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_by_id(
        self, invocation_id: str, org_id: Optional[str] = None
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation_id}"
        response = self.__http_client.get(url, headers=self.headers(org_id))
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def set_logs_location(
        self, record: InvocationRecord, bucket: str, prefix: str
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{record.invocation_id}/logs"
        request_body = SetLogsLocationRequest(bucket=bucket, prefix=prefix)
        response = self.__http_client.patch(
            url,
            data=pydantic_jsonable_dict(request_body, exclude_none=True),
            headers=self.headers(record.org_id),
        )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def update_invocation_status(
        self,
        record: InvocationRecord,
        status: InvocationStatus,
        detail: Optional[str] = None,
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{record.invocation_id}/status"
        response = self.__http_client.post(
            url,
            data={"status": status.value, "detail": detail},
            headers=self.headers(record.org_id),
        )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def query_invocations(
        self,
        filters: dict[str, Any],
        org_id: Optional[str] = None,
        page_token: Optional[dict[str, str]] = None,
    ) -> PaginatedList[InvocationRecord]:
        if page_token:
            filters["page_token"] = page_token

        safe_filters = json.loads(json.dumps(filters))
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/query"
        res = self.__http_client.post(
            url, data=safe_filters, headers=self.headers(org_id)
        )
        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                InvocationRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )
