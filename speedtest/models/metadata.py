import datetime

from pydantic import BaseModel, Field, computed_field


class Metadata(BaseModel):
    hostname: str
    client_ip: str = Field(alias="clientIp")
    http_protocol: str = Field(alias="httpProtocol")
    asn: int
    isp: str = Field(alias="asOrganization")
    colo: str
    country: str
    city: str
    region: str
    postal_code: str = Field(alias="postalCode")
    latitude: str
    longitude: str

    @computed_field
    @property
    def is_ipv6(self) -> bool:
        return ":" in self.client_ip

    @computed_field
    @property
    def date(self) -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)
