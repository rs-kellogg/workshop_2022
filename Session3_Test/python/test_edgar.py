from pathlib import Path
from edgar.forms.secdoc import Document


def test_form3():
    """
    Test Form 3
    :return:
    """
    # input data
    file = Path("form3.txt")

    # tested unit
    doc = Document(file1)

    # assertion
    print(doc.accession_num)
    print(doc.accession_num == '0000011544-20-000013')


def test_file4():
    """
    Test Form4
    :return:
    """
    # ADD CODE HERE


def test_file5():
    """
    Test Form5
    :return:
    """
    # ADD CODE HERE
