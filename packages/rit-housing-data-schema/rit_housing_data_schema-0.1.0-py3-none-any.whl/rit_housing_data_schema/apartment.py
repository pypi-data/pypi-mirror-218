"""Normalized Location Schema

Spec defined here:
https://github.com/rit-hc-website/data-ingest/wiki/Normalized-Location-Schema
"""

import datetime
import enum
import re
from typing import List, Optional

from pydantic import AnyUrl, EmailStr, Field, HttpUrl, datetime_parse, root_validator

from .common import BaseModel

# Validate zipcode is in 5 digit or 5 digit + 4 digit format
# e.g. 94612, 94612-1234
ZIPCODE_RE = re.compile(r"^[0-9]{5}(?:-[0-9]{4})?$")

# Validate that phone number is a valid US phone number.
# Less strict than spec so normalizers don't need to encode phone numbers exactly
# e.g. (444) 444-4444, +1 (444) 444-4444
US_PHONE_RE = re.compile(
    r"^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(([0-9]{3})\)|([0-9]{3}))\s*(?:[.-]\s*)?)?([0-9]{3})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:\#|x\.?|ext\.?|extension)\s*(\d+))?$"  # noqa: E501
)

# Lowercase alpha-numeric and underscores
# e.g. google_places
ENUM_VALUE_RE = re.compile(r"^[a-z0-9_]+$")

# Lowercase alpha-numeric and underscores with one colon
# e.g. az_arcgis:hsdg46sj
LOCATION_ID_RE = re.compile(r"^[a-z0-9_]+\:[a-zA-Z0-9_-]+$")

# Source ids can have anything but a space or a colon. Those must be replaced with another character (like a dash).
SOURCE_ID_RE = re.compile(r"^[^\s\:]+$")

# Max length for long text fields storing notes
NOTE_MAX_LENGTH = 2046

# Max length for normal string value fields
VALUE_MAX_LENGTH = 256

# Max length for short enum identifier fields
ENUM_MAX_LENGTH = 64

# Max length for id string fields
ID_MAX_LENGTH = 128


class StringDatetime(datetime.datetime):
    @classmethod
    def __get_validators__(cls):
        yield datetime_parse.parse_datetime
        yield cls.validate

    @classmethod
    def validate(cls, v: datetime.datetime) -> str:
        return v.isoformat()


class StringDate(datetime.date):
    @classmethod
    def __get_validators__(cls):
        yield datetime_parse.parse_date
        yield cls.validate

    @classmethod
    def validate(cls, v: datetime.date) -> str:
        return v.isoformat()


class StringTime(datetime.date):
    @classmethod
    def __get_validators__(cls):
        yield datetime_parse.parse_time
        yield cls.validate

    @classmethod
    def validate(cls, v: datetime.time) -> str:
        return v.isoformat("minutes")


@enum.unique
class State(str, enum.Enum):
    ALABAMA = "AL"
    ALASKA = "AK"
    AMERICAN_SAMOA = "AS"
    ARIZONA = "AZ"
    ARKANSAS = "AR"
    CALIFORNIA = "CA"
    COLORADO = "CO"
    CONNECTICUT = "CT"
    DELAWARE = "DE"
    DISTRICT_OF_COLUMBIA = "DC"
    FLORIDA = "FL"
    GEORGIA = "GA"
    GUAM = "GU"
    HAWAII = "HI"
    IDAHO = "ID"
    ILLINOIS = "IL"
    INDIANA = "IN"
    IOWA = "IA"
    KANSAS = "KS"
    KENTUCKY = "KY"
    LOUISIANA = "LA"
    MAINE = "ME"
    MARYLAND = "MD"
    MASSACHUSETTS = "MA"
    MICHIGAN = "MI"
    MINNESOTA = "MN"
    MISSISSIPPI = "MS"
    MISSOURI = "MO"
    MONTANA = "MT"
    NEBRASKA = "NE"
    NEVADA = "NV"
    NEW_HAMPSHIRE = "NH"
    NEW_JERSEY = "NJ"
    NEW_MEXICO = "NM"
    NEW_YORK = "NY"
    NORTH_CAROLINA = "NC"
    NORTH_DAKOTA = "ND"
    NORTHERN_MARIANA_IS = "MP"
    OHIO = "OH"
    OKLAHOMA = "OK"
    OREGON = "OR"
    PENNSYLVANIA = "PA"
    PUERTO_RICO = "PR"
    RHODE_ISLAND = "RI"
    SOUTH_CAROLINA = "SC"
    SOUTH_DAKOTA = "SD"
    TENNESSEE = "TN"
    TEXAS = "TX"
    UTAH = "UT"
    VERMONT = "VT"
    VIRGINIA = "VA"
    VIRGIN_ISLANDS = "VI"
    WASHINGTON = "WA"
    WEST_VIRGINIA = "WV"
    WISCONSIN = "WI"
    WYOMING = "WY"


@enum.unique
class ContactType(str, enum.Enum):
    GENERAL = "general"
    BOOKING = "booking"


@enum.unique
class DayOfWeek(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    PUBLIC_HOLIDAYS = "public_holidays"


@enum.unique
class WheelchairAccessLevel(str, enum.Enum):
    YES = "yes"  # there is wheelchair access not sure about level of service
    FULL = "full"  # here is full wheelchair access
    PARTIAL = "partial"  # there is partial wheelchair access
    NO = "no"  # there is no wheelchair access


class Address(BaseModel):
    """
    {
        "street1": str,
        "street2": str,
        "city": str,
        "state": str as state initial e.g. CA,
        "zip": str,
    },
    """

    street1: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
    street2: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
    city: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
    state: Optional[State]
    zip: Optional[str] = Field(pattern=ZIPCODE_RE.pattern)


class Contact(BaseModel):
    """
    {
        "contact_type": str as contact type enum e.g. booking,
        "phone": str as (###) ###-###,
        "website": str,
        "email": str,
        "other": str,
    }
    """

    contact_type: Optional[ContactType]
    phone: Optional[str] = Field(pattern=US_PHONE_RE.pattern)
    website: Optional[HttpUrl]
    email: Optional[EmailStr]
    other: Optional[str] = Field(max_length=NOTE_MAX_LENGTH)

    @root_validator(skip_on_failure=True)
    @classmethod
    def validate_has_one_value(cls, values: dict) -> dict:
        oneof_fields = ["phone", "website", "email", "other"]
        has_values = [key for key in oneof_fields if values.get(key)]

        if len(has_values) > 1:
            raise ValueError(
                f"Multiple values specified in {', '.join(has_values)}. "
                "Only one value should be specified per Contact entry."
            )

        if not has_values:
            raise ValueError("No values specified for Contact.")

        return values


class OpenDate(BaseModel):
    """
    {
        "opens": str as iso8601 date,
        "closes": str as iso8601 date,
    }
    """

    opens: Optional[StringDate]
    closes: Optional[StringDate]

    @root_validator(skip_on_failure=True)
    @classmethod
    def validate_closes_after_opens(cls, values: dict) -> dict:
        opens = values.get("opens")
        closes = values.get("closes")

        if opens and closes:
            if closes < opens:
                raise ValueError("Closes date must be after opens date")

        return values


class OpenHour(BaseModel):
    """
    {
        "day": str as day of week enum e.g. monday,
        "opens": str as 24h local time formatted as hh:mm,
        "closes": str as 24h local time formatted as hh:mm,
    }
    """

    day: DayOfWeek
    opens: StringTime
    closes: StringTime

    @root_validator(skip_on_failure=True)
    @classmethod
    def validate_closes_after_opens(cls, values: dict) -> dict:
        opens = values.get("opens")
        closes = values.get("closes")

        if opens and closes:
            if closes < opens:
                raise ValueError("Closes time must be after opens time")

        return values


class Availability(BaseModel):
    """
    {
        "drop_in": bool,
        "appointments": bool,
    },
    """

    drop_in: Optional[bool]
    appointments: Optional[bool]


class Access(BaseModel):
    """
    {
        "walk": bool,
        "drive": bool,
        "wheelchair": str,
    }
    """

    walk: Optional[bool]
    drive: Optional[bool]
    wheelchair: Optional[WheelchairAccessLevel]


class Source(BaseModel):
    """
    {
        "source": str as source type enum e.g. vaccinespotter,
        "id": str as source defined id e.g. 7382088,
        "fetched_from_uri": str as uri where data was fetched from,
        "fetched_at": str as iso8601 utc datetime (when scraper ran),
        "published_at": str as iso8601 utc datetime (when source claims it updated),
        "data": {...parsed source data in source schema...},
    }
    """

    source: str = Field(pattern=ENUM_VALUE_RE.pattern, max_length=ENUM_MAX_LENGTH)
    id: str = Field(pattern=SOURCE_ID_RE.pattern, max_length=ID_MAX_LENGTH)
    fetched_from_uri: Optional[AnyUrl]
    fetched_at: Optional[StringDatetime]
    published_at: Optional[StringDatetime]
    data: dict


# TODO: accessibility accomodations as amenities
# "accomodationName": {
#     "description": "name of the accessibility accomodation",
#     "type": "string"
# },
# "accomodationDescription": {
#     "description": "Description of the accomodation",
#     "type": "string"
# },
# "accomodationIcon": {
#     "description": "  icon for the accessibility accomodation",
#     "type": "string"
# }


class Amenity(BaseModel):
    """
    {
        "name": str, name of the amenity,
        "description": str description of the amenity,
        "icon": str as uri of icon provided with amenity,
    }
    """

    name: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
    description: Optional[str]
    icon: Optional[AnyUrl]


class RentCost(BaseModel):
    """
    {
        "notes": str, Any notes about the rent,
        "minCost": int, Minimum average cost of rent in cents per month,
        "maxCost": int, Maximum average cost of rent in cents per month,
    }
    """

    notes: Optional[str]
    minCost: Optional[int]
    maxCost: Optional[int]

    @root_validator(skip_on_failure=True)
    @classmethod
    def validate_max_greaterthan_min(cls, values: dict) -> dict:
        low = values.get("minCost")
        high = values.get("maxCost")

        if low and high:
            if high < low:
                raise ValueError(
                    "Minimum rent cost must be less than maximum rent cost"
                )

        return values


class UtilityCosts(BaseModel):
    """
    {
        "electric": int cost of electric service in cents per month
        "water": int cost of water service in cents per month
        "gas": int cost of gas service in cents per month
        "sewer": int cost of sewer service in cents per month
        "internet": int cost of internet service in cents per month
    }
    """

    electric: Optional[int]
    water: Optional[int]
    gas: Optional[int]
    sewer: Optional[int]
    internet: Optional[int]


class Appliances(BaseModel):
    """
    {
        "washingMachine": bool whether or not there is a washingMachine in the unit,
        "dryer": bool whether or not there is a dryer in the unit,
        "oven": bool whether or not there is a oven (put food inside) in the unit,
        "stove": bool whether or not there is a stove (put food on top) in the unit,
        "ovenAsRange": bool whether the oven and the range are part of the same appliance,
        "dishwasher": bool whether or not there is a dishwasher in the unit,
        "refrigerator": bool whether or not there is a refrigerator in the unit,
        "microwave": bool whether or not there is a microwave in the unit,
    }
    """

    # sink
    # garbageDisposal
    # island

    washingMachine: Optional[bool]
    dryer: Optional[bool]
    oven: Optional[bool]
    stove: Optional[bool]
    ovenAsRange: Optional[bool]
    dishwasher: Optional[bool]
    refrigerator: Optional[bool]
    microwave: Optional[bool]


class UnitType(BaseModel):
    """
    {
        "name": str, name of this unit type/model,
        "id": str as source defined id e.g. 7382088,
        "description": str description of this unit type/model,
        "shared": bool Is this unit shared with roommates?,
        "bedroomCount": int number of bedrooms,
        "bathroomCount": int number of bathrooms,
        "floorplanUrl": str as uri to floorplan document,
        "rent": object as RentCost,
        "appliances": object as Appliances what appliances does this unit have,
        "amenities": list of Amenity consisting of other amenities in the unit,
        "utilitiesCost": object as cost of each utility,
    }
    """

    name: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
    description: Optional[str]
    id: str = Field(pattern=SOURCE_ID_RE.pattern, max_length=ID_MAX_LENGTH)
    shared: Optional[bool]
    bedroomCount: Optional[int]
    bathroomCount: Optional[int]
    floorplanUrl: Optional[AnyUrl]
    rent: Optional[RentCost]
    appliances: Optional[Appliances]
    amenities: Optional[List[Amenity]]
    utilitiesCost: Optional[UtilityCosts]


class NormalizedApartmentComplex(BaseModel):
    id: str = Field(max_length=ID_MAX_LENGTH)
    name: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
    address: Optional[Address]
    onRITCampus: Optional[bool]
    renewable: Optional[bool]

    contact: Optional[List[Contact]]
    # languages: Optional[List[str]]  # [str as ISO 639-1 code]
    opening_dates: Optional[List[OpenDate]]
    opening_hours: Optional[List[OpenHour]]
    availability: Optional[Availability]
    access: Optional[Access]
    links: Optional[List[AnyUrl]]
    description: Optional[str]
    subletPolicy: Optional[str]
    reletPolicy: Optional[str]
    imageUrl: Optional[AnyUrl]
    active: Optional[bool]
    amenities: Optional[List[Amenity]]
    unitTypes: Optional[List[UnitType]]
    source: Source

    @root_validator(skip_on_failure=True)
    @classmethod
    def validate_id_source(cls, values: dict) -> dict:
        loc_id = values.get("id")
        if not loc_id:
            return values

        source = values.get("source")
        if not source:
            return values

        source_name = source.source
        if not source_name:
            return values

        if not loc_id.startswith(f"{source_name}:"):
            raise ValueError("Location ID must be prefixed with source name")

        return values
