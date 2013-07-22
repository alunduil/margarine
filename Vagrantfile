# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "base" # TODO Change!
  config.vm.box_url = "http://domain.com/path/to/above.box" # TODO Change!

  config.vm.define "tinge" do |tinge|
    config.vm.network :private_network, ip: "192.168.57.10"
    config.vm.synced_folder ".", "/margarine"
  end

  config.vm.define "blend" do |blend|
    config.vm.network :private_network, ip: "192.168.57.11"
    config.vm.synced_folder ".", "/margarine"
  end

  config.vm.define "spread" do |spread|
    config.vm.network :private_network, ip: "192.168.57.12"
    config.vm.synced_folder ".", "/margarine"
  end

  config.vm.define "redis" do |redis|
    config.vm.network :private_network, ip: "192.168.57.13"
  end

  config.vm.define "mongo" do |mongo|
    config.vm.network :private_network, ip: "192.168.57.14"
  end

  config.vm.define "rabbit" do |rabbit|
    config.vm.network :private_network, ip: "192.168.57.15"
  end

  config.vm.define "swift" do |swift|
    config.vm.network :private_network, ip: "192.168.57.16"
  end
end
