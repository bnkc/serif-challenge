from setuptools import setup, find_packages  # type: ignore
import os
from setuptools.command.install import install  # type: ignore
import urllib.request


class PostInstallCommand(install):
    """Post-installation"""

    def run(self):
        install.run(self)
        self.download_file()

    def download_file(self):
        url = "https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2024-06-01_anthem_index.json.gz"
        download_path = "downloads/2024-06-01_anthem_index.json.gz"
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        print(f"Downloading file from {url} to {download_path}")
        urllib.request.urlretrieve(url, download_path)
        print(f"Downloaded file to {download_path}")


setup(
    name="serif",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "ijson",
        "pydantic",
    ],
    cmdclass={
        "install": PostInstallCommand,
    },
)
