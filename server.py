from serial import Serial
import os
import argparse
import time

name_list = []


class Server(object):

    def __init__(self, device, path):
        ser = Serial(device)  # device
        self.readline = lambda: iter(lambda: ser.read(1), "\n")
        name_dir_list = os.listdir(path)

        self.waiting_for_message("<<SENDFILE>>")
        for element in name_dir_list:
            stat_info = os.stat(path+'/'+element)
            file_size = stat_info.st_size
            if file_size < 4096:
                name_list.append(element)
        ser.write("\n<<NAME_LIST>> %s\n" % name_list)
        ser.write("\n<<END>>\n") #sending file nemes end
        self.waiting_for_message("<<OK>>")
        for file in name_list:
            ser.write(open(path+'/'+file,"rb").read())
            ser.write("\n<<EOF>>\n") # sending file end

    def waiting_for_message(self, message):
        timeout = time.time() + 60 * 5  # 5 minutes from now
        while "".join(self.readline()) != message or time.time() > timeout:
            pass


if __name__ == '__main__':
    parser =argparse.ArgumentParser()
    parser.add_argument("--device", type=str, default="./ttydevice", help="Enter serial device")
    parser.add_argument("--path", type=str, default="/home/krzysztof/PycharmProjects/zadanie1"
                                                    "/files/", help="Enter path to artifacts")
    args = parser.parse_args()
    path = args.path
    device = args.device
    serv = Server(device, path)
