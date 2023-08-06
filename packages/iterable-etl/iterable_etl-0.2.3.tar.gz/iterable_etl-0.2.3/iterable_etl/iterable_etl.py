"""cli"""
import click

from iterable_etl.tables.campaign_history import campaign_history_df
from iterable_etl.tables.campaign_list_history import campaign_list_history_df
from iterable_etl.tables.campaign_metrics import campaign_metrics_df
from iterable_etl.tables.list import list_df
from iterable_etl.tables.list_user_history import list_user_history_df
from iterable_etl.tables.user_history import user_history_df


@click.command()
@click.option("--table")
def main(table: str) -> None:
    """program"""
    if table == "campaign_history":
        campaign_history_df()
    elif table == "campaign_metrics":
        campaign_metrics_df()
    elif table == "list":
        list_df()
    elif table == "campaign_list_history":
        campaign_list_history_df()
    elif table == "list_user_history":
        list_user_history_df()
    elif table == "user_history":
        start_date = "2023-06-25"
        end_date = "2023-06-27"
        user_history_df(start_date=start_date, end_date=end_date)
    elif table == "ALL":
        campaign_history_df()
        campaign_metrics_df()
        list_df()
        campaign_list_history_df()
        list_user_history_df()
    else:
        raise ValueError("Invalid table selection")
