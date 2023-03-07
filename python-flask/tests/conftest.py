from typing import Iterator

import factory
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

from listingapi import adapters
from listingapi.domain import ports, use_cases


@pytest.fixture(scope="session")
def db_session() -> scoped_session:
    in_memory_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    _session_factory = sessionmaker(
        autocommit=False, autoflush=True, bind=in_memory_engine
    )
    db_session: scoped_session = scoped_session(_session_factory)
    return db_session


@pytest.fixture(scope="session")
def listing_repository(db_session: scoped_session) -> ports.ListingRepository:
    listing_repository = adapters.SqlAlchemyListingRepository(db_session)
    listing_repository.init()
    return listing_repository


@pytest.fixture(scope="session")
def persist_listing_use_case(
    listing_repository: ports.ListingRepository,
) -> use_cases.PersistListing:
    return use_cases.PersistListing(listing_repository)


@pytest.fixture(scope="session")
def update_listing_use_case(
    listing_repository: ports.ListingRepository,
) -> use_cases.UpdateListing:
    return use_cases.UpdateListing(listing_repository)


@pytest.fixture(scope="session", autouse=True)
def fix_faker_local() -> Iterator:
    with factory.Faker.override_default_locale("fr_FR"):
        yield
