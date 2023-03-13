import os
import storage
import usb_cdc

new_name = "MicroPico"
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = new_name
storage.remount("/", readonly=True)

fs_stat = os.statvfs('/')
print("Disk size in MB", fs_stat[0] * fs_stat[2] / 1024 / 1024)
print("Free space in MB", fs_stat[0] * fs_stat[3] / 1024 / 1024)

usb_cdc.enable(console=True, data=True)

