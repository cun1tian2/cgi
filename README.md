imgdspl.cgi   tk2aya, tk2nan, xrehan,
depend on  use CGI qw(escapeHTML); Net::FTP, File::Find
inp-Default dspldir=>"checked", dsplsnl=>"checked", dsplrea=>"checked",
 hdr=>"<center>title</center><!-- -->", hmd=>"hp/adl", fnm=>"imgdspl.htm", tgds=>"img/zzz", exds=>"", ftpsvr, htpsvr.
150705 update imgdspl.cgi, upld to tk2aya, xrehan. 
150711 update imgdspl.cgi,input textからtextareaに変更に伴い@{[escapeHTML($hdr)]}除去
150731 install tk2nan

dbgPlan 150731 
       tgtD 2階層可、3階層NG
       tk2aym->nan-imgdspltry.htm:  img/try/sdb2 img/try/sdb1 アンカー不表示？。↓sjis.jpg削除後も同じ
 hp/にsjis.jpg2個ある、winexplFTPで削除(filezilla/dbu削除不可)(*1。
 sortTry; tgtD入力順で表示OK､tgtDのroot/subD表示はsudD..rootの順OK。 
