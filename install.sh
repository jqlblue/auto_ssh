#!/bin/sh
# init config
_current_dir=$(cd "$(dirname "$0")"; pwd)
cp $_current_dir/data/host_config.json.example $_current_dir/data/host_config.json
# init property
echo -e "\tenter default user name:"
read default_user
echo -e "\tenter default user password:"
read -s default_pass
echo -e "\tenter default ssh port:"
read -s default_port
if [[ $default_user == '' || $default_pass == '' || $default_port == '' ]];then
  echo 'please setting default user, pass, port first'
  exit 1
fi
_user=$default_user
_pass=$($_current_dir/utility/crypt.py -s $default_pass)
_port=$default_port
echo -e "[default]\nuser = $_user\npass = $_pass\nport = $_port" > $_current_dir/data/.profile.ini
# chmod
chmod +x $_current_dir/auto_ssh.sh
chmod +x $_current_dir/utility/config.py
chmod +x $_current_dir/utility/crypt.py
chmod +x $_current_dir/utility/expect.exp
# add alias [later]
#alias auto-ssh="$_current_dir/auto_ssh.sh"
