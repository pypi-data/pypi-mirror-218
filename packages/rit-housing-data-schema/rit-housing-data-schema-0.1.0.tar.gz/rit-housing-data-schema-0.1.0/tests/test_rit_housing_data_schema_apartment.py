import enum
import json

import pydantic.error_wrappers
import pytest

from rit_housing_data_schema import apartment

from .common import collect_existing_subclasses


def test_has_expected_schema():
    expected = {
        "BaseModel",
        "Address",
        "Amenity",
        "Contact",
        "OpenDate",
        "OpenHour",
        "Availability",
        "UnitType",
        "Access",
        "Appliances",
        "Source",
        "RentCost",
        "UtilityCosts",
        "NormalizedApartmentComplex",
    }

    existing = collect_existing_subclasses(apartment, pydantic.BaseModel)

    missing = expected - existing
    assert not missing, "Expected pydantic schemas are missing"

    extra = existing - expected
    assert not extra, "Extra pydantic schemas found. Update this test."


def test_has_expected_enums():
    expected = {
        "State",
        "ContactType",
        "DayOfWeek",
        "WheelchairAccessLevel",
    }

    existing = collect_existing_subclasses(apartment, enum.Enum)

    missing = expected - existing
    assert not missing, "Expected enums are missing"

    extra = existing - expected
    assert not extra, "Extra enum found. Update this test."


def test_opening_days():
    assert apartment.OpenDate(
        opens="2021-04-01",
        closes="2021-04-01",
    )

    assert apartment.OpenDate(opens="2021-04-01")

    assert apartment.OpenDate(
        closes="2021-04-01",
    )

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.OpenDate(
            closes="2021-04-01T04:04:04",
        )

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.OpenDate(
            opens="tomorrow",
        )

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.OpenDate(
            opens="2021-06-01",
            closes="2021-01-01",
        )


def test_opening_hours():
    assert apartment.OpenHour(
        day="monday",
        opens="08:00",
        closes="14:00",
    )

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.OpenHour(day="monday", opens="8h", closes="14:00")

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.OpenHour(
            day="mon",
            opens="08:00",
            closes="14:00",
        )

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.OpenHour(
            day="monday",
            opens="20:00",
            closes="06:00",
        )

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.OpenHour(
            day="monday",
            opens="2021-01-01T08:00:00",
            closes="14:00",
        )


def test_valid_contact():
    assert apartment.Contact(
        contact_type=apartment.ContactType.BOOKING,
        email="vaccine@example.com",
    )
    assert apartment.Contact(website="https://example.com")
    assert apartment.Contact(phone="(510) 555-5555")


def test_raises_on_invalid_contact():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.Contact(contact_type=apartment.ContactType.GENERAL)

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.Contact(contact_type="invalid", email="vaccine@example.com")

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.Contact(email="vaccine@example.com", website="https://example.com")


def test_raises_on_invalid_location():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.NormalizedApartmentComplex()

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.NormalizedApartmentComplex(
            id="source:id",
            contact=apartment.Contact(phone="444-444"),
            source=apartment.Source(
                source="source",
                id="id",
                data={"id": "id"},
            ),
        )

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.NormalizedApartmentComplex(
            id="invalid:id",
            source=apartment.Source(
                source="source",
                id="id",
                data={"id": "id"},
            ),
        )

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        apartment.NormalizedApartmentComplex(
            id="source:" + "a" * 200,
            source=apartment.Source(
                source="source",
                id="id",
                data={"id": "id"},
            ),
        )


def test_valid_location():
    # Minimal record
    assert apartment.NormalizedApartmentComplex(
        id="source:id",
        source=apartment.Source(
            source="source",
            id="id",
            data={"id": "id"},
        ),
    )

    # Full record with str enums
    full_loc = apartment.NormalizedApartmentComplex(
        id="source:id",
        name="name",
        address=apartment.Address(
            street1="1991 Mountain Boulevard",
            street2="#1",
            city="Oakland",
            state="CA",
            zip="94611",
        ),
        contact=[
            apartment.Contact(
                contact_type="booking",
                phone="(916) 445-2841",
            )
        ],
        opening_dates=[
            apartment.OpenDate(
                opens="2021-04-01",
                closes="2021-04-01",
            ),
        ],
        opening_hours=[
            apartment.OpenHour(
                day="monday",
                opens="08:00",
                closes="14:00",
            ),
        ],
        availability=apartment.Availability(
            drop_in=False,
            appointments=True,
        ),
        access=apartment.Access(
            walk=True,
            drive=False,
            wheelchair="partial",
        ),
        links=["https://www.google.com"],
        active=True,
        source=apartment.Source(
            source="source",
            id="id",
            fetched_from_uri="https://example.org",
            fetched_at="2020-04-04T04:04:04.4444",
            published_at="2020-04-04T04:04:04.4444",
            data={"id": "id"},
        ),
        onRITCampus=False,
        renewable=False,
        description="description",
        subletPolicy="no",
        reletPolicy="no",
        imageUrl="https://4.bp.blogspot.com/-2llfvEbN9O8/T8zrEtTLkCI/AAAAAAAAMyc/zP4uPLwaQss/s1600/these-funny-cats-001-031.jpg",
        amenities=[apartment.Amenity(name="warm", description="it doesnt freeze")],
        unitTypes=[
            apartment.UnitType(
                name="1bed",
                description="1 bedroom apt",
                id="01-01",
                shared=False,
                bedroomCount=1,
                bathroomCount=1,
                floorplanUrl="https://4.bp.blogspot.com/-2llfvEbN9O8/T8zrEtTLkCI/AAAAAAAAMyc/zP4uPLwaQss/s1600/these-funny-cats-001-031.jpg",
                rent=apartment.RentCost(minCost=899, maxCost=999, notes="pay us"),
                appliances=apartment.Appliances(
                    washingMachine=False,
                    dryer=False,
                    oven=False,
                    stove=False,
                    ovenAsRange=False,
                    dishwasher=False,
                    refrigerator=False,
                    microwave=False,
                ),
                amenities=[apartment.Amenity(name="AC", description="it barely works")],
                utilitiesCost=apartment.UtilityCosts(
                    electric=90,
                    water=90,
                    gas=90,
                    sewer=90,
                    internet=90,
                ),
            )
        ],
    )
    assert full_loc

    # Verify dict serde
    full_loc_dict = full_loc.dict()
    assert full_loc_dict

    parsed_full_loc = apartment.NormalizedApartmentComplex.parse_obj(full_loc_dict)
    assert parsed_full_loc

    assert parsed_full_loc == full_loc

    # Verify json serde
    full_loc_json = full_loc.json()
    assert full_loc_json

    parsed_full_loc = apartment.NormalizedApartmentComplex.parse_raw(full_loc_json)
    assert parsed_full_loc

    assert parsed_full_loc == full_loc

    # Verify dict->json serde
    full_loc_json_dumps = json.dumps(full_loc_dict)
    assert full_loc_json_dumps

    assert full_loc_json_dumps == full_loc_json

    parsed_full_loc = apartment.NormalizedApartmentComplex.parse_raw(
        full_loc_json_dumps
    )
    assert parsed_full_loc

    assert parsed_full_loc == full_loc
