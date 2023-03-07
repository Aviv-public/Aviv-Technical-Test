from freezegun import freeze_time

from listingapi.domain import use_cases
from tests import factories


class TestUpdateListing:
    @freeze_time("2023-01-18 08:50:03.761691")
    def test_update_listing(
        self,
        persist_listing_use_case: use_cases.PersistListing,
        update_listing_use_case: use_cases.UpdateListing,
    ) -> None:
        listing_entity = factories.entities.Listing(name="Mikhail Schmiedt")
        persisted_listing = persist_listing_use_case.listing_repository.create(
            listing_entity
        )

        listing_entity.name = "My new name"
        with freeze_time("2023-01-19 08:50:03.761691"):
            updated_listing = update_listing_use_case.perform(
                persisted_listing["id"], listing_entity
            )

        assert updated_listing["name"] == "My new name"
        assert updated_listing["created_date"] == "2023-01-18T08:50:03.761691"
        assert updated_listing["updated_date"] == "2023-01-19T08:50:03.761691"
