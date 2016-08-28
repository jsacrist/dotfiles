alias l='ls -lrt'
alias la='ls -lrta'
ll(){ ls --color=always -lrt "$@" | less -R ; }
lal(){ ls --color=always -lrta "$@" | less -R ; }
tl(){ tree -C "$@" | less -R ; }
