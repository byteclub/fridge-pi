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

    def __init__(self, mm = None, rotation_degrees = None):
        self.set_metering_mode(mm)
        self.set_rotation(rotation_degrees)

    def set_metering_mode(self, mm):
        if mm != None and not mm in self.ALL_METERING_MODES:
            raise Exception("Unknown metering mode specified: [%s]" % mm)
        self.metering_mode = mm

    def set_rotation(self, rot):
        if rot != None and (rot < 0 or rot > 359):
            raise Exception("Invalid rotation angle specified [%d]" % rot)
        self.rotation_degrees = rot


class RaspiCamera:
    def __init__(self, camconfig = RaspiCameraConfig()):
        self.camconfig = camconfig

    def capture_image_into_file(self, file_name, camconfig = None):
        if camconfig == None:
            camconfig = self.camconfig
        cmd = RaspistillCmdBuilder()
        cmd.take_picture_immediately()
        cmd.save_picture_to_file(file_name)
        if camconfig.metering_mode != None:
            cmd.use_metering_mode(camconfig.metering_mode)
        if camconfig.rotation_degrees != None:
            cmd.rotate_picture(camconfig.rotation_degrees)
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

    def save_picture_to_file(self, file_name):
        self.params.append('-o')
        self.params.append(file_name)

    def use_metering_mode(self, metering_mode):
        self.params.append('-mm')
        self.params.append(metering_mode)

    def rotate_picture(self, rotation):
        self.params.append('-rot')
        self.params.append('%d' % rotation)

    def execute(self):
        subprocess.call(self.params)

