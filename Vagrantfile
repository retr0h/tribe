# encoding: UTF-8

Vagrant.configure('2') do |config|
  config.vm.box = 'hashicorp/precise64'
  config.vm.provision 'ansible' do |ansible|
    ansible.playbook = 'vagrant/site.yml'
    ansible.limit = 'all'
    ansible.sudo = true
    ansible.host_key_checking = false
    ansible.limit = 'all'
    # ansible.verbose = "vvv"
    ansible.groups = {
      'etcd-seed' => ['tribe-1'],
      'etcd' => ['tribe-2', 'tribe-3'],
      'etcd-peers:children' => ['etcd-seed', 'etcd']
    }
    ansible.extra_vars = {
      etcd_interface: 'eth1'
    }
  end

  (1..3).each do |i|
    vm_name = "tribe-#{i}"
    config.vm.define vm_name do |c|
      c.vm.host_name = vm_name
      c.vm.network 'private_network', ip: "192.168.20.#{11 + i}" # eth1
    end
  end
end
