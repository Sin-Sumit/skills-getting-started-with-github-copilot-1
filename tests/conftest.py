import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(scope="function")
def activities_reset():
    """Reset the in-memory `activities` dict before/after each test.

    Saves a deep copy, yields to the test, then restores the saved state.
    """
    saved = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(saved)
