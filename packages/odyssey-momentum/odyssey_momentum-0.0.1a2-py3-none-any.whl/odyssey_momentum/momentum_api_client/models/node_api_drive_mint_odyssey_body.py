from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.node_nft_meta import NodeNFTMeta


T = TypeVar("T", bound="NodeApiDriveMintOdysseyBody")


@attr.s(auto_attribs=True)
class NodeApiDriveMintOdysseyBody:
    """
    Attributes:
        block_hash (str):
        meta (NodeNFTMeta):
        wallet (str):
    """

    block_hash: str
    meta: "NodeNFTMeta"
    wallet: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        block_hash = self.block_hash
        meta = self.meta.to_dict()

        wallet = self.wallet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "block_hash": block_hash,
                "meta": meta,
                "wallet": wallet,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.node_nft_meta import NodeNFTMeta

        d = src_dict.copy()
        block_hash = d.pop("block_hash")

        meta = NodeNFTMeta.from_dict(d.pop("meta"))

        wallet = d.pop("wallet")

        node_api_drive_mint_odyssey_body = cls(
            block_hash=block_hash,
            meta=meta,
            wallet=wallet,
        )

        node_api_drive_mint_odyssey_body.additional_properties = d
        return node_api_drive_mint_odyssey_body

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
