# -*- coding:UTF-8 -*-
# Author: Jenner.Luo

import subprocess


class CreateImage(object):
    def __init__(self):
        pass

    @classmethod
    def subprocess_popen(self, cmd_list):
        p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return p.returncode, stdout, stderr