```shell
cd ~
sudo apt-get install ansible
git clone https://github.com/containernet/containernet.git
sudo ansible-playbook -i "localhost," -c local containernet/ansible/install.yml

sudo cp -r containernet/mininet/ /usr/lib/python3/dist-packages/mininet/
sudo pip install docker --break-system-packages
sudo pip install Flask --break-system-packages --ignore-installed

cd ~/NGN
sudo python3 demo.py
```