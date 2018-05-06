"""
Test data fetching routines.
"""
import os
import warnings
from requests.exceptions import HTTPError

import pytest

from ..datasets.download import fetch_data


def compare_tiny_data(datapath):
    """
    Check if the file exists and compare its content with what we know it
    should be.
    """
    assert os.path.exists(datapath)
    with open(datapath) as datafile:
        content = datafile.read()
    true_content = "\n".join([
        '# A tiny data file for test purposes only',
        '1  2  3  4  5  6'])
    assert content.strip() == true_content


# Has to go first in order to guarantee that the file has been downloaded
def test_fetch_data_from_remote():
    "Download data from Github to the data directory"
    with warnings.catch_warnings(record=True) as warn:
        datapath = fetch_data('tiny-data.txt', force_download=True)
        assert len(warn) == 1
        assert issubclass(warn[-1].category, UserWarning)
        assert str(warn[-1].message).split()[0] == "Downloading"
    compare_tiny_data(datapath)


def test_fetch_data():
    "Make sure the file exists when not being downloaded"
    with warnings.catch_warnings(record=True) as warn:
        datapath = fetch_data('tiny-data.txt')
        assert not warn
    compare_tiny_data(datapath)


def test_fetch_data_from_store_remote_fail():
    "Should raise an exception if the remote 404s"
    with warnings.catch_warnings(record=True) as warn:
        with pytest.raises(HTTPError):
            fetch_data('invalid remote file name')
        assert len(warn) == 1
        assert issubclass(warn[-1].category, UserWarning)
        assert str(warn[-1].message).split()[0] == "Downloading"