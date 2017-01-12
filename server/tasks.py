import os
import pwd
import re
import subprocess
from shutil import copyfile

import yaml
from celery import Task
from django.conf import settings

from .models import GameServer


class GameServerCreateTask(Task):
    name = 'gameserver.create'

    def run(self, server_id, hostname, **kwargs):
        server = GameServer.objects.get(pk=server_id)
        server.status_id = 5
        server.save(update_fields=['status_id'])

        salt_path = os.path.normpath(settings.SALT_PATH)
        roster_tpl = os.path.join(salt_path, 'config/roster.tpl')
        roster_config = os.path.join(salt_path, 'config/roster')
        copyfile(roster_tpl, roster_config)

        ip_address = hostname
        with open(roster_config, 'r+') as roster_file:
            data = roster_file.read()
            replaced_data = re.sub(r'{{ IP_ADDR }}', ip_address, data)

            roster_file.seek(0)
            roster_file.write(replaced_data)
            roster_file.truncate()

        with open(os.path.join(salt_path, 'pillar/private_panel.sls'), 'w+') as pillar:
            yaml.safe_dump({
                'IP_ADDR': ip_address
            }, pillar)

        import getpass
        pw_record = pwd.getpwnam(getpass.getuser())
        user_name = pw_record.pw_name
        user_home_dir = pw_record.pw_dir
        user_uid = pw_record.pw_uid
        user_gid = pw_record.pw_gid
        env = os.environ.copy()
        env['HOME'] = user_home_dir
        env['LOGNAME'] = user_name
        # env['PWD'] = cwd
        env['USER'] = user_name
        env['VENV'] = os.path.join(salt_path, 'venv/bin')
        env['SALT'] = salt_path
        env['IP'] = ip_address

        os.setgid(user_gid)
        os.setuid(user_uid)

        process = subprocess.Popen(['./scripts/create_game_server.sh'], cwd=salt_path, env=env, shell=True)

        (output, err) = process.communicate()

        p_status = process.wait()

        if p_status == 0:
            celery_output = os.path.join(salt_path, 'output.yaml')
            with open(celery_output, 'r') as stream:
                yaml_output = yaml.load(stream)

            auth_token = yaml_output.get('game-server').get(
                'cmd_|-auth-token_|-/home/game-srv/venv/bin/python manage.py create_user_|-run').get('changes').get(
                'stdout')

            server.status_id = 1
            server.auth_token = auth_token
            server.save()

            return {'id': server.id}

        else:
            server.status_id = 9
            server.save(update_fields=['status_id'])

        return p_status, output, err
