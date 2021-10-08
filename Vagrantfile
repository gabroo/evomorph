Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "8192"
    vb.cpus = "4"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get upgrade -y
  SHELL

  # (optional) use this if you have clock skew issues
  # to install, run `vagrant plugin install vagrant-timezone`
  if Vagrant.has_plugin?("vagrant-timezone")
    config.timezone.value = "America/Los_Angeles"
  end
end
