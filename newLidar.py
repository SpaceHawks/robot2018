import pyurg
def main():
    urg = pyurg.UrgDevice()
    if not urg.connect(port="/dev/tty.usbmodem1D1131"):
        print('Connect error')
        exit()

    for i in range(10):
        data, tm = urg.capture()
        if data == 0:
            continue
        print(len(data), tm)



if __name__ == '__main__':
    main()