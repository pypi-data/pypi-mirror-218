import os
import platform
import subprocess
import zipfile
import sys
import shutil

class PlatformTools:
    def __init__(self, android_sdk_directory=None):
        super().__init__()
        self.android_sdk_directory = android_sdk_directory
        self.devices = []

        #build-tools
        if platform.system() == 'Darwin': #맥
            from_zip = f"{self.android_sdk_directory}/build-tools_r34-rc4-macosx.zip"
            if not os.path.exists(from_zip):
                zip_file = zipfile.ZipFile(from_zip)
                zip_file.extractall(self.android_sdk_directory)
                zip_file.close()
                shutil.move(f"{self.android_sdk_directory}/android-UpsideDownCake", f"{self.android_sdk_directory}/build-tools")
        elif platform.system() == 'Windows': #윈도우
            from_zip = f"{self.android_sdk_directory}/build-tools_r34-rc4-windows.zip"
            if not os.path.exists(from_zip):
                zip_file = zipfile.ZipFile(from_zip)
                zip_file.extractall(self.android_sdk_directory)
                zip_file.close()
                shutil.move(f"{self.android_sdk_directory}/android-UpsideDownCake", f"{self.android_sdk_directory}/build-tools")
        elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
            from_zip = f"{self.android_sdk_directory}/build-tools_r34-rc4-linux.zip"
            if not os.path.exists(from_zip):
                zip_file = zipfile.ZipFile(from_zip)
                zip_file.extractall(self.android_sdk_directory)
                zip_file.close()
                shutil.move(f"{self.android_sdk_directory}/android-UpsideDownCake", f"{self.android_sdk_directory}/build-tools")

        #cmdline-tools
        if platform.system() == 'Darwin': #맥
            from_zip = f"{self.android_sdk_directory}/commandlinetools-mac-9477386_latest.zip"
            if not os.path.exists(from_zip):
                zip_file = zipfile.ZipFile(from_zip)
                zip_file.extractall(self.android_sdk_directory)
                zip_file.close()
        elif platform.system() == 'Windows': #윈도우
            from_zip = f"{self.android_sdk_directory}/commandlinetools-win-9477386_latest.zip"
            if not os.path.exists(from_zip):
                zip_file = zipfile.ZipFile(from_zip)
                zip_file.extractall(self.android_sdk_directory)
                zip_file.close()
        elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
            from_zip = f"{self.android_sdk_directory}/commandlinetools-linux-9477386_latest.zip"
            if not os.path.exists(from_zip):
                zip_file = zipfile.ZipFile(from_zip)
                zip_file.extractall(self.android_sdk_directory)
                zip_file.close()

        #platform-tools
        if platform.system() == 'Darwin': #맥
            from_zip = f"{self.android_sdk_directory}/platform-tools_r34.0.3-darwin.zip"
            if not os.path.exists(from_zip):
                zip_file = zipfile.ZipFile(from_zip)
                zip_file.extractall(self.android_sdk_directory)
                zip_file.close()
        elif platform.system() == 'Windows': #윈도우
            from_zip = f"{self.android_sdk_directory}/platform-tools_r34.0.3-windows.zip"
            if not os.path.exists(from_zip):
                zip_file = zipfile.ZipFile(from_zip)
                zip_file.extractall(self.android_sdk_directory)
                zip_file.close()
        elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
            from_zip = f"{self.android_sdk_directory}/platform-tools_r34.0.3-linux.zip"
            if not os.path.exists(from_zip):
                zip_file = zipfile.ZipFile(from_zip)
                zip_file.extractall(self.android_sdk_directory)
                zip_file.close()
                
    '''
$ adb devices
List of devices attached
R95RB00QRCY     offline


$ adb devices
List of devices attached
R95RB00QRCY     unauthorized


$ adb devices
List of devices attached
R95RB00QRCY     device    
    '''
    def check_devices(self):   
        if self.android_sdk_directory:
            cmd = f"{self.android_sdk_directory}/platform-tools/adb"
        else:
            cmd = "adb"
        outputs = subprocess.check_output([cmd, "devices"]).decode('utf-8')
        devices = []
        for output in outputs.split("\n")[1:]:
            output = output.strip()
            #print(output) #R95RB00QRCY     device
            if output:
                device, status = output.split("\t")
                devices.append({"device": device, "status": status})
        #print(devices) #[{'device': 'R95RB00QRCY', 'status': 'unauthorized'}]
        return devices
    
    def data_disable(self):
        if self.android_sdk_directory:
            adb = f"{self.android_sdk_directory}/platform-tools/adb"
        else:
            adb = "adb"
        cmd = f"{adb} -s {self.devices[0]} shell svc data disable"
        os.system(cmd)

    def data_enable(self):
        if self.android_sdk_directory:
            adb = f"{self.android_sdk_directory}/platform-tools/adb"
        else:
            adb = "adb"
        cmd = f"{adb} -s {self.devices[0]} shell svc data enable"
        os.system(cmd)

if __name__ == "__main__":
    android_sdk_directory = os.path.dirname(__file__) + "/android_sdk"
    platform_tools = PlatformTools(android_sdk_directory)

    devices = platform_tools.check_devices()

    print(devices)
