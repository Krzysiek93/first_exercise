from serial import Serial

ser = Serial("./ttyclient") #device
ser.write("<<SENDFILE>>\n") #tell server to send files
readline = lambda : iter(lambda:ser.read(1),"\n")


class Client(object):

    def __init__(self):
        while True:
            line = "".join(readline())
            if  "<<NAME_LIST>>" in line:
                nameList = line[14:].replace("[","").replace("]","").replace("'","").replace(",","").split()
                break
        self.waiting_for_message("<<END>>") #server informs that there are no more files to send
        ser.write("<<OK>>\n") #tell server that client is ready to receive
        for file in nameList:
            with open(file,"wb") as outfile:
               while True:
                   line = "".join(readline())
                   if line == "<<EOF>>":
                       break
                   print >> outfile,line

    def waiting_for_message(self, message):
        while "".join(readline()) != message:
            pass


if __name__ == '__main__':
    client = Client()
