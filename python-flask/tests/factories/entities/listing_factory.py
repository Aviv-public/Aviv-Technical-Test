from factory import Factory, Faker, SelfAttribute, SubFactory

from .postal_address_factory import PostalAddress

from listingapi.domain import entities


class Listing(Factory):
    class Meta:
        model = entities.ListingEntity

    bedrooms_count = Faker("random_int", min=1, max=SelfAttribute("..rooms_count"))
    building_type = Faker("random_element", elements=["STUDIO", "APARTMENT", "HOUSE"])
    contact_phone_number = Faker("phone_number")
    description = Faker("text")
    latest_price_eur = Faker("pyfloat", min_value=100_000, max_value=2_000_000)
    name = Faker("name")
    postal_address = SubFactory(PostalAddress)
    rooms_count = Faker("random_int", min=1, max=8)
    surface_area_m2 = Faker("random_int", min=10, max=500)
