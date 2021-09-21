import os
import tempfile

import pytest

from NFTMe.__init__ import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
