from pathlib import Path
from edgar.forms.secdoc import Document


def test_file1():
    # input data
    file1 = Path("./data/11544_1_0000011544-20-000013.txt")

    # tested unit
    doc = Document(file1)

    # assertion
    assert doc.accession_num == '0000011544-20-000013'


def test_file2():
    # input data
    file2 = Path("./data/37996_4_0001209191-20-054135.txt")

    # tested unit
    doc = Document(file2)

    # assertion
    assert False


def test_file3():
    # input data
    file3 = Path("./data/0001012975-17-000759.txt")

    # tested unit
    doc = Document(file3)

    # assertion
    assert False