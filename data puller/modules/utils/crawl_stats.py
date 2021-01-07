old_dated = 0
parsed_id = 0
collected = 0
discarded_mode = 0
cycles = 0
oldest_date = ''
newest_date = ''
crawl_ended = False


def addCollected(amount):
    global collected
    collected += amount


def addOld(amount):
    global old_dated
    old_dated += amount


def setParsedID(id):
    global parsed_id
    parsed_id = id


def addDiscardedMode(amount):
    global discarded_mode
    discarded_mode += amount


def setCycles(number):
    global cycles
    cycles = number


def setOldestDate(inputDate):
    global oldest_date
    oldest_date = inputDate


def setNewestDate(inputDate):
    global newest_date
    newest_date = inputDate


def setCrawlEnd(state):
    global crawl_ended
    crawl_ended = state
