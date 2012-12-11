#!/bin/bash
# 参数定义
# -h help
# -c list category
# -i item of list alias
# -l hostname
# [laster] -P port
# -p password
# -u username
# [laster] -m modify host config
# -a add host config
# [laster] -d delete host config
# $0 脚本名
# $1 第一个参数
# $@ 所有参数

#_全局变量
#__参数变量
#example
#auto_ssh.sh -h host
#auto_ssh.sh -i alias of host
#auto_ssh.sh -c category
#auto_ssh.sh
_current_dir=$(cd "$(dirname "$0")"; pwd)
d_get_help()
{
    usage="Usage $0 [-l host] [-u user] [-p pass]"
    echo ${usage}
    #todo restruct it later
}
while getopts ":hc:i:l:a" opt; do
  case $opt in
    c )
      __category=$OPTARG;;
    i )
      __alias=$OPTARG;;
    l )
      __host=$OPTARG;;
    p )
      __pass=$OPTARG;;
    u )
      __user=$OPTARG;;
    a )
      __is_add=1;;
    h )
      d_get_help
      exit 0;;
    : ) 
      echo ">>> Error: '-$OPTARG' requires an argument"
      exit 1;;
    ? ) 
      echo ">>> Error: '-$OPTARG' not supported"
      echo $usage
      exit 1;;
  esac
done
shift $(($OPTIND - 1))

d_get_category() {
  declare -a categorys
  local categorys="($($_current_dir/utility/config.py))"
  local i=0
  local category_len=${#categorys[@]}
  if [[ $category_len == 0 ]];then
    echo "get categorys falied"
    exit 1
  fi
  while [[ $i -lt $category_len ]]
  do
    echo -e "\t$i) ${categorys[$i]}"
    let i++
  done
  read category_no
  if [[ ${categorys[$category_no]} == '' ]]
  then
    echo 'unknow category'
    exit 1
  fi
  _category=${categorys[$category_no]}
}
d_get_item() {
  local category=$1
  declare -a items
  local items="($($_current_dir/utility/config.py -c $category))"
  local i=0
  local item_len=${#items[@]}
  if [[ $item_len == 0 ]];then
    echo "get item by category [$_category] falied"
    exit 1
  fi
  while [[ $i -lt $item_len ]]
  do
    echo -e "\t$i) ${items[$i]}"
    let i++
  done
  read item_no
  _host=${items[$item_no]}
}
d_get_host_by_alias() {
  declare -a hosts
  local alias=$1
  local hosts="($($_current_dir/utility/config.py -a $alias))"
  local i=0
  local host_len=${#hosts[@]}
  if [[ $host_len == 0 ]];then
    echo "get host by alias [$__alias] falied"
    exit 1
  fi
  while [[ $i -lt $host_len ]]
  do
    echo -e "\t$i) ${hosts[$i]}"
    let i++
  done
  read host_no
  _host=${hosts[$host_no]}
}
d_get_pass() {
  if [[ $__pass == "" ]]
  then
    echo $($_current_dir/utility/crypt.py -d $_pass)
  else
    echo $__pass
  fi
}
d_get_user() {
  if [[ $__user == "" ]]
  then
    echo $_user
  else
    echo $__user
  fi
}
d_get_host() {
  echo $_host | awk -F ']' '{print $2}'
}

d_login() {
  local host="$(d_get_host)"
  if [[ $host == "" ]]
  then
    echo 'host parameter is required'
    exit 1
  fi
  local user="$(d_get_user)"
  local pass="$(d_get_pass)"
  /usr/bin/expect -f $_current_dir/utility/expect.exp $user $pass $host
}
d_connect() {
  if [[ -n $__host ]];then
    _host=$__host
  elif [[ -n $__category ]];then
    d_get_item $__category
    #get item by category
  elif [[ -n $__alias ]];then
    d_get_host_by_alias $__alias
  else
    d_get_category
    d_get_item $_category
  fi
  d_login
}

. $_current_dir/data/.property
if [[ $__is_add == 1 ]]
then
  #d_add_config
  echo add _config
fi
d_connect
exit 0
