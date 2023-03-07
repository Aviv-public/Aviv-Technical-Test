import logging

import factory

from tests import factories

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    with factory.Faker.override_default_locale("fr_FR"):
        listings = factories.entities.Listing.create_batch(10)

    for listing in listings:
        print(listing.json(ensure_ascii=False, indent="\t"))

    logger.info("done")
