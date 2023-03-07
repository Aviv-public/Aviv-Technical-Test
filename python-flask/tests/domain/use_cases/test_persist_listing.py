import pytest
from freezegun import freeze_time

from listingapi.domain import entities, use_cases
from tests import factories


class TestPersistListing:
    @pytest.fixture
    def listing_entity(self) -> entities.ListingEntity:
        listing_entity = factories.entities.Listing(
            bedrooms_count=2,
            building_type="APARTMENT",
            contact_phone_number="",
            description="description",
            latest_price_eur=720000,
            name="Mikhail Schmiedt",
            postal_address=factories.entities.PostalAddress(
                city="Berchtesgaden",
                country="DE",
                postal_code="21810",
                street_address="Johan-Ernst-Ring 7",
            ),
            rooms_count=6,
            surface_area_m2=167,
        )

        return listing_entity

    @freeze_time("2023-01-18 08:50:03.761691")
    def test_persist_listing(
        self,
        persist_listing_use_case: use_cases.PersistListing,
        listing_entity: entities.ListingEntity,
    ) -> None:
        persisted_listing_dict = persist_listing_use_case.listing_repository.create(
            listing_entity
        )

        assert persisted_listing_dict["id"] == 1
        assert persisted_listing_dict["name"] == "Mikhail Schmiedt"
        assert persisted_listing_dict["postal_address"] == {
            "street_address": "Johan-Ernst-Ring 7",
            "postal_code": "21810",
            "city": "Berchtesgaden",
            "country": "DE",
        }
        assert persisted_listing_dict["description"] == "description"
        assert persisted_listing_dict["building_type"] == "APARTMENT"
        assert persisted_listing_dict["latest_price_eur"] == 720000.0
        assert persisted_listing_dict["surface_area_m2"] == 167
        assert persisted_listing_dict["rooms_count"] == 6
        assert persisted_listing_dict["bedrooms_count"] == 2
        assert persisted_listing_dict["contact_phone_number"] == ""
        assert persisted_listing_dict["created_date"] == "2023-01-18T08:50:03.761691"
        assert persisted_listing_dict["updated_date"] == "2023-01-18T08:50:03.761691"
