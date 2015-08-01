imgdspl.cgi v150711
  tk2aym(v150711), tk2nan(V150225), xrehan,(V150705), xrehbr(v110419), xrehbr601(v150205),xres89335(v110117)
  tk2aym2 xress292 (none)
depend on  use CGI qw(escapeHTML); Net::FTP, File::Find
inp-Default dspldir=>"checked", dsplsnl=>"checked", dsplrea=>"checked",
 hdr=>"<center>title</center><!-- -->", hmd=>"hp/adl", fnm=>"imgdspl.htm", tgds=>"img/zzz", exds=>"", ftpsvr, htpsvr.
 
150705 update imgdspl.cgi, upld to tk2aya, xrehan. 
150711 update imgdspl.cgi,input textからtextareaに変更に伴い@{[escapeHTML($hdr)]}除去
150802 Done, tgtD 2階層OK,3階層NG(tgtD tk2nan/img/try/sbd.. sdbの取り違え)
       Done, sort確認 tgtD入力順で表示OK､tgtDのroot/subD表示はsudD..rootの順OK、tgtD/extDの応用でrootのみ選択等可。 
dbgPlan 1508
  dspldirでhp/adl/存在htmファイルのアンカー参照頁の自動生成等

