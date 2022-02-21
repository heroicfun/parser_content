import shelve


def open_db(filename='database'):
    return shelve.open(filename)


def write_to_db(results, shelf):
    for key, value in results.items():
        if key not in shelf.keys():
            shelf[key] = value


def close(shelf):
    shelf.close()