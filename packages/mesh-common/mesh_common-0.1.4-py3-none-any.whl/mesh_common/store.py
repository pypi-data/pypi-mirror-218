from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Optional

from nhs_aws_helpers.dynamodb_model_store.base_model import (
    BaseModel,
    model_properties_cache,
    serialised_property,
)

from mesh_common import ModelKey, is_dataclass_instance


class BaseMeshModel(BaseModel[ModelKey]):
    _index_model_type: bool = True
    _model_key_type = ModelKey


@dataclass(kw_only=True)
class MeshModel(BaseMeshModel):
    # pk: str
    # sk: str
    last_modified: datetime = field(default_factory=datetime.utcnow)
    created_timestamp: datetime = field(default_factory=datetime.utcnow)

    def _create_key(self) -> ModelKey:
        raise NotImplementedError()

    @serialised_property
    def pk(self) -> str:
        return self._create_key()["pk"]

    @serialised_property
    def sk(self) -> str:
        return self._create_key()["sk"]

    @serialised_property
    def gsi_model_type_pk(self) -> Optional[str]:
        if self._index_model_type:
            return self.__class__.__name__
        return None

    @classmethod
    def _as_dict_value(cls, value: Any) -> Any:
        if not value or isinstance(value, type):
            return value

        if isinstance(value, list):
            return [cls._as_dict_value(val) for val in value]

        if hasattr(value, "as_dict"):
            return value.as_dict()

        if is_dataclass_instance(value):
            return asdict(value)

        return value

    def as_dict(self) -> dict[str, Any]:

        model_fields = model_properties_cache(self.__class__)  # type: ignore[arg-type]

        result: dict[str, Any] = {}

        for field_name, _, _ in model_fields:
            value = getattr(self, field_name)
            result[field_name] = self._as_dict_value(value)

        return result
