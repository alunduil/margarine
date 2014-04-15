# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_plugin 'vagrant-omnibus'
Vagrant.require_plugin 'vagrant-berkshelf'

ip_addresses = {
  :tinge       => '192.0.2.2',
  :blend       => '192.0.2.3',
  :spread      => '192.0.2.4',

  :queue       => '192.0.2.5',
  :token_store => '192.0.2.6',
  :datastore   => '192.0.2.7',
}

Vagrant.configure('2') do |config|
  config.vm.box = 'precise64'
  config.vm.box_url = 'http://files.vagrantup.com/precise64.box'

  config.vm.define 'token_store' do |token_store|
    token_store.vm.network :private_network, ip: ip_addresses[:token_store]
        
    token_store.vm.synced_folder '.', '/vagrant', :disabled => true

    token_store.vm.provision 'shell', inline: <<-EOF
      apt-get -qq update
      apt-get -qq -y install redis-server
      sed -i -e \'s/bind 127.0.0.1/#\0/\' /etc/redis/redis.conf
      service redis-server restart
    EOF
  end

  config.vm.define 'queue' do |queue|
    queue.vm.network :private_network, ip: ip_addresses[:queue]

    queue.vm.synced_folder '.', '/vagrant', :disabled => true

    queue.omnibus.chef_version = :latest
    queue.vm.provision :chef_solo do |chef|
      chef.node_name = 'queue'

      chef.log_level = :warn

      chef.json = {
        'rabbitmq' => {
          'enabled_plugins' => [
            'rabbitmq_management',
          ],
          'use_distro_version' => true,
        },
      }

      chef.add_recipe 'apt'
      chef.add_recipe 'rabbitmq'
      chef.add_recipe 'rabbitmq::plugin_management'
    end
  end

  config.vm.define 'datastore' do |datastore|
    datastore.vm.network :private_network, ip: ip_addresses[:datastore]
      
    datastore.vm.synced_folder '.', '/vagrant', :disabled => true

    datastore.omnibus.chef_version = :latest
    datastore.vm.provision :chef_solo do |chef|
      chef.node_name = 'datastore'

      chef.log_level = :warn

      chef.json = {
        'build_essentail' => {
          'compiletime' => true,
        },
      }

      chef.add_recipe 'apt'
      chef.add_recipe 'build-essential'
      chef.add_recipe 'mongodb::10gen_repo'
      chef.add_recipe 'mongodb'
    end
  end

  [ :tinge, :blend, :spread ].each do |component|
    config.vm.define component do |box|
      box.vm.network :private_network, ip: ip_addresses[component]

      box.vm.provision 'shell', inline: <<-EOF
        apt-get -qq update
        apt-get -qq -y install python-pip build-essential python-dev
        ln -snf /vagrant/conf /etc/margarine
        pip install -q -e /vagrant 
        start-stop-daemon -Sbmp /run/#{component}.pid --exec /usr/local/bin/#{component}
      EOF
    end
  end
end
