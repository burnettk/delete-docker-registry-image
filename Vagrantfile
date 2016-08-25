Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  name = 'test-delete-docker-registry-image-docker-latest'
  config.vm.define name
  config.vm.provider "virtualbox" do |v|
    v.name = name
  end
  config.vm.hostname = name

  config.vm.provision :shell, path: "install_docker.sh"

  # you will need to install a vagrant plugin first: vagrant plugin install vagrant-docker-compose
  config.vm.provision :docker_compose, project_name: 'registry', yml: "/vagrant/test/docker-compose.yml", run: "always"
end
