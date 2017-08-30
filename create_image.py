# -*- coding:UTF-8 -*-
# Author: Jenner.Luo

import os
import subprocess
import glob


class CreateImage(object):
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def subprocess_popen(cls, cmd_list, stderr=subprocess.PIPE,shell=False,
                         stdout=subprocess.PIPE):
        p = subprocess.Popen(cmd_list, stdout=stdout, stderr=stderr, shell=shell)
        stdout, stderr = p.communicate()
        return p.returncode, stdout, stderr

    @classmethod
    def glob_file(cls, re_str):
        res = glob.glob(re_str)
        return res[0] if res else re_str

    @classmethod
    def _get_res(cls, res):
        print res[1], res[2]
        if res[0] == 0:
            return True
        return False

    def execute_wget(self, url, args_dict={}):
        return self._get_res(self.subprocess_popen(["wget", str(url)],
                                                   stderr=None))

    def qemu_img_create(self, filename="centos.qcow2", fmt='qcow2',
                        size="10G"):
        return self._get_res(self.subprocess_popen(["qemu-img", "create", "-f", fmt,
                                     filename, size]))

    def virt_install(self, args_dict={}):
        init_arg = {"--virt-type": "kvm", "--name": "centos",
                    "--ram": "1024", "--disk": "{0},format=qcow2".format(
                os.path.join(self.current_dir, "centos.qcow2")),
                    "--network": "network=default",
                    "--graphics": "vnc,listen=0.0.0.0",
                    "--noautoconsole": "", "--os-type=linux": "",
                    "--os-variant=rhel7": "",
                    "--location={0}".format(os.path.join(
                        self.current_dir,self.glob_file("*.iso"))): ""
                    }
        if args_dict:
            init_arg.update(args_dict)
        args = ['virt-install', "--name {0}".format(init_arg.pop("--name")),
                "--ram {0}".format(init_arg.pop("--ram")),
                "--disk {0}".format(init_arg.pop("--disk"))]
        args.extend(["{0} {1}".format(key, val).strip() for key, val in init_arg.iteritems()])
        if "--location=" in " ".join(args):
            print " ".join(args)
            return self._get_res(self.subprocess_popen(args, shell=True))
        return False


if __name__ == "__main__":
    ci = CreateImage()
    url = 'http://mirror.retentionrange.co.bw/centOS/7/isos/x86_64/CentOS-7-x86_64-NetInstall-1611.iso'
    print ci.current_dir
    # ci.execute_wget(url)
    print ci.qemu_img_create()
    print ci.virt_install()
