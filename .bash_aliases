alias l='ls -lrt --group-directories-first'
alias la='ls -lrta --group-directories-first'
ll(){ ls --color=always -lrt "$@" | less -R ; }
lal(){ ls --color=always -lrta "$@" | less -R ; }
tl(){ tree -C "$@" | less -R ; }
