from optparse import Option
from typing import Set, Union, Optional

from flask import flash
from pydantic import BaseModel, Field, ValidationError
from app.utils import convert_errors, CUSTOM_MESSAGES


class StoreBase(BaseModel):
    name: str = Field(alias="Nama")
    description: Optional[str] = Field(None, alias="Deskripsi")
    open_at: Optional[str] = Field(None, alias="Jam Buka")
    close_at: Optional[str] = Field(None, alias="Jam Tutup")
    categories: Optional[Set[str]] = Field(None, alias="Kategori")
    phone: Optional[str] = Field(None, alias="Nomor HP")
    google_maps: Optional[str] = Field(None, alias="Alamat Google Map")


class StoreCreate(StoreBase):
    user_id: int


class StoreUpdate(StoreBase):
    store_id: int


def validate_store_input(model: StoreCreate = StoreCreate, **data):
    pass
    # try:
    #     StoreCreate(**data)
    # except ValidationError as e:
    #     errors = convert_errors(e, CUSTOM_MESSAGES)
    #     for error in errors:
    #         print(error, "vsi")
    #         field_name = error["loc"][0]
    #         if field_name in model.model_fields:
    #             alias = model.model_fields[field_name].alias
    #             error["loc"] = (alias,) if alias else error["loc"]
    #         flash(f"{error['loc'][0]}: {error['msg']}", "error")
