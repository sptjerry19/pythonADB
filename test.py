import os, time, sys
try: 
    import numpy as np
    import cv2
    import subprocess
    import threading
except: 
    os.system("pip install cv2")
    os.system("pip install numpy")
    os.system("pip install opencv-python")
import numpy as np
import cv2
import subprocess
import threading

class ADB:
    def __init__(self,handle):
        self.handle = handle

    def screen_capture(self,name):
        os.system(f"adb -s {self.handle} exec-out screencap -p > {name}.png ")

    def click(self,x,y):
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")

    def send_text(self, text):
        os.system(f"adb -s {self.handle} shell input text '{text}'")

    def find(self,img='',template_pic_name=False,threshold=0.99):
        if template_pic_name == False:
            self.screen_capture(self.handle)
            template_pic_name = self.handle+'.png'
        else:
            self.screen_capture(template_pic_name)
        img = cv2.imread(img)
        img2 = cv2.imread(template_pic_name)
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        test_data = list(zip(*loc[::-1]))
        return test_data


def execute_adb_command(device_id, command):
    """Execute ADB command for a specific device."""
    adb_command = ['adb', '-s', device_id] + command
    subprocess.run(adb_command, check=True)

def perform_action_on_devices(device_ids, command):
    """Perform an action on multiple devices simultaneously."""
    threads = []
    for device_id in device_ids:
        thread = threading.Thread(target=execute_adb_command, args=(device_id, command))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def chrome(d):
    name = 2
    while True:
        try:
            image1 = d.find('./images/1.png')
            if image1>[(0,0)]:
                d.click(image1[0][0], image1[0][1])
                step(d, name)
                break
            else:
                step(d,name)
                break
        except:
            return "can not find image"

def step(d, name):
    while True:
        try:
            image_path = './images/' + str(name) + '.png'
            print(image_path)
            time.sleep(2)
            image = d.find(image_path)
            name+=1
            print(name)
            if name == 6:
                text_to_fill = "hello world"
                print(text_to_fill)
                d.send_text(text_to_fill)
                break

            if image>[(0,0)]:
                print("have image", image)
                time.sleep(2)
                d.click(image[0][0], image[0][1])
                step(d, name)
                break
            else:
                print("dont have image")
                step(d, name)
                break
        except:
            return 0


def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if len(p) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 0


class starts(threading.Thread):
    def __init__(self, nameLD, i):
        super().__init__()
        self.nameLD = nameLD
        self.device = i
    def run(self):
        device = self.device
        d = ADB(device)
        print("click to image 1")
        chrome(d)
        # d.DumpXML()



# if __name__ == "__main__":
#     connected_devices = get_connected_devices()
#     thread_count = len(connected_devices)
#     print("count conected device: ", thread_count)
#     print("Connected devices:", connected_devices)
    # d = ADB(connected_devices[0])
    # print(d)
    # print("click to image 1")
    # run(d)
    # listdevice = get_connected_devices()
    # thread_count = len(listdevice)
    # print(thread_count)

def main(m):
    device = GetDevices()[m]
    for i in range(m, 1, thread_count):
        run = starts(device,device,)
        run.run()

connected_devices = GetDevices()
thread_count = len(connected_devices)
print("count conected device: ", thread_count)
print("Connected devices:", connected_devices)

for m in range(thread_count):
    threading.Thread(target=main, args=(m)).start()

