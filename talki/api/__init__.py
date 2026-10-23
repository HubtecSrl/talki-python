"""The API's operations, one package per tag, and `Resources` / `AsyncResources`,
one attribute per tag, which `Talki` and `AsyncTalki` mix in."""

from functools import cached_property

from ..client import AuthenticatedClient
from .account import AccountResource, AsyncAccountResource
from .appointments import AppointmentsResource, AsyncAppointmentsResource
from .availability import AsyncAvailabilityResource, AvailabilityResource
from .caller_rules import AsyncCallerRulesResource, CallerRulesResource
from .calls import AsyncCallsResource, CallsResource
from .closures import AsyncClosuresResource, ClosuresResource
from .contacts import AsyncContactsResource, ContactsResource
from .locations import AsyncLocationsResource, LocationsResource
from .pending_contacts import AsyncPendingContactsResource, PendingContactsResource
from .resources import AsyncResourcesResource, ResourcesResource
from .sandbox import AsyncSandboxResource, SandboxResource
from .services import AsyncServicesResource, ServicesResource
from .tags import AsyncTagsResource, TagsResource
from .unresolved_requests import AsyncUnresolvedRequestsResource, UnresolvedRequestsResource
from .usage import AsyncUsageResource, UsageResource
from .voices import AsyncVoicesResource, VoicesResource
from .working_hours import AsyncWorkingHoursResource, WorkingHoursResource

__all__ = ["AsyncResources", "Resources"]


class Resources:
    """The operations of every tag, on the generated `client`."""

    client: AuthenticatedClient

    @cached_property
    def account(self) -> AccountResource:
        """The `account` operations."""
        return AccountResource(self.client)

    @cached_property
    def appointments(self) -> AppointmentsResource:
        """The `appointments` operations."""
        return AppointmentsResource(self.client)

    @cached_property
    def availability(self) -> AvailabilityResource:
        """The `availability` operations."""
        return AvailabilityResource(self.client)

    @cached_property
    def caller_rules(self) -> CallerRulesResource:
        """The `caller_rules` operations."""
        return CallerRulesResource(self.client)

    @cached_property
    def calls(self) -> CallsResource:
        """The `calls` operations."""
        return CallsResource(self.client)

    @cached_property
    def closures(self) -> ClosuresResource:
        """The `closures` operations."""
        return ClosuresResource(self.client)

    @cached_property
    def contacts(self) -> ContactsResource:
        """The `contacts` operations."""
        return ContactsResource(self.client)

    @cached_property
    def locations(self) -> LocationsResource:
        """The `locations` operations."""
        return LocationsResource(self.client)

    @cached_property
    def pending_contacts(self) -> PendingContactsResource:
        """The `pending_contacts` operations."""
        return PendingContactsResource(self.client)

    @cached_property
    def resources(self) -> ResourcesResource:
        """The `resources` operations."""
        return ResourcesResource(self.client)

    @cached_property
    def sandbox(self) -> SandboxResource:
        """The `sandbox` operations."""
        return SandboxResource(self.client)

    @cached_property
    def services(self) -> ServicesResource:
        """The `services` operations."""
        return ServicesResource(self.client)

    @cached_property
    def tags(self) -> TagsResource:
        """The `tags` operations."""
        return TagsResource(self.client)

    @cached_property
    def unresolved_requests(self) -> UnresolvedRequestsResource:
        """The `unresolved_requests` operations."""
        return UnresolvedRequestsResource(self.client)

    @cached_property
    def usage(self) -> UsageResource:
        """The `usage` operations."""
        return UsageResource(self.client)

    @cached_property
    def voices(self) -> VoicesResource:
        """The `voices` operations."""
        return VoicesResource(self.client)

    @cached_property
    def working_hours(self) -> WorkingHoursResource:
        """The `working_hours` operations."""
        return WorkingHoursResource(self.client)


class AsyncResources:
    """The async operations of every tag, on the generated `client`."""

    client: AuthenticatedClient

    @cached_property
    def account(self) -> AsyncAccountResource:
        """The `account` operations."""
        return AsyncAccountResource(self.client)

    @cached_property
    def appointments(self) -> AsyncAppointmentsResource:
        """The `appointments` operations."""
        return AsyncAppointmentsResource(self.client)

    @cached_property
    def availability(self) -> AsyncAvailabilityResource:
        """The `availability` operations."""
        return AsyncAvailabilityResource(self.client)

    @cached_property
    def caller_rules(self) -> AsyncCallerRulesResource:
        """The `caller_rules` operations."""
        return AsyncCallerRulesResource(self.client)

    @cached_property
    def calls(self) -> AsyncCallsResource:
        """The `calls` operations."""
        return AsyncCallsResource(self.client)

    @cached_property
    def closures(self) -> AsyncClosuresResource:
        """The `closures` operations."""
        return AsyncClosuresResource(self.client)

    @cached_property
    def contacts(self) -> AsyncContactsResource:
        """The `contacts` operations."""
        return AsyncContactsResource(self.client)

    @cached_property
    def locations(self) -> AsyncLocationsResource:
        """The `locations` operations."""
        return AsyncLocationsResource(self.client)

    @cached_property
    def pending_contacts(self) -> AsyncPendingContactsResource:
        """The `pending_contacts` operations."""
        return AsyncPendingContactsResource(self.client)

    @cached_property
    def resources(self) -> AsyncResourcesResource:
        """The `resources` operations."""
        return AsyncResourcesResource(self.client)

    @cached_property
    def sandbox(self) -> AsyncSandboxResource:
        """The `sandbox` operations."""
        return AsyncSandboxResource(self.client)

    @cached_property
    def services(self) -> AsyncServicesResource:
        """The `services` operations."""
        return AsyncServicesResource(self.client)

    @cached_property
    def tags(self) -> AsyncTagsResource:
        """The `tags` operations."""
        return AsyncTagsResource(self.client)

    @cached_property
    def unresolved_requests(self) -> AsyncUnresolvedRequestsResource:
        """The `unresolved_requests` operations."""
        return AsyncUnresolvedRequestsResource(self.client)

    @cached_property
    def usage(self) -> AsyncUsageResource:
        """The `usage` operations."""
        return AsyncUsageResource(self.client)

    @cached_property
    def voices(self) -> AsyncVoicesResource:
        """The `voices` operations."""
        return AsyncVoicesResource(self.client)

    @cached_property
    def working_hours(self) -> AsyncWorkingHoursResource:
        """The `working_hours` operations."""
        return AsyncWorkingHoursResource(self.client)
