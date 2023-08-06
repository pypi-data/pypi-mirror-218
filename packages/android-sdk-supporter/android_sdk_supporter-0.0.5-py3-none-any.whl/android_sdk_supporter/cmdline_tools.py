import os
import platform
import subprocess
import zipfile
import sys
import shutil

class CmdlineTools:
    def __init__(self, android_sdk_directory=None):
        super().__init__()
        self.android_sdk_directory = android_sdk_directory

        if self.android_sdk_directory:
            #cmdline-tools
            cmdline_tools_directory = f"{self.android_sdk_directory}/cmdline-tools"
            if not os.path.exists(cmdline_tools_directory):
                if platform.system() == 'Darwin': #맥
                    from_zip = f"{self.android_sdk_directory}/commandlinetools-mac-9477386_latest.zip"
                    zip_file = zipfile.ZipFile(from_zip)
                    zip_file.extractall(self.android_sdk_directory)
                    zip_file.close()
                elif platform.system() == 'Windows': #윈도우
                    from_zip = f"{self.android_sdk_directory}/commandlinetools-win-9477386_latest.zip"
                    zip_file = zipfile.ZipFile(from_zip)
                    zip_file.extractall(self.android_sdk_directory)
                    zip_file.close()
                elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
                    from_zip = f"{self.android_sdk_directory}/commandlinetools-linux-9477386_latest.zip"
                    zip_file = zipfile.ZipFile(from_zip)
                    zip_file.extractall(self.android_sdk_directory)
                    zip_file.close()
    
