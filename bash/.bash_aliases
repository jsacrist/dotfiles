# ls aliases

if command -v eza &> /dev/null; then
    alias ls='eza -lh --group-directories-first --icons=auto'
fi
alias l='ls -lrth --group-directories-first --color=always'
alias la='ls -lrtah --group-directories-first --color=always'
alias ll='ls -lrth --group-directories-first --color=always | less -R'

# tree alias
tl(){ tree -aC "$@" | less -R ; }

# Misc aliases
