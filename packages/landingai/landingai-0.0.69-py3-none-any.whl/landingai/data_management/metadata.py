from typing import Any, Dict, List, Optional, Union

from landingai.data_management.client import METADATA_UPDATE, LandingLens
from landingai.data_management.utils import (
    PrettyPrintable,
    obj_to_dict,
    validate_metadata,
)


class Metadata:
    """Metadata management API client.
    This class provides a set of APIs to manage the metadata of the medias (images) uploaded to LandingLens.
    For example, you can use this class to update the metadata of the uploaded medias.
    """

    def __init__(self, api_key: str, project_id: int):
        self._client = LandingLens(api_key=api_key, project_id=project_id)

    def update(
        self,
        media_ids: Union[int, List[int]],
        **input_metadata: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        project_id = self._client._project_id
        if (
            not media_ids
            or isinstance(media_ids, bool)
            or (not isinstance(media_ids, int) and len(media_ids) == 0)
        ):
            raise ValueError("Missing required flags: {'media_ids'}")

        if not input_metadata or len(input_metadata) == 0:
            raise ValueError("Missing required flags: {'metadata'}")

        dataset_id = self._client.get_project_property(project_id, "dataset_id")

        if isinstance(media_ids, int):
            media_ids = [media_ids]
        else:
            # to avoid errors due to things like numpy.int
            media_ids = list(map(int, media_ids))

        metadata_mapping, id_to_metadata = self._client.get_metadata_mappings(
            project_id
        )

        body = _MetadataUploadRequestBody(
            selectOption=_SelectOption(media_ids),
            project=_Project(project_id, dataset_id),
            metadata=_metadata_to_ids(input_metadata, metadata_mapping),
        )

        resp = self._client._api(METADATA_UPDATE, data=obj_to_dict(body))
        resp_data = resp["data"]
        return {
            "project_id": project_id,
            "metadata": _ids_to_metadata(resp_data[0]["metadata"], id_to_metadata),
            "media_ids": [media["objectId"] for media in resp_data],
        }


class _SelectOption(PrettyPrintable):
    def __init__(self, selected_media: List[int]) -> None:
        self.selected_media = selected_media
        self.unselected_media: List[Union[int, List[int]]] = []
        self.field_filter_map: Dict[str, Any] = {}
        self.column_filter_map: Dict[str, Any] = {}
        self.is_unselect_mode = False


class _Project(PrettyPrintable):
    def __init__(
        self,
        project_id: int,
        dataset_id: int,
    ) -> None:
        self.project_id = project_id
        self.dataset_id = dataset_id


class _MetadataUploadRequestBody(PrettyPrintable):
    def __init__(
        self,
        selectOption: _SelectOption,
        project: _Project,
        metadata: Dict[str, Any],
    ) -> None:
        self.selectOption = selectOption
        self.project = project
        self.metadata = metadata


def _metadata_to_ids(
    input_metadata: Dict[str, Any], metadata_mapping: Dict[str, Any]
) -> Dict[str, Any]:
    validate_metadata(input_metadata, metadata_mapping)
    return {
        metadata_mapping[key][0]: val
        for key, val in input_metadata.items()
        if key in metadata_mapping
    }


def _ids_to_metadata(
    metadata_ids: Dict[str, Any], id_to_metadata: Dict[int, str]
) -> Dict[str, Any]:
    return {
        id_to_metadata[int(key)]: val
        for key, val in metadata_ids.items()
        if int(key) in id_to_metadata
    }
