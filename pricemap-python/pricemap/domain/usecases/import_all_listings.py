from datetime import datetime
from logging import Logger

import requests

from pricemap import settings
from pricemap.adapters.mappers.listing import ListingMapper
from pricemap.domain.ports.finder.geo_place_finder import GeoPlaceFinder
from pricemap.domain.ports.repository.listing_repository import ListingRepository


class ImportAllListings:
    def __init__(
        self,
        api_url: str,
        listing_repository: ListingRepository,
        geo_place_finder: GeoPlaceFinder,
        logger: Logger,
    ):
        self.api_url = api_url
        self.listing_repository = listing_repository
        self.geo_place_finder = geo_place_finder
        self.logger = logger

    def import_all_listings(self) -> None:
        """Import listings for all places."""
        for place_id in self.geo_place_finder.retrieve_all_places_ids():
            self.logger.debug("Import listings for placeId %s", place_id)
            self._import_listings_for(place_id)

    def _import_listings_for(self, place_id: int) -> None:
        """
        Import all listings for a given place_id.

        That method will call an external API to retrieve data
        while the API returns a 200 status code then bulk persists
        Listings entities into a dedicated table.

        Args:
            - place_id : place id used to call the external API
        """
        current_page = 1
        is_last_page = False
        while not is_last_page:
            response = requests.get(self.api_url % place_id, {"page": current_page})
            if response.status_code != 200:
                if response.status_code != 416:
                    raise Exception(
                        "Listing API returns an unexpected status code",
                        {
                            "status_code": response.status_code,
                            "response": response.text,
                        },
                    )
                break

            json_response = response.json()
            # If we received fewer results than the page limit, we reached the last page
            is_last_page = len(json_response) < settings.LISTING_API_NB_RESULTS_PER_PAGE

            self.logger.info(
                f"Import listings for placeId {place_id} - page {current_page}"
            )

            bulk_listings = []
            for item in json_response:
                listing = ListingMapper.from_dict_to_entity(
                    item, place_id, datetime.now()
                )
                self.logger.debug("Add listing %s to bulk", listing.id)
                bulk_listings.append(listing)

            self.listing_repository.persist(bulk_listings)
            current_page += 1
