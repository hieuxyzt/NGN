```shell
cd ~
sudo apt-get install maven
sudo apt install openjdk-21-jdk

sudo apt-get install ansible
git clone https://github.com/containernet/containernet.git
sudo ansible-playbook -i "localhost," -c local containernet/ansible/install.yml

sudo cp -r containernet/mininet/ /usr/lib/python3/dist-packages/mininet/
sudo pip install docker --break-system-packages
sudo pip install Flask --break-system-packages --ignore-installed

cd ~/NGN
sh image_build.sh
sudo python3 demo.py
```

1. Thuc hien migrate:
- Thong bao cho partner
- Dung server moi
- Test
- Force update client dieu huong sang ip server moi
2. Thuc hien scale up:
- Theo doi so luong request di vao nginx (prometheus)
- Lay ips cac server dang hoat dong (eureka server/client)
- Call Api trigger tao node moi, refresh nginx (hoac su dung spring cloud gateway)