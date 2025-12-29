def collate(*args):
    return ','.join(str(arg) for arg in args if arg)
