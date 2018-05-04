from django.core.management.base import BaseCommand,CommandError
from django.conf import settings
from django.utils import timezone
from notifications.models import Telegram, Message
from scans.models import Device, DeviceHistory
from time import sleep
import os
import signal


class Command(BaseCommand):
    help = 'Dispatch pending notifications'

    def handle(self, *args, **options):
        try:
            cpid = int(open(settings.NOTIFICATIONS_PID_FILE).read())
            try:
                os.kill(cpid, 0)
                raise CommandError('Process already running (pid %d)' % cpid)
            except OSError as e:
                # error 3: no such process, great!
                if e.errno != 3:
                    raise
        except IOError:
            # no file, no process
            pass

        # signal handler itself is irrelevant, we just want to
        # be able to break sleep() syscall :)
        signal.signal(signal.SIGUSR1, self.signal)
        open(settings.NOTIFICATIONS_PID_FILE, 'w').write(str(os.getpid()))
        _x = DeviceHistory.objects.order_by('pk').last()
        last_history = _x.pk if _x else -1
        
        try:
            while True:
                qs = DeviceHistory.objects.order_by('pk').filter(pk__gt=last_history)
                proc = 0
                for history in qs:
                    proc += 1
                    for t in Telegram.objects.all():
                        t.notify(str(history))
                    last_history = history.pk
                if proc > 0:
                    self.stdout.write('%d events added to queue' % proc)

                proc = [0, 0]
                for message in Message.objects.filter(sent=None):
                    res = message.post()
                    if res is True:
                        proc[1] += 1
                    proc[0] += 1
                if proc[0] > 0:
                    self.stdout.write('%d messages posted (%d processed)' % (proc[1], proc[0]))

                sleep(30)
        except KeyboardInterrupt:
            pass

    def signal(self, signal, frame):
        # may be used in the future..
        self.stdout.write('signal received...\n')
