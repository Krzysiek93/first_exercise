from serial import Serial
import os

ser = Serial("./ttydevice") #device
readline = lambda : iter(lambda:ser.read(1),"\n")
path = "/home/krzysztof/PycharmProjects/zadanie1/files/" #path to files
name_dir_list = os.listdir(path)
name_list = []


class Server(object):

    def __init__(self):
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
        while "".join(readline()) != message:
            pass


if __name__ == '__main__':
    serv = Server()
