# dotfiles

This repository contains files I use on my linux system's home directory.
They contain my preferences, like aliases and look-n-feel for some command line tools I use (vim, screen, git)

## Instructions

In order to quickly set up a fresh linux distro with these configuration files.  Run the following:

```bash
stow --adopt bash bin git hyprland i3 screen ssh starship tmux vim waybar
git restore .
```

WARNING: This repository includes my own version of .ssh/authorized_keys, don't donwload it if you don't know what that means!!!
