import abc
from typing import Any, Optional

from ...pagination import PaginatedList
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_record import ActionRecord
from .invocation_record import (
    InvocationDataSourceType,
    InvocationRecord,
    InvocationSource,
    InvocationStatus,
)


class InvocationDelegate(abc.ABC):
    @abc.abstractmethod
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
        """Create an Invocation"""
        raise NotImplementedError("create_invocation")

    @abc.abstractmethod
    def get_by_id(
        self, invocation_id: str, org_id: Optional[str] = None
    ) -> InvocationRecord:
        """Get an Invocation by ID"""
        raise NotImplementedError("get_by_id")

    @abc.abstractmethod
    def set_logs_location(
        self, record: InvocationRecord, bucket: str, prefix: str
    ) -> InvocationRecord:
        raise NotImplementedError("set_logs_location")

    @abc.abstractmethod
    def update_invocation_status(
        self,
        record: InvocationRecord,
        status: InvocationStatus,
        detail: Optional[str] = None,
    ) -> InvocationRecord:
        """Update the status of an Invocation"""
        raise NotImplementedError("update_invocation_status")

    @abc.abstractmethod
    def query_invocations(
        self,
        filters: dict[str, Any],
        org_id: Optional[str] = None,
        page_token: Optional[dict[str, str]] = None,
    ) -> PaginatedList[InvocationRecord]:
        raise NotImplementedError("query_invocations")
