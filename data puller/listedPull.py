from hotsapi import hotsapi
from hots_df import get_paged
from helpers import makeFilePath
import crawl_stats
import json
import sys


def run(CYCLES):
    STARTING_INDEX = 0  # 20000000
    DEFAULT_HOTSAPI_PAGEING_SIZE = 1000
    ENDING_INDEX = STARTING_INDEX + CYCLES * DEFAULT_HOTSAPI_PAGEING_SIZE

    h = hotsapi()
    amount = 0

    for i in range(STARTING_INDEX, ENDING_INDEX, DEFAULT_HOTSAPI_PAGEING_SIZE):
        crawl_stats.setCycles(i)
        form_name = 'flat_form'
        get_paged(h, i, form_name, _start_date="2018-09-01 00:00")
        sys.stdout.write("\r{}/{}......parsed id: {}  old: {}   collected: {}   skipped_bad_mode: {}......".format(
            crawl_stats.cycles, CYCLES, crawl_stats.parsed_id, crawl_stats.old_dated, crawl_stats.collected, crawl_stats.discarded_mode))
        sys.stdout.flush()


"""         df = get_paged(h, i, form_name)
        amount += len(df)
        if i == STARTING_INDEX:
            df.to_csv(makeFilePath('export_'+form_name),
                      index=False, header=True)
        else:
            df.to_csv(makeFilePath('export_'+form_name),
                      index=False, header=False, mode='a')

    print("\ntotal DF rows amount: "+str(amount)) """


CYCLES = 2
# run(CYCLES)
h = hotsapi()
get_paged(h, 20000000, 'flat_form', _start_date="2018-09-01 00:00")


def test():
    h = hotsapi()
    try:
        # game_type="StormLeague"
        rl = h.get_replay_list(
            start_date="2018-09-01 00:00", end_date="2017-03-01 00:00")

        #r = h.get_replay(rl[0]["id"])
        rl = rl.json()
        print(rl[0])
        print(rl[-1])
        print("\nlen:"+str(len(rl)))
        # print(r)
    except Exception as e:
        # excpt TypeError:
        #print("Error when request data, last error code:" + str(h.status_code))
        print("Error when request data, exception:" + str(e))


# test()
#df = get_paged(h, i, form_name)
#df.to_csv(makeFilePath('export_'+form_name), index=False, header=True)
