from pathlib import Path
from edgar.forms.secdoc import Document


def test_form3():
    # input data
    file = Path("form3.txt")

    # tested unit
    doc = Document(file1)

    # assertion
    print(doc.accession_num)
    print(doc.accession_num == '0000011544-20-000013')


def test_file4():
    # input data
    file = Path("form4.txt")

    # tested unit
    doc = Document(file)

    # assertion
    # ADD CODE HERE


def test_file5():
    # ADD CODE HERE
