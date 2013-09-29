# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_plugin "vagrant-omnibus"
Vagrant.require_plugin "vagrant-berkshelf"

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.define "queue" do |queue|
    queue.vm.network :private_network, ip: "192.168.57.13"
    
    queue.vm.provision "shell", inline: "apt-get -q=2 update"
    queue.vm.provision "shell", inline: "apt-get -q=2 -y install rabbitmq-server"
  end

  config.vm.define "token" do |token|
    token.vm.network :private_network, ip: "192.168.57.14"
        
    token.vm.provision "shell", inline: "apt-get -q=2 update"
    token.vm.provision "shell", inline: "apt-get -q=2 -y install redis-server"
  end

  config.vm.define "datastore_mongo" do |datastore_mongo|
    datastore_mongo.vm.network :private_network, ip: "192.168.57.15"
      
    datastore_mongo.omnibus.chef_version = :latest
    datastore_mongo.vm.provision :chef_solo do |chef|
      chef.node_name = "datastore.mongo"

      chef.json = {
        :build_essential => {
          :compiletime => true
        },
        :mongodb => {
          :auth => true
        },
      }

      chef.add_recipe "apt"
      chef.add_recipe "build-essential"
      chef.add_recipe "mongodb::10gen_repo"
      chef.add_recipe "mongodb"
      chef.add_recipe "mongodb::mongo_user"
    end
  end

  config.vm.define "tinge" do |tinge|
    tinge.vm.network :private_network, ip: "192.168.57.10"

    tinge.omnibus.chef_version = :latest
    tinge.vm.provision :chef_solo do |chef|
      chef.node_name = "tinge"

      # TODO Change parameters to use internal services
      # TODO Change path to be /vagrant
      # TODO Common items should be in global Hash
      chef.json = {
        :margarine => {
          :path => "/srv/www", # TODO Probably should be default attribute
          :pyrax_user => "RAX_USERNAME",
          :pyrax_apikey => "RAX_APIKEY",
          :pyrax_region => "RAX_REGION",
          :queue_user => "guest", # TODO Should be default attribute
          :queue_password => "guest", # TODO Should be default attribute
          :queue_hostname => "192.168.57.13",
          :mongodb_user => "margarine", # TODO Should use default?
          :mongodb_password => "margarineisawesome!", # TODO Should use default?
          :mongodb_connection_string => "192.168.57.15:27017", # TODO Match this with queue → datastore_uri or datastore_hostname?
          :mongodb_database => "production",
          :redis_url => "redis://192.168.57.14", # TODO Why URL here but not others?
          :tinge => {
            :endpoint => "http://192.168.57.11/v1"
          }
        },
      }

      chef.add_recipe "margarine"
      chef.add_recipe "margarine::tinge" # TODO This recipe should call the installation, &c
    end
  end

  config.vm.define "blend" do |blend|
    blend.vm.network :private_network, ip: "192.168.57.11"
    
    blend.omnibus.chef_version = :latest
    blend.vm.provision :chef_solo do |chef|
      chef.node_name = "blend"

      # TODO Change parameters to use internal services
      # TODO Change path to be /vagrant
      # TODO Common items should be in global Hash
      chef.json = {
        :margarine => {
          :path => "/srv/www", # TODO Probably should be default attribute
          :pyrax_user => "RAX_USERNAME",
          :pyrax_apikey => "RAX_APIKEY",
          :pyrax_region => "RAX_REGION",
          :queue_user => "guest", # TODO Should be default attribute
          :queue_password => "guest", # TODO Should be default attribute
          :queue_hostname => "192.168.57.13",
          :mongodb_user => "margarine", # TODO Should use default?
          :mongodb_password => "margarineisawesome!", # TODO Should use default?
          :mongodb_connection_string => "192.168.57.15:27017", # TODO Match this with queue → datastore_uri or datastore_hostname?
          :mongodb_database => "production",
          :redis_url => "redis://192.168.57.14", # TODO Why URL here but not others?
          :blend => {
            :flask_debug => "true", 
            :server_hostname => "http://192.168.57.10" 
          }
        },
      }

      chef.add_recipe "margarine"
      chef.add_recipe "margarine::blend" # TODO This recipe should call the installation, &c
    end
  end

  config.vm.define "spread" do |spread|
    spread.vm.network :private_network, ip: "192.168.57.12"
    
    spread.omnibus.chef_version = :latest
    spread.vm.provision :chef_solo do |chef|
      chef.node_name = "spread"

      # TODO Change parameters to use internal services
      # TODO Change path to be /vagrant
      # TODO Common items should be in global Hash
      chef.json = {
        :margarine => {
          :path => "/srv/www", # TODO Probably should be default attribute
          :pyrax_user => "RAX_USERNAME",
          :pyrax_apikey => "RAX_APIKEY",
          :pyrax_region => "RAX_REGION",
          :queue_user => "guest", # TODO Should be default attribute
          :queue_password => "guest", # TODO Should be default attribute
          :queue_hostname => "192.168.57.13",
          :mongodb_user => "margarine", # TODO Should use default?
          :mongodb_password => "margarineisawesome!", # TODO Should use default?
          :mongodb_connection_string => "192.168.57.15:27017", # TODO Match this with queue → datastore_uri or datastore_hostname?
          :mongodb_database => "production",
          :redis_url => "redis://192.168.57.14", # TODO Why URL here but not others?
          :spread => {
            # TODO We should set up a relay mailer for test emails
            :mailgun_email => "MAILGUN_EMAIL", 
            :mailgun_password => "MAILGUN_PASSWORD",
            :from_email => "FROM_EMAIL@DOMAIN.COM",
            :api_server_hostname => "192.168.57.11"
          }
        },
      }

      chef.add_recipe "margarine"
      chef.add_recipe "margarine::spread" # TODO This recipe shoudl call the installation, &c
    end
  end
end
