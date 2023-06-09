import logging
import os

import pandas as pd

from src.api import spl
from src.configuration import store, config


def update_season_end_dates():
    if store.season_end_dates.empty:
        from_season_id = 1
    else:
        from_season_id = store.season_end_dates.id.max() + 1

    till_season_id = spl.get_current_season()['id']
    # logging.info("Update season end dates for '" + str(till_season_id) + "' seasons")
    for season_id in range(from_season_id, till_season_id + 1):
        logging.info("Update season end date for season: " + str(season_id))

        store.season_end_dates = pd.concat([store.season_end_dates,
                                            spl.get_season_end_time(season_id)],
                                           ignore_index=True)
    save_stores()


def get_store_names():
    stores_arr = []
    for store_name, _store in store.__dict__.items():
        if isinstance(_store, pd.DataFrame):
            stores_arr.append(store_name)
    return stores_arr


def get_store_file(name):
    return os.path.join(config.store_dir, str(name + config.file_extension))


def load_stores():
    for store_name in get_store_names():
        store_file = get_store_file(store_name)
        if os.path.isfile(store_file):
            store.__dict__[store_name] = pd.read_csv(store_file, index_col=0)


def save_stores():
    for store_name in get_store_names():
        store_file = get_store_file(store_name)
        store.__dict__[store_name].sort_index().to_csv(store_file)


def get_account_names():
    if store.accounts.empty:
        return list()
    else:
        return store.accounts.account_name.tolist()


def get_first_account_name():
    if store.accounts.empty:
        return ""
    else:
        return store.accounts.values[0][0]


def add_account(account_name):
    new_account = pd.DataFrame({'account_name': account_name}, index=[0])
    if store.accounts.empty:
        store.accounts = pd.concat([store.accounts, new_account], ignore_index=True)
    else:
        if store.accounts.loc[(store.accounts.account_name == account_name)].empty:
            store.accounts = pd.concat([store.accounts, new_account], ignore_index=True)
    save_stores()
    return store.accounts.account_name.tolist()


def remove_account_from_store(store_name, search_column, account_name):
    _store = store.__dict__[store_name]
    if search_column in _store.columns.tolist():
        rows = _store.loc[(_store[search_column] == account_name)]
        if not rows.empty:
            _store = _store.drop(rows.index)
    return _store


def remove_data(account_name):
    for store_name in get_store_names():
        store.__dict__[store_name] = remove_account_from_store(store_name, 'account_name', account_name)
        store.__dict__[store_name] = remove_account_from_store(store_name, 'account', account_name)
        store.__dict__[store_name] = remove_account_from_store(store_name, 'player', account_name)

    save_stores()


def remove_account(account_name):
    if store.accounts.empty:
        return list()
    else:
        account_row = store.accounts.loc[(store.accounts.account_name == account_name)]
        if not account_row.empty:
            remove_data(account_name)

    return store.accounts.account_name.tolist()


def get_last_portfolio_selection():
    if store.portfolio.empty or store.view_portfolio_accounts.empty:
        return list()
    else:
        # Remove users that are no longer in
        curr_users = store.portfolio.account_name.unique().tolist()
        mask = (store.view_portfolio_accounts.account_name.isin(curr_users))
        return store.view_portfolio_accounts.loc[mask].account_name.tolist()


def get_seasons_played_list():
    input_df = store.battle_big.copy()
    if not input_df.empty:
        first_date = pd.to_datetime(input_df.created_date).min()

        temp_end_dates = store.season_end_dates.copy()
        temp_end_dates.end_date = pd.to_datetime(temp_end_dates.end_date)

        last_id = temp_end_dates.loc[(temp_end_dates.end_date > first_date)].id.min()
        return temp_end_dates.sort_values('id', ascending=False).loc[(temp_end_dates.id >= last_id-1)].id.to_list()
    else:
        return list()


def get_rule_sets_list():
    rule_sets = config.settings['battles']['rulesets']
    list_of_ruleset = []
    for rule_set in rule_sets:
        list_of_ruleset.append(rule_set['name'])
    return list(list_of_ruleset)


def get_last_season_values(df, users, season_id_column='season_id'):
    return df.loc[(df.player.isin(users)) & (df[season_id_column] == df[season_id_column].max())].copy()
