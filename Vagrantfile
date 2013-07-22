# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.define "tinge" do |tinge|
    tinge.vm.network :private_network, ip: "192.168.57.10"
    tinge.vm.synced_folder ".", "/margarine"
  end

  config.vm.define "blend" do |blend|
    blend.vm.network :private_network, ip: "192.168.57.11"
    blend.vm.synced_folder ".", "/margarine"
  end

  config.vm.define "spread" do |spread|
    spread.vm.network :private_network, ip: "192.168.57.12"
    spread.vm.synced_folder ".", "/margarine"
  end

  config.vm.define "redis" do |redis|
    redis.vm.network :private_network, ip: "192.168.57.13"
  end

  config.vm.define "mongo" do |mongo|
    mongo.vm.network :private_network, ip: "192.168.57.14"
  end

  config.vm.define "rabbit" do |rabbit|
    rabbit.vm.network :private_network, ip: "192.168.57.15"
  end

  config.vm.define "swift" do |swift|
    swift.vm.network :private_network, ip: "192.168.57.16"
  end
end
