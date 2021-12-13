from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.encoders import jsonable_encoder


class Amount(BaseModel):
    currencyCode: str
    value: float


class Contact(BaseModel):
    id: str = Field(None, alias="_id")
    iban: str
    name: str
    organization: str
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)


class Invoice(BaseModel):
    id: str = Field(None, alias="_id")
    organization: str
    createdAt: datetime
    updatedAt: datetime
    amount: Amount
    contact: Contact
    invoiceDate: datetime
    invoiceId: str

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data

class SuggestInvoice(BaseModel):
    organization: str
    contactName: str


class AbnoramlChecking(BaseModel):
    organization: str
    contactName: str
    amount: float

