import logging
from datetime import datetime

import pandas as pd

from src.api import spl


def filter_items(deed, df, param):
    if deed[param]:
        # return matching values
        return df.loc[(df[param] == deed[param])]
    else:
        # return value either None or ""
        return df[(df[param].isnull()) | (df[param] == "")]


def get_deeds_value(account_name):
    collection = spl.get_deeds_collection(account_name)
    market_df = pd.DataFrame(spl.get_deeds_market())
    deeds_price_found = 0
    deeds_owned = 0
    deeds_total = 0.0
    for deed in collection:
        deeds_owned += 1
        filter_types = ["rarity", 'plot_status', 'magic_type', 'deed_type']
        df = market_df
        missing_types = []
        for filter_type in filter_types:
            temp = filter_items(deed, df, filter_type)
            if not temp.empty:
                df = temp
            else:
                missing_types.append(filter_type)
        if missing_types:
            logging.warning("Not a perfect match found missing filters: " + str(missing_types))
            logging.warning("Was looking for: \n" +
                            "\n".join([str(x) + ": " + str(deed[x]) for x in filter_types]))
            logging.warning("Current estimated best value now: " +
                            str(df.astype({'listing_price': 'float'}).listing_price.min()))
        listing_price = df.astype({'listing_price': 'float'}).listing_price.min()
        deeds_price_found += 1

        deeds_total += listing_price

    return pd.DataFrame({'date': datetime.today().strftime('%Y-%m-%d'),
                         'account_name': account_name,
                         'deeds_qty': deeds_owned,
                         'deeds_price_found_qty': deeds_price_found,
                         'deeds_value': deeds_total}, index=[0])
