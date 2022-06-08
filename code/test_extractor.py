#!/usr/bin/env python3

from extractor import line_has_medicine, get_medicine_and_dosage, extract_from_file_contents, extract_medicines_from_file, DEFINED_MEDICINES

import pytest


@pytest.mark.parametrize("line, expected", [
    ["some Simple line", True], ["One SpaceLine", True], ["NoSpaceLine", True],
    ["", False], [" ", False], ["   ", False]
])
def test_line_has_medicine_with(line, expected):
    got = line_has_medicine(line)
    assert got == expected


@pytest.mark.parametrize("line, exp_med, exp_dose", [
    # existing medicines
    ["Aspirin 75mg daily", 2, "75mg daily"], ["ASPIRIN 75mg a minute", 2, "75mg a minute"],
    ["PANADOL 1000mg WHEN NEEDED MAX FOUR TIMES DAILY", 1, "1000mg WHEN NEEDED MAX FOUR TIMES DAILY"],
    # non-existing "medicines"
    ["some Simple line", None, None], ["One SpaceLine",
                                       None, None], ["NoSpaceLine", None, None],
    # no defined medicine
    ["", None, None], [" ", None, None], ["   ", None, None]
])
def test_get_medicine_and_dosage_with(line, exp_med, exp_dose):
    med, dose = get_medicine_and_dosage(line, DEFINED_MEDICINES)
    assert med == exp_med
    assert dose == exp_dose

@pytest.mark.parametrize("contents, expected", [["""Aspirin 75mg daily
PANADOL 1000mg WHEN NEEDED MAX FOUR TIMES DAILY""", [[2, "75mg daily"], [1, "1000mg WHEN NEEDED MAX FOUR TIMES DAILY"]]]])
def test_extract_from_file_contents_with(contents, expected):
    got = extract_from_file_contents(contents)
    assert len(got) == len(expected)
    assert got == expected


@pytest.mark.parametrize("file_name, expected_output", [
    ["data/input1.data", [[2, '75mg daily'], [1,
                                              '1000mg WHEN NEEDED MAX FOUR TIMES DAILY'], [3, '500mg daily'], [1, '']]],
    ["data/input2.data", [[2, '75mg daily'],
                          [1, '1000mg WHEN NEEDED MAX FOUR TIMES DAILY']]],
    ["data/input3.data", [[2, '75mg daily'],
                          [1, '1000mg WHEN NEEDED MAX FOUR TIMES daily']]],
])
def test_extraction_from_file(file_name, expected_output):
    extracted = extract_medicines_from_file(file_name)
    assert len(extracted) == len(expected_output)
    assert all([e1 == e2 for e1, e2 in zip(extracted, expected_output)])
    assert extracted == expected_output
