func WorkSetFootNote()
	let l:flg1 = "notef"
	let l:flg2 = "note"
	let l:flg1 = "zhu"
	let l:flg2 = "zw"

	let l:pattern_search = '\[\[[^\[\]]\+_'.l:flg1.'[^\[\]]\+\]\[\[[0-9]\+\]\]\]'
	call search(l:pattern_search, "cw")
	let l:pattern_ref = matchstr(getline('.'), l:pattern_search)
	if l:pattern_ref == ""
		echo "未找到可用引用"
		return
	endif
	let l:pattern_def = substitute(l:pattern_ref, "_".l:flg1, "_".l:flg2, "")

	mark 1
	call setline('.', substitute(getline('.'), "\\V".l:pattern_ref, "", ""))
	call OrgAddFootnote()
	mark 2

	" 假设注释定义在后面
	" call cursor(0, 1)
	let l:notedef_line = search("\\V".l:pattern_def, 'w')
	if l:notedef_line == 0
		echo "未找到定义: ".l:pattern_def
		return
	endif
	call setline('.', substitute(getline('.'), "\\V".l:pattern_def, "", ""))
	let l:notedef = getline('.')
	normal! dddd
	let @" = l:notedef
	normal! `2$p`1
endfunc
augroup Work
	autocmd!
	autocmd FileType org nnoremap <buffer> <space><space> :call WorkSetFootNote()<CR>
	autocmd FileType org :%s/\\\\$\n\n/\\\\\r/e
	autocmd FileType org :%s/注释：\n\n//e
	autocmd FileType org :%s/————--\n\n//e
	autocmd FileType org :%s/\^{\([^}]\+\)}/\1/ge
augroup END
" nmap <local> <leader>n nt]lllvT[hhhT[hhd,fc^I$T]v$hdjj^Ipg[
