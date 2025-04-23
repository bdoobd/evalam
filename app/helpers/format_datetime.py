import copy

def format_date(item):
    cloned = copy.deepcopy(item)
    cloned.stock.date = cloned.stock.date.strftime('%d.%m.%Y')

    return cloned