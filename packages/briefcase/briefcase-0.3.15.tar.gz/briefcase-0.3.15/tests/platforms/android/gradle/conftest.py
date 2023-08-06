import pytest

from ....utils import create_file


@pytest.fixture
def first_app_generated(first_app_config, tmp_path):
    # Create the briefcase.toml file
    create_file(
        tmp_path
        / "base_path"
        / "build"
        / "first-app"
        / "android"
        / "gradle"
        / "briefcase.toml",
        """
[paths]
app_packages_path="app_packages"
support_path="support"
metadata_resource_path="res/briefcase.xml"
""",
    )

    create_file(
        tmp_path
        / "base_path"
        / "build"
        / "first-app"
        / "android"
        / "gradle"
        / "res"
        / "briefcase.xml",
        """<resources></resources>""",
    )
    return first_app_config
