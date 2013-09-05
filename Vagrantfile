# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_plugin "vagrant-omnibus"
Vagrant.require_plugin "vagrant-berkshelf"

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.define "rabbitmq" do |rabbitmq|
    rabbitmq.vm.network :private_network, ip: "192.168.57.13"
    
    config.vm.provision "shell", inline: "apt-get update"
    config.vm.provision "shell", inline: "apt-get -y install rabbitmq-server"
  end

  config.vm.define "redis" do |redis|
      redis.vm.network :private_network, ip: "192.168.57.14"
        
      config.vm.provision "shell", inline: "apt-get update"
      config.vm.provision "shell", inline: "apt-get -y install redis-server"
  end

  config.vm.define "mongodb" do |mongodb|
      mongodb.vm.network :private_network, ip: "192.168.57.15"
      
      config.vm.provision :chef_solo do |chef|
      config.omnibus.chef_version = :latest
      chef.node_name = "mongodb"
      chef.add_recipe "apt"
      chef.add_recipe "build-essential"
      chef.add_recipe "mongodb::10gen_repo"
      chef.add_recipe "mongodb"
      chef.add_recipe "mongodb::mongo_user"

      chef.json = {
        :build_essential => {
          :compiletime => true
        },
        :mongodb => {
          :auth => true
          },
      }
    end
  end

  config.vm.define "tinge" do |tinge|
    tinge.vm.network :private_network, ip: "192.168.57.10"

    config.vm.provision :chef_solo do |chef|
      config.omnibus.chef_version = :latest
      chef.node_name = "tinge"
      chef.add_recipe "margarine"
      chef.add_recipe "margarine::tinge"

      chef.json = {
      :margarine => {
        :path => "/srv/www",
        :pyrax_user => "RAX_USERNAME",
        :pyrax_apikey => "RAX_APIKEY",
        :pyrax_region => "RAX_REGION",
        :queue_user => "guest",
        :queue_password => "guest",
        :queue_hostname => "192.168.57.13",
        :mongodb_user => "margarine",
        :mongodb_password => "margarineisawesome!",
        :mongodb_connection_string => "192.168.57.15:27017",
        :mongodb_database => "production",
        :redis_url => "redis://192.168.57.14",
          :tinge => {
            :endpoint => "http://192.168.57.11/v1"
          }
      },
      }
    end
  end

  config.vm.define "blend" do |blend|
    blend.vm.network :private_network, ip: "192.168.57.11"
    
    config.vm.provision :chef_solo do |chef|
      config.omnibus.chef_version = :latest
      chef.node_name = "blend"
      chef.add_recipe "margarine"
      chef.add_recipe "margarine::blend"

      chef.json = {
      :margarine => {
        :path => "/srv/www",
        :pyrax_user => "RAX_USERNAME",
        :pyrax_apikey => "RAX_APIKEY",
        :pyrax_region => "RAX_REGION",
        :queue_user => "guest",
        :queue_password => "guest",
        :queue_hostname => "192.168.57.13",
        :mongodb_user => "margarine",
        :mongodb_password => "margarineisawesome!",
        :mongodb_connection_string => "192.168.57.15:27017",
        :mongodb_database => "production",
        :redis_url => "redis://192.168.57.14",
          :blend => {
            :flask_debug => "true",
            :server_hostname => "http://192.168.57.10"
          }
      },
      }
    end
  end

  config.vm.define "spread" do |spread|
    spread.vm.network :private_network, ip: "192.168.57.12"
    
    config.vm.provision :chef_solo do |chef|
      config.omnibus.chef_version = :latest
      chef.node_name = "spread"
      chef.add_recipe "margarine"
      chef.add_recipe "margarine::spread"
      
      chef.json = {
      :margarine => {
        :path => "/srv/www",
        :pyrax_user => "RAX_USERNAME",
        :pyrax_apikey => "RAX_APIKEY",
        :pyrax_region => "RAX_REGION",
        :queue_user => "guest",
        :queue_password => "guest",
        :queue_hostname => "192.168.57.13",
        :mongodb_user => "margarine",
        :mongodb_password => "margarineisawesome!",
        :mongodb_connection_string => "192.168.57.15:27017",
        :mongodb_database => "production",
        :redis_url => "redis://192.168.57.14",
          :spread => {
            :mailgun_email => "MAILGUN_EMAIL",
            :mailgun_password => "MAILGUN_PASSWORD",
            :from_email => "FROM_EMAIL@DOMAIN.COM",
            :api_server_hostname => "192.168.57.11"
          }
      },
      }

    end
  end

end