#!/bin/sh

set -e


usage() {
  helptext="$(cat <<EOF
  -h Help
  This File is used to add the following symlins
  /usr/local/bin/wgui -> ./wgui.py
  /usr/local/bin/wpush -> ./plugins/push/__init__.py
  /usr/local/bin/wpull -> ./plugins/pull/__init__.py
  /usr/local/bin/wplugin -> ./plugings/wordpress_plugin/__init__.py

  if wpush, wpull, wplugin already exists it will rename to _wpush, _wpull, and _wplugin

EOF
)"
  echo "$helptext"
}

## Main program start
echo "\n-------------------------------"
echo "| BCGov Devops Gui Installer    |"
echo "-------------------------------\n"


#get options

while getopts ":hrbwe:p:" arg; do
  case "${arg}" in
    h)
      usage
      exit 1
     ;;
    *)
      ;;
  esac
done
work_dir=$(pwd)
symlink_list=('push' 'pull' 'wordpress_plugin')
symlink_alias=('wpush' 'wpull' 'wplugin')
echo 'Creating wgui symlink'
symlink="ln -s ${work_dir}/wgui.py /usr/local/bin/wgui"
$symlink

if [[  -e "/usr/local/bin/_wpush" ]]; then
  # This means that i have already done converting
  echo 'It looks like this script has already been run'
  echo 'Skiping symlink creation, and the moving of old symlinks.'
  #read -p "Please provide your IDIR [$IDIR]? " VALUE
  #IDIR=${VALUE}
else

  echo 'Checking if existing links exists'
  found_flag=true
  count=0
  for i in "${symlink_list[@]}"
  do
    if [[ -f "/usr/local/bin/${symlink_alias[count]}" && ! -f "/usr/local/bin/_${symlink_alias[count]}" ]]; then
      move="mv /usr/local/bin/${symlink_alias[count]} /usr/local/bin/_${symlink_alias[count]}"
      echo $move
      $move
      found_flag=false
      count=$(( $count + 1 ))
    fi
  done
  if $found_flag; then
    #hack just in case this script gets re-run.
    symlink="ln -s /dev/null /usr/local/bin/_wpush"
    echo $symlink
    $symlink
  fi
  echo 'Creating Symlinks'
  count=0
  for i in  "${symlink_list[@]}"
  do
    symlink="ln -s ${work_dir}/plugins/${symlink_list[count]}/__init__.py /usr/local/bin/${symlink_alias[count]}"
    echo $symlink
    $symlink
    count=$(( $count + 1 ))
  done
fi

echo 'Checking if [DEFAULT] needs to be replaced with [User]'
sed -i -e 's/\[DEFAULT\]/\[User\]/g' $HOME/wp_vars

# a bit of a hack, im sure there is an easier way to do this.
set +e
test_repo_section=$(egrep -o '\[Repos\]' $HOME/wp_vars)
test_pipline_section=$(egrep -o '\[plugin_pipeline\]' $HOME/wp_vars)
plugin_path=$(egrep -o 'PATH_TO_PLUGIN_REPO="(.*)"' $HOME/wp_vars | sed 's/PATH_TO_PLUGIN_REPO="//g' | sed 's/"//g')
thene_path=$(egrep -o 'PATH_TO_THEME_REPO="(.*)"' $HOME/wp_vars | sed 's/PATH_TO_THEME_REPO="//g' | sed 's/"//g')
set -e


if [[ -n "$test_repo_section" ]]; then
  echo 'It looks like you already have a Repos section.'
else
  read -p "Please enter you plugin path, if different than: [$plugin_path]? " VALUE
  plugin_path=${VALUE:-$plugin_path}
  read -p "Please enter you theme path, if different than: [$thene_path]? " VALUE
  theme_path=${VALUE:-$thene_path}
  echo 'Appending Repos to end of file.'
  config_text="$(cat <<EOF

\n[Repos]\nplugin=${plugin_path}\ntheme=${theme_path}\n\n[repo_plugin]\nexclude=wordpress-importer,gravityforms\nrsync=True\nrsync_servers=\nrsync_remote=\n
test_url=http://cactuar.dmz/gitlist/
EOF
)"
echo $config_text >> $HOME/wp_vars
fi

if [[ -n "$test_pipline_section" ]]; then
  echo 'It looks like you already have a Pipeline section.'
else
  echo 'Appending Pipeline configurations to end of file.  Values will need to be added.'
  config_text="$(cat <<EOF

\n[plugin_pipeline]\nurl=\ntest_url=\ntoken=\nuser=\npassword=\n
EOF
)"
echo $config_text >> $HOME/wp_vars
fi


exit 1
