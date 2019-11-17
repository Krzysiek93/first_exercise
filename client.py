from serial import Serial
import argparse
import time


class Client(object):

    def __init__(self, device):
        ser = Serial(device)  # device
        ser.write("<<SENDFILE>>\n")  # tell server to send files
        self.readline = lambda: iter(lambda: ser.read(1), "\n")

        while True:
            line = "".join(self.readline())
            if  "<<NAME_LIST>>" in line:
                nameList = line[14:].replace("[","").replace("]","").replace("'","").replace(",","").split()
                break
        self.waiting_for_message("<<END>>") #server informs that there are no more files to send
        ser.write("<<OK>>\n") #tell server that client is ready to receive
        for file in nameList:
            with open(file,"wb") as outfile:
               while True:
                   line = "".join(self.readline())
                   if line == "<<EOF>>":
                       break
                   print >> outfile,line

    def waiting_for_message(self, message):
        timeout = time.time() + 60 * 5  # 5 minutes from now
        while "".join(self.readline()) != message or time.time() > timeout:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=str, default="./ttyclient", help="Enter serial device")
    args = parser.parse_args()
    device = args.device

    client = Client(device)
