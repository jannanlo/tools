#!/bin/bash
#Author: ZhenNan.luo(Jenner)
#


append_mountflags(){
    local kolla_conf=$1
    tee $kolla_conf <<-'EOF'
[Service]
MountFlags=shared
EOF
}

set_docker_mountflags(){
    local docker_service_d=/etc/systemd/system/docker.service.d
    mkdir -p $docker_service_d
    local kolla_conf=${docker_service_d}/kolla.conf
    if [[ ! -f $kolla_conf ]]; then
        append_mountflags $kolla_conf
    fi
}

restart_docker(){
    systemctl daemon-reload
    systemctl restart docker
}

set_virt_type(){
    local kolla_nova=/etc/kolla/config/nova
    mkdir -p $kolla_nova
cat << EOF > $kolla_nova/nova-compute.conf
[libvirt]
virt_type=qemu
EOF
}

main(){
    yum install epel-release
    yum install python-pip
    pip install -U pip
    yum install python-devel libffi-devel gcc openssl-devel libselinux-python
    yum install ansible
    curl -sSL https://get.docker.io | bash
    set_docker_mountflags
    restart_docker

    pip install -U docker
    pip install -U Jinja2

    yum install ntp
    systemctl enable ntpd.service
    systemctl start ntpd.service

    systemctl stop libvirtd.service
    systemctl disable libvirtd.service

    pip install kolla-ansible
    cp -r /usr/share/kolla-ansible/etc_examples/kolla /etc/kolla/
    cp /usr/share/kolla-ansible/ansible/inventory/* .
    docker run -d -v /opt/registry:/var/lib/registry -p 4000:5000 --restart=always --name registry registry:2.3
    wget http://tarballs.openstack.org/kolla/images/centos-binary-registry-ocata.tar.gz
    tar zxf centos-binary-registry-ocata.tar.gz -C /opt/registry/
    set_virt_type    #execute this method if your machine is a virtual machine
    kolla-genpwd
}

main