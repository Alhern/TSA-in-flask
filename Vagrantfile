# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/focal64"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = "1"
    vb.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
  end

  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "forwarded_port", guest: 5001, host: 5001

  config.vm.provision :docker
  config.vm.provision "docker-compose-run", type: "shell", preserve_order: true, :run => "always", path: "./vagrant_data/docker/run.sh"

end
