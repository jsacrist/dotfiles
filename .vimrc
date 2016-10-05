
"===============================================================================
set background=dark     " =dark for termansi black screens.
set ts=4        " Tabstop
set sw=4        " Shiftwidth
set ai          " Autoindent.
set incsearch   " Incremental Search
set hlsearch    " Highlight search - set nohl to turn off.
set ruler
set number
set directory=.
set laststatus=2
"=====================================================================
" Indent using coding standards
"
autocmd Filetype c set cindent
autocmd Filetype c set cinoptions=f0,{1s,g0,p0,t0,+2s,u0
autocmd BufNewFile *.c  0r /user/sms/src_hd
syntax on   " Turn on syntax for known file types.

"=====================================================================
"
" Remove ^M from files created in DOS.
" cope with possible multiple trailing ^m's
autocmd BufRead * silent! %s/\r\+$//
"

" '*' Comments a line.
map * ^i/* ^[A */^[

" '_' Uncomments a line.
map _ ^3x$xxx


" <F2> Toggle Tlist window
map <F2> :TlistToggle<CR>

set tags=./tags,tags

if ! &diff
	au BufRead,BufNewFile * match ErrorMsg /\%>80v.\+/
endif

filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab

