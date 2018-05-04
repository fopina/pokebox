from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import subprocess
import os

from scans.models import Device, DeviceHistory


class Command(BaseCommand):
    help = 'Scans the network for devices and updates DB'

    def handle(self, *args, **options):
        lines = subprocess.check_output(settings.SCANS_NMAP_COMMAND + ['-sn'] + settings.SCANS_NETWORK).split('\n')

        now = timezone.now().replace(microsecond=0)

        for line in lines:
            if line.startswith('Nmap scan report for '):
                tmp = line[21:]
                if tmp.find(' (') > -1:
                    name = tmp.split(' (')[0]
                    tmp = tmp.split(' (')[1][:-1]
                else:
                    name = ''
                data = [name, tmp, '']
            elif line.startswith('MAC Address:'):
                data[2] = line.split(' ')[2]
                m, created = Device.objects.get_or_create(mac=data[2])
                m.ip = data[1]
                if data[0]:
                    m.name = data[0]
                m.last_seen = now
                m.online = True
                m.save()
                if options.get('verbosity'):
                    self.stdout.write(str(m))


        # update devices not found as offline
        devices = Device.objects.filter(online=True).exclude(last_seen=now)
        # this skips history
        devices.update(online=False)
        # so create it manually
        DeviceHistory.objects.bulk_create([
            DeviceHistory(
                device=device,
                field_changed='online',
                field_value='False',
                field_old_value='True'
            )
            for device in devices
        ])

        try:
            os.kill(
                int(open(settings.NOTIFICATIONS_PID_FILE).read()), 
                30
            )
        except:
            # if signal fails, no one cares, sleep will trigger eventually
            pass