from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dto_object_options_child_placement import DtoObjectOptionsChildPlacement
    from ..models.dto_object_options_frame_templates import DtoObjectOptionsFrameTemplates
    from ..models.dto_object_options_subs import DtoObjectOptionsSubs


T = TypeVar("T", bound="DtoObjectOptions")


@attr.s(auto_attribs=True)
class DtoObjectOptions:
    """
    Attributes:
        allowed_subobjects (Union[Unset, List[str]]):
        asset_2d_options (Union[Unset, Any]):
        asset_3d_options (Union[Unset, Any]):
        child_placement (Union[Unset, DtoObjectOptionsChildPlacement]):
        dashboard_plugins (Union[Unset, List[str]]):
        default_tiles (Union[Unset, List[Any]]):
        editable (Union[Unset, bool]):
        frame_templates (Union[Unset, DtoObjectOptionsFrameTemplates]):
        infoui_id (Union[Unset, str]):
        minimap (Union[Unset, bool]):
        private (Union[Unset, bool]):
        subs (Union[Unset, DtoObjectOptionsSubs]):
        visible (Union[Unset, int]):
    """

    allowed_subobjects: Unset | list[str] = UNSET
    asset_2d_options: Unset | Any = UNSET
    asset_3d_options: Unset | Any = UNSET
    child_placement: Union[Unset, "DtoObjectOptionsChildPlacement"] = UNSET
    dashboard_plugins: Unset | list[str] = UNSET
    default_tiles: Unset | list[Any] = UNSET
    editable: Unset | bool = UNSET
    frame_templates: Union[Unset, "DtoObjectOptionsFrameTemplates"] = UNSET
    infoui_id: Unset | str = UNSET
    minimap: Unset | bool = UNSET
    private: Unset | bool = UNSET
    subs: Union[Unset, "DtoObjectOptionsSubs"] = UNSET
    visible: Unset | int = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allowed_subobjects: Unset | list[str] = UNSET
        if not isinstance(self.allowed_subobjects, Unset):
            allowed_subobjects = self.allowed_subobjects

        asset_2d_options = self.asset_2d_options
        asset_3d_options = self.asset_3d_options
        child_placement: Unset | dict[str, Any] = UNSET
        if not isinstance(self.child_placement, Unset):
            child_placement = self.child_placement.to_dict()

        dashboard_plugins: Unset | list[str] = UNSET
        if not isinstance(self.dashboard_plugins, Unset):
            dashboard_plugins = self.dashboard_plugins

        default_tiles: Unset | list[Any] = UNSET
        if not isinstance(self.default_tiles, Unset):
            default_tiles = self.default_tiles

        editable = self.editable
        frame_templates: Unset | dict[str, Any] = UNSET
        if not isinstance(self.frame_templates, Unset):
            frame_templates = self.frame_templates.to_dict()

        infoui_id = self.infoui_id
        minimap = self.minimap
        private = self.private
        subs: Unset | dict[str, Any] = UNSET
        if not isinstance(self.subs, Unset):
            subs = self.subs.to_dict()

        visible = self.visible

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed_subobjects is not UNSET:
            field_dict["allowed_subobjects"] = allowed_subobjects
        if asset_2d_options is not UNSET:
            field_dict["asset_2d_options"] = asset_2d_options
        if asset_3d_options is not UNSET:
            field_dict["asset_3d_options"] = asset_3d_options
        if child_placement is not UNSET:
            field_dict["child_placement"] = child_placement
        if dashboard_plugins is not UNSET:
            field_dict["dashboard_plugins"] = dashboard_plugins
        if default_tiles is not UNSET:
            field_dict["default_tiles"] = default_tiles
        if editable is not UNSET:
            field_dict["editable"] = editable
        if frame_templates is not UNSET:
            field_dict["frame_templates"] = frame_templates
        if infoui_id is not UNSET:
            field_dict["infoui_id"] = infoui_id
        if minimap is not UNSET:
            field_dict["minimap"] = minimap
        if private is not UNSET:
            field_dict["private"] = private
        if subs is not UNSET:
            field_dict["subs"] = subs
        if visible is not UNSET:
            field_dict["visible"] = visible

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dto_object_options_child_placement import DtoObjectOptionsChildPlacement
        from ..models.dto_object_options_frame_templates import DtoObjectOptionsFrameTemplates
        from ..models.dto_object_options_subs import DtoObjectOptionsSubs

        d = src_dict.copy()
        allowed_subobjects = cast(list[str], d.pop("allowed_subobjects", UNSET))

        asset_2d_options = d.pop("asset_2d_options", UNSET)

        asset_3d_options = d.pop("asset_3d_options", UNSET)

        _child_placement = d.pop("child_placement", UNSET)
        child_placement: Unset | DtoObjectOptionsChildPlacement
        if isinstance(_child_placement, Unset):
            child_placement = UNSET
        else:
            child_placement = DtoObjectOptionsChildPlacement.from_dict(_child_placement)

        dashboard_plugins = cast(list[str], d.pop("dashboard_plugins", UNSET))

        default_tiles = cast(list[Any], d.pop("default_tiles", UNSET))

        editable = d.pop("editable", UNSET)

        _frame_templates = d.pop("frame_templates", UNSET)
        frame_templates: Unset | DtoObjectOptionsFrameTemplates
        if isinstance(_frame_templates, Unset):
            frame_templates = UNSET
        else:
            frame_templates = DtoObjectOptionsFrameTemplates.from_dict(_frame_templates)

        infoui_id = d.pop("infoui_id", UNSET)

        minimap = d.pop("minimap", UNSET)

        private = d.pop("private", UNSET)

        _subs = d.pop("subs", UNSET)
        subs: Unset | DtoObjectOptionsSubs
        if isinstance(_subs, Unset):
            subs = UNSET
        else:
            subs = DtoObjectOptionsSubs.from_dict(_subs)

        visible = d.pop("visible", UNSET)

        dto_object_options = cls(
            allowed_subobjects=allowed_subobjects,
            asset_2d_options=asset_2d_options,
            asset_3d_options=asset_3d_options,
            child_placement=child_placement,
            dashboard_plugins=dashboard_plugins,
            default_tiles=default_tiles,
            editable=editable,
            frame_templates=frame_templates,
            infoui_id=infoui_id,
            minimap=minimap,
            private=private,
            subs=subs,
            visible=visible,
        )

        dto_object_options.additional_properties = d
        return dto_object_options

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
