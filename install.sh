#!/bin/sh
# init config
_current_dir=$(cd "$(dirname "$0")"; pwd)
cp $_current_dir/data/host_config.json.example $_current_dir/data/host_config.json
# init property
echo -e "\tenter default user name:"
read default_user
echo -e "\tenter default user password:"
read -s default_pass
if [[ $default_user == '' || $default_pass == '' ]];then
  echo 'please setting default user and pass first'
  exit 1
fi
_user=$default_user
_pass=$($_current_dir/utility/crypt.py -s $default_pass)
echo -e "_user=$_user\n_pass=$_pass" > $_current_dir/data/.property
# intall expect
# add alias
alias auto-ssh="$_current_dir/auto_ssh.sh"
