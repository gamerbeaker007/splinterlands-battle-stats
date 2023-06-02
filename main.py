from src.pages import navigation_page
from src.pages.main_dash import app
from src.utils import store_util

store_util.load_stores()
store_util.update_season_end_dates()


def main():
    # balances_info.get_balances()
    # collection_store.update_collection()
    # battle_store.process_battles()
    #
    # store_util.save_stores()
    # portfolio.update_portfolios()

    app.layout = navigation_page.layout
    app.run_server(debug=True)


if __name__ == '__main__':
    main()
