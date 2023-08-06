import os
import platform
import subprocess
import zipfile
import sys
import shutil

class BuildTools:
    def __init__(self, android_sdk_directory=None):
        super().__init__()
        self.android_sdk_directory = android_sdk_directory

        if self.android_sdk_directory:
            #build-tools
            build_tools_directory = f"{self.android_sdk_directory}/build-tools"
            if not os.path.exists(build_tools_directory):
                if platform.system() == 'Darwin': #맥
                    from_zip = f"{self.android_sdk_directory}/build-tools_r34-rc4-macosx.zip"
                    zip_file = zipfile.ZipFile(from_zip)
                    zip_file.extractall(self.android_sdk_directory)
                    zip_file.close()
                    shutil.move(f"{self.android_sdk_directory}/android-UpsideDownCake", f"{self.android_sdk_directory}/build-tools")
                elif platform.system() == 'Windows': #윈도우
                    from_zip = f"{self.android_sdk_directory}/build-tools_r34-rc4-windows.zip"
                    zip_file = zipfile.ZipFile(from_zip)
                    zip_file.extractall(self.android_sdk_directory)
                    zip_file.close()
                    shutil.move(f"{self.android_sdk_directory}/android-UpsideDownCake", f"{self.android_sdk_directory}/build-tools")
                elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
                    from_zip = f"{self.android_sdk_directory}/build-tools_r34-rc4-linux.zip"
                    zip_file = zipfile.ZipFile(from_zip)
                    zip_file.extractall(self.android_sdk_directory)
                    zip_file.close()
                    shutil.move(f"{self.android_sdk_directory}/android-UpsideDownCake", f"{self.android_sdk_directory}/build-tools")
    
