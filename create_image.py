# -*- coding:UTF-8 -*-
# Author: Jenner.Luo

import os
import subprocess


class CreateImage(object):
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def subprocess_popen(cls, cmd_list):
        p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return p.returncode, stdout, stderr

    def execute_wget(self, url, args_dict={}):
        print args_dict
        p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
        print 11, self.subprocess_popen(["wget", str(url)])

    def qemu_img_create(self, filename="centos.qcow2", fmt='qcow2', size="10G"):
        res = self.subprocess_popen(["qemu-img", "create", "-f", fmt,
                                      filename, size])
        print res[1], res[2]
        if res[0] == 0:
            return True
        return False

    def virt_install(self, args_dict={}):
        if args_dict:
            args_dict.update({"--virt-type": "kvm", "--name": "centos",
                              "--ram":"1024"})
        res = self.subprocess_popen()


if __name__ == "__main__":
    ci = CreateImage()
    url = 'http://mirror.retentionrange.co.bw/centOS/7/isos/x86_64/CentOS-7-x86_64-NetInstall-1611.iso'
    print ci.current_dir
    # ci.execute_wget(url, {'-p':ci.current_dir})
    ci.qemu_img_create()