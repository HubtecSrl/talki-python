from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_detail_type import ErrorDetailType

T = TypeVar("T", bound="ErrorDetail")


@_attrs_define
class ErrorDetail:
    """The error itself. Branch on `code`; `message` is for people.

    Attributes:
        type_ (ErrorDetailType):
        code (str): Stable machine code; branch on this, not on `message`. Known codes: `invalid_credentials`,
            `insufficient_scope`, `account_closed`, `subscription_inactive`, `plan_upgrade_required`,
            `plan_feature_unavailable`, `forbidden`, `livemode_required`, `sandbox_api_key_required`, `unsupported_version`,
            `invalid_parameter`, `invalid_cursor`, `method_not_allowed`, `resource_not_found`, `conflict`,
            `precondition_failed`, `payload_too_large`, `export_too_large`, `idempotency_key_required`,
            `idempotency_key_reuse`, `request_in_progress`, `request_conflict`, `rate_limit_exceeded`, `ip_rate_limited`,
            `internal_error`, `api_error`, `booking_refused`, `appointment_cancelled`, `appointment_not_cancelled`,
            `unresolved_request_not_resolved`, `faq_full`, `service_has_upcoming_bookings`, `resource_is_default`,
            `resource_required_by_service`, `capacity_below_committed`, `capacity_below_service_requirement`,
            `resource_too_small`, `tag_limit_reached`, `caller_rule_limit_reached`, `transcript_not_available`,
            `trial_suspended`, `phone_number_missing`, `forwarding_number_missing`, `forwarding_number_invalid`,
            `check_in_progress`, `check_quota_exceeded`, `checks_busy`, `check_call_failed`, `unknown_scenario`,
            `sandbox_not_ready`, `too_many_keys`, `key_not_active`, `key_already_rolled`, `invalid_registration`,
            `client_disabled`, `client_changed`, `delivery_in_progress`, `events_url_unset`, `events_paused`,
            `event_unsubscribed`, `account_refused`, `installation_inactive`, `invalid_client`, `invalid_request`,
            `unauthorized_client`, `access_denied`, `invalid_scope`, `slot_unavailable`, `capacity_exhausted`,
            `service_exclusion`, `closed_day`, `in_the_past`, `outside_hours`, `service_inactive`, `location_inactive`,
            `service_deleted`, `no_services_requested`, `party_too_large`, `stay_too_short`, `stay_too_long`,
            `stay_dates_invalid`. New codes may be added; treat an unknown one by its HTTP status.
        message (str):
        request_id (str):
    """

    type_: ErrorDetailType
    code: str
    message: str
    request_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        code = self.code

        message = self.message

        request_id = self.request_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "code": code,
                "message": message,
                "request_id": request_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ErrorDetailType(d.pop("type"))

        code = d.pop("code")

        message = d.pop("message")

        request_id = d.pop("request_id")

        error_detail = cls(
            type_=type_,
            code=code,
            message=message,
            request_id=request_id,
        )

        error_detail.additional_properties = d
        return error_detail

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
