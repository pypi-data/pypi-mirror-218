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

        if self.android_sdk_directory:
            #platform-tools
            platform_tools_directory = f"{self.android_sdk_directory}/platform-tools"
            if not os.path.exists(platform_tools_directory):
                if platform.system() == 'Darwin': #맥
                    from_zip = f"{self.android_sdk_directory}/platform-tools_r34.0.3-darwin.zip"
                    zip_file = zipfile.ZipFile(from_zip)
                    zip_file.extractall(self.android_sdk_directory)
                    zip_file.close()
                elif platform.system() == 'Windows': #윈도우
                    from_zip = f"{self.android_sdk_directory}/platform-tools_r34.0.3-windows.zip"
                    zip_file = zipfile.ZipFile(from_zip)
                    zip_file.extractall(self.android_sdk_directory)
                    zip_file.close()
                elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
                    from_zip = f"{self.android_sdk_directory}/platform-tools_r34.0.3-linux.zip"
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
        self.devices.clear()
        for output in outputs.split("\n")[1:]:
            output = output.strip()
            #print(output) #R95RB00QRCY     device
            if output:
                device, status = output.split("\t")
                self.devices.append({"device": device, "status": status})
        #print(self.devices) #[{'device': 'R95RB00QRCY', 'status': 'unauthorized'}]
        return self.devices
    
    def data_disable(self):
        if not self.devices:
            self.check_devices()
            
        if self.devices:
            if self.android_sdk_directory:
                adb = f"{self.android_sdk_directory}/platform-tools/adb"
            else:
                adb = "adb"
            cmd = f"{adb} -s {self.devices[0]["device"]} shell svc data disable"
            os.system(cmd)

    def data_enable(self):
        if not self.devices:
            self.check_devices()
        
        if self.devices:        
            if self.android_sdk_directory:
                adb = f"{self.android_sdk_directory}/platform-tools/adb"
            else:
                adb = "adb"
            cmd = f"{adb} -s {self.devices[0]["device"]} shell svc data enable"
            os.system(cmd)

    def cmd(self, command):
        if self.android_sdk_directory:
            command = f"{self.android_sdk_directory}/platform-tools/{command}"
        os.system(command)
 
