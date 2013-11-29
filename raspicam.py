import subprocess
import os

class RaspiCameraConfig:
    METERING_MODE_MATRIX = 'matrix'
    METERING_MODE_AVERAGE = 'average'
    METERING_MODE_BACKLIT = 'backlit'
    METERING_MODE_SPOT = 'spot'

    ALL_METERING_MODES = [
        METERING_MODE_MATRIX,
        METERING_MODE_AVERAGE,
        METERING_MODE_BACKLIT,
        METERING_MODE_SPOT,
    ]

    def __init__(self, mm = METERING_MODE_AVERAGE):
        self.set_metering_mode(mm)

    def set_metering_mode(self, mm):
        if not mm in ALL_METERING_MODES:
            raise Exception("Unknown metering mode specified: [%s]" % mm)
        self.metering_mode = mm


class RaspiCamera:
    def __init__(self, camconfig = RaspiCameraConfig()):
        self.camconfig = camconfig

    def capture_image_into_file(self, file_name, camconfig = None):
        if camconfig == None:
            comconfig = self.camconfig
        cmd = RaspiStillCmdBuilder()
        cmd.take_picture_immediately()
        cmd.save_picture_to_file(file_name)
        cmd.use_metering_mode(camconfig.metering_mode)
        cmd.execute()
        if not os.path.exists(file_name):
            raise Exception("Called raspistill but can't find output file [%s]!" % file_name)
        return file_name


class RaspistillCmdBuilder:
    def __init__(self):
        self.params = ['/usr/bin/raspistill']

    def take_picture_immediately(self):
        self.params.append('-t')
        self.params.append('0')
        return self

    def save_picture_to_file(self, file_name):
        self.params.append('-o')
        self.params.append(file_name)
        return self

    def use_metering_mode(self, metering_mode):
        self.params.append('-mm')
        self.params.append(metering_mode)
        return self

    def execute(self):
        subprocess.call(self.params)

