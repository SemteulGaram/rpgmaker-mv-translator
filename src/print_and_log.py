log_file_path = 'log.txt'

# can input multiple parameters
def log(*args):
    message = ' '.join([str(arg) for arg in args])
    print(message)
    # unicode support log writing to file
    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(message + '\n')