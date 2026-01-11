import datetime

from pydantic import BaseModel, Field, computed_field, field_validator


class Metadata(BaseModel):
    hostname: str
    client_ip: str = Field(alias="clientIp")
    http_protocol: str = Field(alias="httpProtocol")
    asn: int
    isp: str = Field(alias="asOrganization")
    colo: str
    country: str
    city: str | None = Field(default="N/A")
    region: str | None = Field(default="N/A")
    postal_code: str | None = Field(alias="postalCode", default="N/A")
    latitude: str
    longitude: str

    @field_validator("colo", mode="before")
    @classmethod
    def extract_colo_iata(cls, v):
        """Extract IATA code from colo object if present."""
        if isinstance(v, dict):
            return v.get("iata", "N/A")
        return v  # Return as-is if already a string

    @computed_field
    @property
    def is_ipv6(self) -> bool:
        return ":" in self.client_ip

    @computed_field
    @property
    def date(self) -> datetime.datetime:
        return datetime.datetime.now(datetime.UTC)
