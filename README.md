# linux_config

This repository contains files I use on my linux system's home directory.
They contain my preferences, like aliases and look-n-feel.

# INSTRUCTIONS

In order to quickly set up a fresh linux distro with these configuration files.  Run the following:



```bash
	git clone https://github.com/jsacrist/linux_config.git
	find linux_config/ -not -path "*git*" -exec cp -ir '{}' "$HOME/" \;
	rm -rf linux_config
```

