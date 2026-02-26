"""
Test algorithm to get valid history periods.

Taken from the Account class in hlp_account.py
"""


from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class Self:
    """..."""
    b_date: str = None
    valid_pers: list[int] = None


def get_valid_periods(self):
    """Get valid periods because source data has old history sometimes."""
    # todo: this looks messy - clean it up?
    mths_nml = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    mths_rev = list(reversed(mths_nml))  # because that's the way the data comes
    curr_year = int(self.b_date[-4:])
    prior_year = curr_year - 1

    curr_mth = mths_nml[int(self.b_date[:2]) - 1]
    mth_ptr = mths_rev.index(curr_mth)
    mth_lbl = mths_rev[mth_ptr:] + mths_rev[:mth_ptr+1]

    # valid use periods curr yr months until Dec then prior yr months
    yr, py, valid_pers = str(curr_year), str(prior_year), []
    yr_chg_ptr = len(mth_lbl)-mth_ptr-1
    for ptr, month in enumerate(mth_lbl):
        yr = py if ptr >= yr_chg_ptr else yr
        valid_pers.append(f'{yr}{mths_nml.index(month)+1:02}')
    self.valid_pers = valid_pers

    return self.valid_pers


if __name__ == "__main__":
    test_file = Path("data/archive/valid_periods.json")
    with open(test_file , 'r', encoding='utf8') as jfile:
        test_data = json.load(jfile)
        for idx, (date, expected) in enumerate(test_data.items()):
            assert get_valid_periods(Self(date)) == expected
            print(f'Passed test {idx+1} for {date}')
