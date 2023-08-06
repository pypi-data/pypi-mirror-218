from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.config_ui_feature_flags import ConfigUIFeatureFlags


T = TypeVar("T", bound="NodeApiGetUIClientConfigResponse")


@attr.s(auto_attribs=True)
class NodeApiGetUIClientConfigResponse:
    """
    Attributes:
        agora_app_id (Union[Unset, str]):
        backend_endpoint_url (Union[Unset, str]):
        blockchain_id (Union[Unset, str]):
        contract_dad_address (Union[Unset, str]):
        contract_faucet_address (Union[Unset, str]):
        contract_mom_address (Union[Unset, str]):
        contract_nft_address (Union[Unset, str]):
        contract_staking_address (Union[Unset, str]):
        feature_flags (Union[Unset, ConfigUIFeatureFlags]):
        node_id (Union[Unset, str]):
        render_service_url (Union[Unset, str]):
        streamchat_key (Union[Unset, str]):
    """

    agora_app_id: Unset | str = UNSET
    backend_endpoint_url: Unset | str = UNSET
    blockchain_id: Unset | str = UNSET
    contract_dad_address: Unset | str = UNSET
    contract_faucet_address: Unset | str = UNSET
    contract_mom_address: Unset | str = UNSET
    contract_nft_address: Unset | str = UNSET
    contract_staking_address: Unset | str = UNSET
    feature_flags: Union[Unset, "ConfigUIFeatureFlags"] = UNSET
    node_id: Unset | str = UNSET
    render_service_url: Unset | str = UNSET
    streamchat_key: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agora_app_id = self.agora_app_id
        backend_endpoint_url = self.backend_endpoint_url
        blockchain_id = self.blockchain_id
        contract_dad_address = self.contract_dad_address
        contract_faucet_address = self.contract_faucet_address
        contract_mom_address = self.contract_mom_address
        contract_nft_address = self.contract_nft_address
        contract_staking_address = self.contract_staking_address
        feature_flags: Unset | dict[str, Any] = UNSET
        if not isinstance(self.feature_flags, Unset):
            feature_flags = self.feature_flags.to_dict()

        node_id = self.node_id
        render_service_url = self.render_service_url
        streamchat_key = self.streamchat_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agora_app_id is not UNSET:
            field_dict["AGORA_APP_ID"] = agora_app_id
        if backend_endpoint_url is not UNSET:
            field_dict["BACKEND_ENDPOINT_URL"] = backend_endpoint_url
        if blockchain_id is not UNSET:
            field_dict["BLOCKCHAIN_ID"] = blockchain_id
        if contract_dad_address is not UNSET:
            field_dict["CONTRACT_DAD_ADDRESS"] = contract_dad_address
        if contract_faucet_address is not UNSET:
            field_dict["CONTRACT_FAUCET_ADDRESS"] = contract_faucet_address
        if contract_mom_address is not UNSET:
            field_dict["CONTRACT_MOM_ADDRESS"] = contract_mom_address
        if contract_nft_address is not UNSET:
            field_dict["CONTRACT_NFT_ADDRESS"] = contract_nft_address
        if contract_staking_address is not UNSET:
            field_dict["CONTRACT_STAKING_ADDRESS"] = contract_staking_address
        if feature_flags is not UNSET:
            field_dict["FEATURE_FLAGS"] = feature_flags
        if node_id is not UNSET:
            field_dict["NODE_ID"] = node_id
        if render_service_url is not UNSET:
            field_dict["RENDER_SERVICE_URL"] = render_service_url
        if streamchat_key is not UNSET:
            field_dict["STREAMCHAT_KEY"] = streamchat_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.config_ui_feature_flags import ConfigUIFeatureFlags

        d = src_dict.copy()
        agora_app_id = d.pop("AGORA_APP_ID", UNSET)

        backend_endpoint_url = d.pop("BACKEND_ENDPOINT_URL", UNSET)

        blockchain_id = d.pop("BLOCKCHAIN_ID", UNSET)

        contract_dad_address = d.pop("CONTRACT_DAD_ADDRESS", UNSET)

        contract_faucet_address = d.pop("CONTRACT_FAUCET_ADDRESS", UNSET)

        contract_mom_address = d.pop("CONTRACT_MOM_ADDRESS", UNSET)

        contract_nft_address = d.pop("CONTRACT_NFT_ADDRESS", UNSET)

        contract_staking_address = d.pop("CONTRACT_STAKING_ADDRESS", UNSET)

        _feature_flags = d.pop("FEATURE_FLAGS", UNSET)
        feature_flags: Unset | ConfigUIFeatureFlags
        if isinstance(_feature_flags, Unset):
            feature_flags = UNSET
        else:
            feature_flags = ConfigUIFeatureFlags.from_dict(_feature_flags)

        node_id = d.pop("NODE_ID", UNSET)

        render_service_url = d.pop("RENDER_SERVICE_URL", UNSET)

        streamchat_key = d.pop("STREAMCHAT_KEY", UNSET)

        node_api_get_ui_client_config_response = cls(
            agora_app_id=agora_app_id,
            backend_endpoint_url=backend_endpoint_url,
            blockchain_id=blockchain_id,
            contract_dad_address=contract_dad_address,
            contract_faucet_address=contract_faucet_address,
            contract_mom_address=contract_mom_address,
            contract_nft_address=contract_nft_address,
            contract_staking_address=contract_staking_address,
            feature_flags=feature_flags,
            node_id=node_id,
            render_service_url=render_service_url,
            streamchat_key=streamchat_key,
        )

        node_api_get_ui_client_config_response.additional_properties = d
        return node_api_get_ui_client_config_response

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
