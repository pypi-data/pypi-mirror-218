import pytest
from snowflake_utilities.utils import check_resource_viable


@pytest.fixture
def incorrect_resource_type():
    """example incorrect resource type"""
    return "oogaboooga"


@pytest.fixture
def correct_resource_type():
    """example correct resource type"""
    return "WAREHOUSES"


class TestCheckResourceViable:
    """Testing class to test the flatten function."""

    def test_error_is_raised(self, incorrect_resource_type):
        """Check if the function throws an error if the input is not allowed."""
        with pytest.raises(ValueError):
            check_resource_viable(resource_type=incorrect_resource_type)

    def test_no_error_is_raised(self, correct_resource_type):
        """Check if the function doesn't throw an error if the input is allowed."""
        check_resource_viable(resource_type=correct_resource_type)
