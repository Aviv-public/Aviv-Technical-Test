from factory import Factory, Faker

from listingapi.domain import entities


class PostalAddress(Factory):
    class Meta:
        model = entities.PostalAddressEntity

    street_address = Faker("street_address")
    postal_code = Faker("postcode")
    city = Faker("city")
    country = Faker("current_country_code")
