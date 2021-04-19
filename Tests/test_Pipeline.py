from FootyStats.spiders import FootywireSpider
from pipelines import FootystatsPipeline
import pytest


@pytest.fixture
def FwS():
    return FootywireSpider()