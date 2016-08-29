# linux_config

This repository contains files I use on my linux system's home directory.
They contain my preferences, like aliases and look-n-feel.

# Instructions

In order to quickly set up a fresh linux distro with these configuration files.  Run the following:

```bash
cd $HOME
git clone https://github.com/jsacrist/linux_config.git
cd linux_config
find . -not -path "*git*" -exec cp -i --parent '{}' "$HOME/" \;
cd ..
rm -rf linux_config
```

