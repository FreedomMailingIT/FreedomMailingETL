"""
Read 'Tyler Tech Software' XML file to conversion to CSV.

Tyler Tech absolutely inflexible on XML output.  Using module
approach in case future citites change to Tyler Tech.
"""

import xml.etree.ElementTree as et  # noqa
from io import StringIO


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
CONS_KEY = 'Cons_hist'


class SourceXML:
    """Handle reading source XML."""

    def __init__(  # pylint: disable=too-many-arguments
                self,
                source_text,
                xml_extract,  # fields to be extracted
                active_only=False,
                delinqent_accts=False,
                zero_balance=False,
                root='Accounts/Account'
                ):
        """Init source XML text."""
        self.xml_extract = xml_extract
        self.active_only = active_only
        self.delinqent_accts = delinqent_accts
        self.zero_balance = zero_balance
        self.root = root
        self.cons_hist = []
        self.csv_cols = {}
        self.bills = et.ElementTree(
            file=StringIO('\n'.join(source_text))).getroot()
        self.comments = self.get_global_comments()
        self.accounts = et.ElementTree(
            file=StringIO('\n'.join(source_text))).findall(root)

    def _pack_data(self, csv_col, attrib_req, data):
        if csv_col.endswith('?'):
            # possible multi value (like multi meter reads)
            try:
                # add to list of values
                self.csv_cols[csv_col].append(data)
            except KeyError:
                # no values yet so start list
                self.csv_cols[csv_col] = [data]
        elif attrib_req == 'No':  # don't strip account number
            self.csv_cols[csv_col] = data
        else:
            self.csv_cols[csv_col] = data.strip()

    def extract_data(self, element):
        """Extract required data from element attributes."""
        if element.tag == 'Year':
            # get consumption history (multi year & perhaps multi meter)
            for month in months:
                self.cons_hist.insert(0, element.attrib[month])
        else:
            attribs = element.attrib
            for attrib_req, csv_col in self.xml_extract.items():
                if attrib_req in attribs:
                    self._pack_data(
                        csv_col, attrib_req, element.attrib[attrib_req])
                elif attrib_req in element.tag:
                    # extract non-attribute data
                    self._pack_data(csv_col, attrib_req, element.text)

    def get_children(self, parent):
        """Recursive traversal of XML tree."""
        for child in parent:
            self.extract_data(child)
            self.get_children(child)

    def get_global_comments(self):
        """Extract file comments and separate multi-line comments."""
        tmp = [comment.text or '' for comment
               in self.bills.findall('BillComments/BillComment')]
        comments = []
        for message in tmp:
            comments.extend(iter(message.split('\n')))
        return comments

    def traverse_xml(self):
        """Traverse XML source extracting data."""
        for account in self.accounts:
            active_codes = ['Active', 'New', 'Disconnect', 'Suspend']
            if self.delinqent_accts:
                active_codes.append('Disconnect')
            if self.active_only and account.attrib.get('Status') not in active_codes:
                print('Not converted: ',
                      account.attrib.get('No'),
                      account.attrib.get('Status'))
                continue
            self.cons_hist = []
            self.csv_cols = {}
            self.extract_data(account)  # first element before children
            self.get_children(account)

            # for bills only - skip zero balance accts, if requested
            if 'Drft_dt' in self.xml_extract \
                    and not self.zero_balance \
                    and self.csv_cols.get(self.xml_extract['Due'])\
                    .lstrip('0') == '.00':
                continue

            if 'Accounts' in self.root:
                self.csv_cols[CONS_KEY] = self.cons_hist
            yield self.csv_cols
