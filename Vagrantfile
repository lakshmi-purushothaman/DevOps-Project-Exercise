Vagrant.configure("2") do |config|
  
  config.vm.box = "hashicorp/bionic64"

  #Pyenv setup
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    # Install pyenv prerequisities
    sudo apt-get -y update
    sudo apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

    #Install pyenv
    rm -rf ~/.pyenv
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

    cd ~/.pyenv && src/configure && make -C src

    #Configure shell's environment for Python
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo 'eval "$(pyenv init --path)"' >> ~/.profile

    #Sourcing .profile
    source ~/.profile

    #Install Python
    pyenv install 3.9.6

    #Setting global Python version
    pyenv global 3.9.6

    #Install Poetry
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

  SHELL

  #Trigger to install app dependencies
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script" 
    trigger.run_remote = {privileged: false, inline: "
      # Install dependencies and launch
      cd /vagrant
      poetry install
      poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
      #gunicorn --bind 0.0.0.0:5000 wsgi:app
    "}
  end

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:5000" will access port 5000 on the guest machine.
  # NOTE: This will enable public access to the opened port
  config.vm.network "forwarded_port", guest: 5000, host: 5000
end