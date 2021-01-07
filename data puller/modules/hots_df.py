from .data_forms import hDataForm
import pandas as pd
from pandas import json_normalize
from .utils.helpers import printNewestOldest
from .utils import crawl_stats


def get_paged(h, start_id, form_name, _start_date=None):
    # try:
    rl = h.get_replay_list(min_id=start_id)

    # print(rl[:10])
    # print("")
    # print("length: {}".format(len(rl)))
    # print("last id: {}".format(rl[-1]["parsed_id"]))
    index = 0
    skipped = 0
    temp_df = json_normalize(rl.json())
    temp_df['date'] = pd.to_datetime(temp_df["game_date"])
    temp_df = temp_df.drop(
        columns=['filename', 'size', 'url', 'deleted', 'fingerprint', 'processed', 'region', 'updated_at', 'created_at', 'game_date'])
    # print(temp_df.columns)
    # print(temp_df.head())
    # printNewestOldest(temp_df)
    crawl_stats.setNewestDate(temp_df.date.max())
    crawl_stats.setOldestDate(temp_df.date.min())
    date_mask = (temp_df.date > '2018-06-01')
    df_newer_dates = temp_df.loc[date_mask]
    # printNewestOldest(df_newer_dates)
    crawl_stats.addOld(len(temp_df)-len(df_newer_dates))

    new_form = hDataForm(form_name)

    if len(df_newer_dates) == 0:
        return None

    crawl_stats.setParsedID(df_newer_dates.id.iloc[-1])
    rows = df_newer_dates["id"]

    for row in rows:
        # print(row)
        match = h.get_replay(row)
        if match["game_type"] in ["Brawl", "QuickMatch"]:
            skipped += 1
            continue
        index += 1

        new_form.input_match(match)

    crawl_stats.addDiscardedMode(skipped)

    column_names, object_for_df = new_form.get_output()

    df = pd.DataFrame(object_for_df, columns=column_names)
    # print("\ntotal added: " + str(index+1))
    return df
    # except Exception as e:
    # excpt TypeError:
    # print("Error when request data, last error code:" + str(h.status_code))
    # print("Error when request data, exception:" + str(e))


def get_paged_parsed(h, start_id, form_name):
    # try:
    rl = h.get_replays_parsed(id=start_id)
    # print(rl)
    if rl == []:
        crawl_stats.setCrawlEnd(True)
        return pd.DataFrame()
    if rl == None:
        return pd.DataFrame()
    temp_df = json_normalize(rl)
    # print(temp_df.columns)
    temp_df['date'] = pd.to_datetime(temp_df["game_date"])
    crawl_stats.setNewestDate(temp_df.date.max())
    crawl_stats.setOldestDate(temp_df.date.min())
    # print(temp_df.columns)
    cols_to_drop = ['filename', 'size', 'url', 'deleted', 'fingerprint',
                    'processed', 'region', 'updated_at', 'created_at', 'game_date']
    [cols_to_drop.append(x) for x in temp_df.columns if any(
        word in x for word in [".talents", '.score', '.blizz', '.silenced'])]
    temp_df = temp_df.drop(columns=cols_to_drop)
    # print(temp_df.columns)
    # print(temp_df.head())
    # printNewestOldest(temp_df)
    date_mask = (temp_df.date > '2020-01-01')
    df_newer_dates = temp_df.loc[date_mask]
    # printNewestOldest(df_newer_dates)
    crawl_stats.addOld(len(temp_df)-len(df_newer_dates))

    new_form = hDataForm(form_name)

    if len(df_newer_dates) == 0:
        return pd.DataFrame()

    crawl_stats.setParsedID(df_newer_dates.id.iloc[-1])

    new_form = hDataForm(form_name)
    unwanted_match_types = ["Brawl", "QuickMatch"]
    game_type_filter = (
        ~df_newer_dates["game_type"].isin(unwanted_match_types))
    crawl_stats.addDiscardedMode(len(df_newer_dates[~game_type_filter]))
    df_newer_dates = df_newer_dates[game_type_filter]

    crawl_stats.addCollected(len(df_newer_dates))
    pd.options.display.max_columns = None
    # print(df_newer_dates.head())

    for index, match in df_newer_dates.iterrows():
        new_form.input_match(match)

    column_names, object_for_df = new_form.get_output()

    df = pd.DataFrame(object_for_df, columns=column_names)
    return df
    # except TypeError:
    #    print("Error when request data, last error code:" + str(h.status_code))
