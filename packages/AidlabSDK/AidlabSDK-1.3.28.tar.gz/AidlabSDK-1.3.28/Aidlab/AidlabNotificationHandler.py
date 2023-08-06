#
# AidlabNotificationHandler.py
# Aidlab-SDK
# Created by Szymon Gesicki on 09.05.2020.
#

class AidlabNotificationHandler(object):

    def __init__(self, aidlab_address, delegate, aidlab_characteristics_uuid):
        self.aidlab_address = aidlab_address
        self.delegate = delegate
        self.aidlab_characteristics_uuid = aidlab_characteristics_uuid

    def handle_notification(self, sender, data):

        try:
            sender = sender.upper()
        except AttributeError:
            pass

        if sender == self.aidlab_characteristics_uuid.temperatureUUID["handle"] or sender == self.aidlab_characteristics_uuid.temperatureUUID["uuid"].upper():
            self.delegate.did_receive_raw_temperature(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.ecgUUID["handle"] or sender == self.aidlab_characteristics_uuid.ecgUUID["uuid"].upper():
            self.delegate.did_receive_raw_ecg(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.batteryUUID["handle"] or sender == self.aidlab_characteristics_uuid.batteryUUID["uuid"].upper():
            self.delegate.did_receive_raw_battery_level(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.respirationUUID["handle"] or sender == self.aidlab_characteristics_uuid.respirationUUID["uuid"].upper():
            self.delegate.did_receive_raw_respiration(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.activityUUID["handle"] or sender == self.aidlab_characteristics_uuid.activityUUID["uuid"].upper():
            self.delegate.did_receive_raw_activity(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.stepsUUID["handle"] or sender == self.aidlab_characteristics_uuid.stepsUUID["uuid"].upper():
            self.delegate.did_receive_raw_steps(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.heartRateUUID["handle"] or sender == self.aidlab_characteristics_uuid.heartRateUUID["uuid"].upper() or sender == "2A37":
            self.delegate.did_receive_raw_heart_rate(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.soundVolumeUUID["handle"] or sender == self.aidlab_characteristics_uuid.soundVolumeUUID["uuid"].upper():
            self.delegate.did_receive_raw_sound_volume(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.cmdUUID["handle"] or sender == self.aidlab_characteristics_uuid.cmdUUID["uuid"].upper():
            self.delegate.did_receive_raw_cmd_value(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.orientationUUID["handle"] or sender == self.aidlab_characteristics_uuid.orientationUUID["uuid"].upper():
            self.delegate.did_receive_raw_orientation(data, self.aidlab_address)

        elif sender == self.aidlab_characteristics_uuid.motionUUID["handle"] or sender == self.aidlab_characteristics_uuid.motionUUID["uuid"].upper():
            self.delegate.did_receive_raw_imu_values(data, self.aidlab_address)
