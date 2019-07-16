alias l='ls -lrt --group-directories-first'
alias la='ls -lrta --group-directories-first'
tl(){ tree -C "$@" | less -R ; }
