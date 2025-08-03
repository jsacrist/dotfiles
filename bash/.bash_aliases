# ls aliases
alias l='ls -lrth --group-directories-first --color=always'
alias la='ls -lrtah --group-directories-first --color=always'
alias ll='ls -lrth --group-directories-first --color=always | less -R'

# tree alias
tl(){ tree -aC "$@" | less -R ; }

# Misc aliases
