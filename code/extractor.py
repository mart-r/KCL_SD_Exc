#!/usr/bin/env python3
"""
KCL Software Developmetn Interview exercise.

Please write a function in Python to extract specific medication codes and associated medication
dosages from a text document. Your function should accept a string as input, and should output a
list of medication items, where each item is a sublist consisting of (1) the medication code, as an
integer, and (2) the dosage, as a string.
"""


from typing import Dict, List, Tuple


DEFINED_MEDICINES = {"paracetamol": 1,
                     "panadol": 1, "aspirin": 2, "penicillin": 3}
"""The predefined medicines.
The medicine name (in lower case) mapped to the medicine ID (intger).

If two different medicines map to the same ID they are assumed to use
the same the same active component and are thus considered identical"""


def extract_from_file_contents(contents: str, medicines: Dict[str, int] = DEFINED_MEDICINES) -> List[Tuple[int, str]]:
    """Extract the medicine id and dosage information from an input file contents.

    The medicine names to their IDs can be specifeid.

    The contents is expected to have any number of medications.
    Each line contains medications with dosage.
    Contents after an empty (or whitespace) line are ignored.
    Unknown medicine names are ignored.

    Args:
        contents (str): The contents of the file (including new lines \n)
        medicines (Dict[str, int], optional): The mapping of medicine names to their IDs. Defaults to DEFINED_MEDICINES.

    Returns:
        List[Tuple[int, str]]: The list of medicine IDs and dosages
    """
    extracted_medicines = []
    for line in contents.split('\n'):
        if not line_has_medicine(line):
            break
        medicine_id, dosage = get_medicine_and_dosage(line, medicines)
        if medicine_id is None or dosage is None:
            continue
        extracted_medicines.append([medicine_id, dosage])
    return extracted_medicines


def line_has_medicine(line: str) -> bool:
    """Check if the line describes a medicine and dosage.

    An empty line or a line with only whitespace does not define a medicine.
    All other lines are assumed to describe a medicine.

    Args:
        line (str): The line in question

    Returns:
        bool: Whether or not the line describes a medicine
    """
    if len(line) == 0:
        return False
    if len(line.strip()) == 0:
        return False
    return True


def get_medicine_and_dosage(line: str, medicines: Dict[str, int], allow_empty_dosage: bool = True, verbose: bool = False) -> Tuple[int, str]:
    """Get the medicine and dosage from a line.

    The medicines mapping needs to be specified. 

    Args:
        line (str): The line in question
        medicines (Dict[str, int]): The mapping of medicine names to their IDs
        allow_empty_dosage (bool, optional): Whether to allow empty dosage. Defaults to True.
        verbose (bool, optional): Whether to generate verbose output. Defaults to False.

    Returns:
        Tuple[int, str]: A tuple of the ID and the dosage or (None, None) if the medicine is unknown
    """
    parts = line.split(' ', maxsplit=1)
    if len(parts) == 1:
        if not allow_empty_dosage:
            if verbose:
                print('Unable to identify medicine and dosage from line: ', line)
            return None, None
        parts.append('')
    medicine_name, dosage = parts
    medicine_name = medicine_name.lower()
    if medicine_name in medicines:
        return medicines[medicine_name], dosage.strip()
    if verbose:
        print('Unknown medicine:', medicine_name)
    return None, None


def extract_medicines_from_file(file_name: str, medicines: Dict[str, int] = DEFINED_MEDICINES) -> List[Tuple[int, str]]:
    """Extract medicines from a file.

    This method extract the contents from the file and uses the
    :func:`~extractor.extract_from_file_contents` method for to extract the medicines.
    See :func:`~extractor.extract_from_file_contents` for further details.

    Args:
        file_name (str): The file name to read the contents from
        medicines (Dict[str, int], optional): The mapping of medicine names to their IDs. Defaults to DEFINED_MEDICINES.

    Returns:
        List[Tuple[int, str]]: The list of medicine IDs and dosages
    """
    with open(file_name) as f:
        contents = f.read()
        f.close()
    return extract_from_file_contents(contents, medicines=medicines)


def extract_and_print_defaults_from_file(file_name: str) -> None:
    """Extract and print pre-defined (default) medicines from file.

    Args:
        file_name (str): File to extraf medicines from
    """
    medicines = extract_medicines_from_file(file_name)
    print(medicines)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 1:
        print('Need to specify a file name')
        sys.exit(0)
    for fn in sys.argv[1:]:
        print('Extracting from', fn)
        extract_and_print_defaults_from_file(fn)
