# Please do not use
#     from __future__ import annotations
# in modules such as this one where hybrid cloud data models or service classes are
# defined, because we want to reflect on type annotations and avoid forward references.

import abc
from typing import Any, Mapping, Optional

from sentry.services.hybrid_cloud.app import (
    RpcAlertRuleActionResult,
    RpcSentryApp,
    RpcSentryAppComponent,
    RpcSentryAppEventData,
    RpcSentryAppInstallation,
    RpcSentryAppService,
    SentryAppInstallationFilterArgs,
)
from sentry.services.hybrid_cloud.auth import AuthenticationContext
from sentry.services.hybrid_cloud.filter_query import OpaqueSerializedResponse
from sentry.services.hybrid_cloud.rpc import RpcService, rpc_method
from sentry.services.hybrid_cloud.user import RpcUser
from sentry.silo import SiloMode


class AppService(RpcService):
    key = "app"
    local_mode = SiloMode.CONTROL

    @classmethod
    def get_local_implementation(cls) -> RpcService:
        from sentry.services.hybrid_cloud.app.impl import DatabaseBackedAppService

        return DatabaseBackedAppService()

    @rpc_method
    @abc.abstractmethod
    def serialize_many(
        self,
        *,
        filter: SentryAppInstallationFilterArgs,
        as_user: Optional[RpcUser] = None,
        auth_context: Optional[AuthenticationContext] = None,
    ) -> list[OpaqueSerializedResponse]:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_many(
        self, *, filter: SentryAppInstallationFilterArgs
    ) -> list[RpcSentryAppInstallation]:
        pass

    @rpc_method
    @abc.abstractmethod
    def find_installation_by_proxy_user(
        self, *, proxy_user_id: int, organization_id: int
    ) -> Optional[RpcSentryAppInstallation]:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_installed_for_organization(
        self,
        *,
        organization_id: int,
    ) -> list[RpcSentryAppInstallation]:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_sentry_app_by_id(self, *, id: int) -> Optional[RpcSentryApp]:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_sentry_app_by_slug(self, *, slug: str) -> Optional[RpcSentryApp]:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_installation_by_id(self, *, id: int) -> Optional[RpcSentryAppInstallation]:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_installation(
        self, *, sentry_app_id: int, organization_id: int
    ) -> Optional[RpcSentryAppInstallation]:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_installation_token(self, *, organization_id: int, provider: str) -> Optional[str]:
        pass

    @rpc_method
    @abc.abstractmethod
    def find_alertable_services(self, *, organization_id: int) -> list[RpcSentryAppService]:
        pass

    @rpc_method
    @abc.abstractmethod
    def find_service_hook_sentry_app(self, *, api_application_id: int) -> Optional[RpcSentryApp]:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_custom_alert_rule_actions(
        self,
        *,
        event_data: RpcSentryAppEventData,
        organization_id: int,
        project_slug: Optional[str],
    ) -> list[Mapping[str, Any]]:
        pass

    @rpc_method
    @abc.abstractmethod
    def find_app_components(self, *, app_id: int) -> list[RpcSentryAppComponent]:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_related_sentry_app_components(
        self,
        *,
        organization_ids: list[int],
        sentry_app_ids: list[int],
        type: str,
        group_by: str = "sentry_app_id",
    ) -> Mapping[str, Any]:
        pass

    @rpc_method
    @abc.abstractmethod
    def trigger_sentry_app_action_creators(
        self, *, fields: list[Mapping[str, Any]], install_uuid: Optional[str]
    ) -> RpcAlertRuleActionResult:
        pass

    @rpc_method
    @abc.abstractmethod
    def get_published_sentry_apps_for_organization(
        self, *, organization_id: int
    ) -> list[RpcSentryApp]:
        pass

    @rpc_method
    @abc.abstractmethod
    def create_internal_integration_for_channel_request(
        self,
        *,
        organization_id: int,
        integration_name: str,
        integration_scopes: list[str],
        integration_creator_id: int,
        metadata: Optional[dict[str, Any]] = None,
    ) -> RpcSentryAppInstallation:
        pass

    @rpc_method
    @abc.abstractmethod
    def prepare_sentry_app_components(
        self, *, installation_id: int, component_type: str, project_slug: Optional[str] = None
    ) -> Optional[RpcSentryAppComponent]:
        pass

    @rpc_method
    @abc.abstractmethod
    def disable_sentryapp(self, *, id: int) -> None:
        pass


app_service = AppService.create_delegation()
