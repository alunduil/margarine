# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.define "tinge" do |tinge|
    tinge.vm.network :private_network, ip: "192.168.57.10"
    tinge.vm.synced_folder ".", "/margarine"

    config.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = "chef/cookbooks"
      chef.add_recipe("tinge")
    end
  end

  config.vm.define "blend" do |blend|
    blend.vm.network :private_network, ip: "192.168.57.11"
    blend.vm.synced_folder ".", "/margarine"

    config.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = "chef/cookbooks"
      chef.add_recipe("blend")
    end
  end

  config.vm.define "spread" do |spread|
    spread.vm.network :private_network, ip: "192.168.57.12"
    spread.vm.synced_folder ".", "/margarine"

    config.vm.provision "shell", inline: "apt-get install -y curl"
    config.vm.provision "shell", inline: "curl -L https://www.opscode.com/chef/install.sh | sudo bash"

    config.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = "chef/cookbooks"
      chef.add_recipe("spread")
    end
  end

  config.vm.define "rabbit" do |rabbit|
    rabbit.vm.network :private_network, ip: "192.168.57.13"

    config.vm.provision "shell", inline: "apt-get install -y rabbitmq-server"
  end
end
