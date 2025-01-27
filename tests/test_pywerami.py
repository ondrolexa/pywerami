#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pywerami
----------------------------------

Tests for `pywerami` module.
"""

from pywerami.api import GridData


def test_read_grid():
    GridData.from_tab("./pywerami/samples/luca3_1.tab", degrees=False)
    assert True, "Data reading error"
