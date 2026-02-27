"""Test XML extraction methods for Tyler Tech."""

# flake8: noqa: E501 Line to long

import transforms.client_transforms.tyler_tech_xml as ttx


def test_empty_field():
    """Extract comments and split multi-line comment lines."""
    xml = """
<?xml version="1.0"?>
<BillExtract>
<BillComments>
<BillComment>Please go to FrederickCO.gov/Newsletter to view the Town of Frederick monthly newsletter.</BillComment>
<BillComment></BillComment>
<BillComment>https://www.frederickco.gov/ArchiveCenter/ViewFile/Item/1325</BillComment>
</BillComments>
<Accounts>
<Account>
</Account>
</Accounts>
</BillExtract>
""".strip().split('\n')

    source = ttx.SourceXML(xml, xml_extract={})
    comments = source.comments

    assert len(comments) == 3
    assert not comments[1]


def test_multi_line():
    """Extract comments and split multi-line comment lines."""
    xml = """
<?xml version="1.0"?>
<BillExtract>
<BillComments>
<BillComment>Please go to FrederickCO.gov/Newsletter to view the Town of Frederick monthly newsletter.

https://www.frederickco.gov/ArchiveCenter/ViewFile/Item/1325</BillComment>
</BillComments>
<Accounts>
<Account>
</Account>
</Accounts>
</BillExtract>
""".strip().split('\n')

    source = ttx.SourceXML(xml, xml_extract={})
    comments = source.comments

    assert len(comments) == 3
    assert not comments[1]


def test_embed_multi_line():
    """Extract comments and split multi-line comment lines."""
    xml = """
<?xml version="1.0"?>
<BillExtract>
<BillComments>
<BillComment>Preceeding line</BillComment>
<BillComment>Please go to FrederickCO.gov/Newsletter to view the Town of Frederick monthly newsletter.

https://www.frederickco.gov/ArchiveCenter/ViewFile/Item/1325</BillComment>
<BillComment>Folloeing line.</BillComment>
</BillComments>
<Accounts>
<Account>
</Account>
</Accounts>
</BillExtract>
""".strip().split('\n')

    source = ttx.SourceXML(xml, xml_extract={})
    comments = source.comments

    assert len(comments) == 5
    assert not comments[2]
