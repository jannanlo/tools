# -*- coding:UTF-8 -*-
# Author: Jenner.Luo
import subprocess
import re


class VirshManage(object):
    def __init__(self):
        pass

    @classmethod
    def subprocess_popen(self, cmd_list):
        p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return p.returncode, stdout, stderr

    def domain_state(self, domain):
        res = self.subprocess_popen(["virsh", "domstate", str(domain)])
        return res[1].strip()

    def domain_shutdown(self, domain, wait_result=False):
        res = self.subprocess_popen(["virsh", "shutdown", str(domain)])
        print res[1], res[2]
        if wait_result:
            if res[0] > 0 and 'domain is not running' in res[2]:
                return True
            else:
                while 1:
                    if self.domain_state(domain) == 'shut off':
                        return True

    def domains_shutdown(self, domain_list, wait_result=False):
        for item in domain_list:
            self.domain_shutdown(item, wait_result)

    def domain_destroy(self, domain):
        res = self.subprocess_popen(["virsh", "destroy", str(domain)])
        if res[0] == 0 or 'domain is not running' in res[2]:
            return True
        return False

    def domain_undefine(self, domain):
        res = self.subprocess_popen(["virsh", "undefine", str(domain)])
        if res[0] == 0 or "Domain not found" in res[2]:
            return True
        return False

    def domain_start(self, domain):
        res = self.subprocess_popen(["virsh", "start", str(domain)])
        print res[1], res[2]
        if res[0] == 0 or "Domain is already active" in res[2]:
            return True
        return False

    def domains_start(self, domain_list):
        for domain in domain_list:
            self.domain_start(domain)

    def is_domain_exist(self, domain):
        res = self.subprocess_popen(["virsh", "domstate", str(domain)])
        if res[0] == 0:
            return True
        return False

    def snapshot_list(self, domain):
        res = self.subprocess_popen(["virsh", "snapshot-list", str(domain)])
        if res[0] == 0:
            sp1 = str(res[1]).strip().split("\n")
            if len(sp1) > 2:
                return sp1[2:]

    def domain_blocks(self, domain):
        res = self.subprocess_popen(["virsh", "domblklist", str(domain)])
        if res[0] == 0:
            sp1 = str(res[1]).strip().split("\n")
            if len(sp1) > 2:
                return sp1[2:]

    def rm_domain_blocks(self, domain_blocks):
        for item in domain_blocks:
            new_item = re.subn(r"\s+", " ", str(item).strip())[0].split(" ")
            res = self.subprocess_popen(["rm", "-f", str(new_item[1])])
            if res[0] == 0:
                print "Removed: ", " ".join(new_item)

    def delete_snapshot(self, domain, snapshot_name):
        res = self.subprocess_popen(["virsh", "snapshot-delete",
                                     str(domain), str(snapshot_name)])
        if res[0] == 0 or 'Domain snapshot not found' in res[2]:
            return True
        return False

    def delete_snapshots(self, domain, snapshot_list):
        for item in snapshot_list:
            new_item = re.subn(r"\s+", " ", str(item).strip())[0].split(" ")
            if self.delete_snapshot(domain, new_item[0]):
                print "Deleted: ", " ".join(new_item)

    def create_snapshot(self, domain, snapshot_name):
        res = self.subprocess_popen(["virsh", "snapshot-create-as",
                                     str(domain), str(snapshot_name)])
        print res[1], res[2]
        if res[0] == 0:
            return True
        return False

    def create_same_snapshot_name(self, domain_list, snapshot_name):
        for item in domain_list:
            if self.domain_shutdown(item, True):
                self.create_snapshot(item, snapshot_name)

    def snapshot_revert(self, domain, snapshot_name, running=True):
        cmds = ["virsh", "snapshot-revert", str(domain), str(snapshot_name)]
        if running:
            cmds.extend(['--running', '--force'])
        res = self.subprocess_popen(cmds)
        if res[0] == 0:
            print '{0} revert to {1}'.format(domain, snapshot_name)
            return True
        return False

    def snapshots_revert(self, domain_list, snapshot_name, running=True):
        for item in domain_list:
            self.snapshot_revert(item, snapshot_name, running)

    def delete_domain(self, domain):
        if self.domain_destroy(domain):
            print '=' * 10, 'Deleting: ', domain, '=' * 10
            snapshot_list = self.snapshot_list(domain)
            if snapshot_list:
                self.delete_snapshots(domain, snapshot_list)
            domain_blocks = self.domain_blocks(domain)
            if self.domain_undefine(domain) and domain_blocks:
                self.rm_domain_blocks(domain_blocks)
            print '=' * 10, 'Deleted: ', domain, domain, '=' * 10

    def delete_snapshot_in_domains(self, domain_list, snapshot_name):
        for item in domain_list:
            print 'delete ', item, ' snapshot ', snapshot_name
            self.delete_snapshot(item, snapshot_name)


def vm_in_90():
    vm = VirshManage()
    domain_list = [
        #    'test-rh68-192-168-215-103',
        #    'test-rh68-192-168-215-104',
        #    'test-rh68-192-168-215-105',
        #    'test-rh68-192-168-215-106',
        'test-rh68-192-168-215-110',  # installed-ceph   installed-gluster
        'test-rh68-192-168-215-111',  # installed-ceph  installed-gluster
        # 'test-rh68-192-168-215-112'            #installed-ceph
    ]
    # domain_list = [
    #     'test-rh68-192-168-215-116',
    #     'test-rh68-192-168-215-117',
    #     'test-rh68-192-168-215-118',
    #     'test-rh68-192-168-215-119',
    #     'test-rh68-192-168-215-120',
    #     'test-rh68-192-168-215-121'
    # ]
    # vm.snapshots_revert(domain_list, 'init')
    # vm.snapshots_revert(domain_list, 'installed-ceph')
    # vm.create_same_snapshot_name(domain_list, 'installed-ceph')
    # vm.create_same_snapshot_name(domain_list, 'installed-gluster')
    # vm.domains_start(domain_list)
    vm.delete_snapshot_in_domains(domain_list, 'installed-glusters')

if __name__ == "__main__":
    # vm = VirshManage()
    # domain_list = ['test-rh68-192-168-215-10','test-rh68-192-168-215-21',
    #                'test-rh68-192-168-215-22','test-rh68-192-168-215-23',
    #                'test-rh68-192-168-215-24', 'test-rh68-192-168-215-25']
    # for a in domain_list:
    #     vm.delete_domain(a)
    # vm.create_same_snapshot_name(domain_list, 'init')
    # vm.snapshots_revert(domain_list, 'init')
    vm_in_90()