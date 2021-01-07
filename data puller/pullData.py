from modules.hotsapi import hotsapi
from modules.hots_df import get_paged_parsed
from modules.utils.helpers import makeFilePath
from modules.utils import crawl_stats
import sys


def run(CYCLES):
    STARTING_INDEX = 25060000
    DEFAULT_HOTSAPI_PAGEING_SIZE = 100
    ENDING_INDEX = STARTING_INDEX + CYCLES * DEFAULT_HOTSAPI_PAGEING_SIZE

    h = hotsapi()
    amount = 0

    for i in range(STARTING_INDEX, ENDING_INDEX, DEFAULT_HOTSAPI_PAGEING_SIZE):
        form_name = 'flat_form'
        df = get_paged_parsed(h, i, form_name)
        crawl_stats.setParsedID(i+DEFAULT_HOTSAPI_PAGEING_SIZE)

        if df.empty == False:
            amount += len(df)
            if i == STARTING_INDEX:
                df.to_csv(makeFilePath('export_'+form_name),
                          index=False, header=True)
            else:
                df.to_csv(makeFilePath('export_'+form_name),
                          index=False, header=False, mode='a')
        crawl_stats.setCycles((i-STARTING_INDEX) /
                              DEFAULT_HOTSAPI_PAGEING_SIZE)

        sys.stdout.write("\r{}/{}......end id: {}  old: {}   collected: {}   skipped_bad_mode: {} oldest: {} newest: {}......".format(
            crawl_stats.cycles+1, CYCLES, crawl_stats.parsed_id, crawl_stats.old_dated, crawl_stats.collected, crawl_stats.discarded_mode,
            crawl_stats.oldest_date, crawl_stats.newest_date))
        sys.stdout.flush()
        if crawl_stats.crawl_ended:
            print("\nending crawl due to index end...")
            break
    print("\ntotal DF rows amount: "+str(amount))


CYCLES = 1
run(CYCLES)
