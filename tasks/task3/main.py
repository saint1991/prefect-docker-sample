import time

def main():
    print('Start task3.')
    print('Sleeping 5 sec...')
    time.sleep(5)

    raise RuntimeError("Some error occurred...")

if __name__ == '__main__':
    main()
