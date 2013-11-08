#!/usr/bin/perl --
# imgdspl.cgi 131022reviced(javascript 子窓onclick化 foldersFilesArray.sort()、親窓フォーカス )110419acfhgk tmp.cgi 110414rev-all rftpのみTOK 110117-10:(escapeHTML他)
use CGI qw(escapeHTML);  		# use Net::FTP or File::Find at concerned_proc
sub cgihtmout;
$cgi=CGI->new();
$hdr=$cgi->param("hdr") || "<center>title</center>";		## header
$ftpsvr0=$cgi->param("ftpsvr");					## ftpsvr
($usr,$pw,$ftpsvr,$path)=($ftpsvr0=~/ftp:\/\/([^:]+):([^@]+)@([^\/]+)(.*)/) if $ftpsvr0; ##
$htpsvr=$cgi->param("htpsvr");					## htpsvr
$dsp=$cgi->param("dsp");					## dirDisplay(nocheck=>suppress)
$htmfile=$cgi->param("fnm") || "imgdspl.htm";			## htmFileName
$hmd=$hmd_depth=($cgi->param("hmd") ? $cgi->param("hmd") : "hp/adl"); ## homeDir
$hmd_depth=~s/[^\/]+/\.\./g;					# homeDir_depth_rootUp
@exds=$cgi->param("exd");
$re=join "|",grep{quotemeta $_}@exds;				## exceptDirs(reg_Exp)
($itself)=($0=~/([^\/]+)$/);
$ftpput="${itself}_tmp.txt";					# ftpPut_SrcFile
@blocks=();
unless(@tgds=grep $_,$cgi->param("tgd")){
    @tgds=("img/zzz");				## デホルトtargetDir
    cgihtmout(); exit;				## targetDirs無 exit
}

# @blk=(d1,f11..f1n) @blks(@blkのtab結合,同subDir..) @blocks(@blks,@blks..)
if ($ftpsvr) {						# ftp_proc_bgn
    use Net::FTP;
    $ftp=Net::FTP->new($ftpsvr); $ftp->login($usr,$pw); $ftp->cwd($path);
    for $targetdir(@tgds){
	undef @blks;
	push @blocks,&dird($targetdir);
    }
}
else{							# local_proc_bgn
    use File::Find;
    for $targetdir(@tgds){
	@blk=();					# @blk clear	
	find(\&ffindread,"../${targetdir}");		# rootUp_from_cbDir
	push(@blocks,join("\t",@blk)) if(@blk);		# @blk flush
    }
}
#-----------------------------------------
    sub dird($){		# 
	my ($arg,@blk);
	$arg=shift;
	push @blk,"${hmd_depth}/${arg}";
	for($ftp->dir($arg)){
	    my @tmp=split(' ',$_,9);				# ' 'は/\s+/相当
	    if($tmp[0]=~/^d/i){
	    	next if (($tmp[8]=~/^\.{1,2}/) || ($re && $tmp[8]=~/$re/)); # . .. excpt除外
	    	&dird("${arg}/$tmp[8]");			# dir再帰検索
	    }
#	    if($re && $tmp[0]=~/^d/i && $tmp[8]=~/$re/){ next }	# excpt dir
#	    if($tmp[8]=~/^\.{1,2}/){ next }			# . .. 除外
#	    elsif($tmp[0]=~/^d/i){ &dird("${arg}/$tmp[8]") }	# dir再帰検索
	    else{ push @blk,$tmp[8] }				# file挿入
	}
	push @blks,join("\t",@blk);
	return @blks;
    }
#-----------------------------------------
    sub ffindread{
	if(-d $_){						# dir (find内でchdir)
	    if(@blk){push(@blocks,join("\t",@blk)); @blk=();}	# @blk flush & clear
	    return if ($re && ${File::Find::name}=~/$re/);	# excpt dir
	    $baseDir=substr(${File::Find::name},3);		# baseDir変換cb→root、"../"除去
	    push(@blk,"${hmd_depth}/$baseDir");
	}
	else{push(@blk,$_) if @blk}				# file 該当dir時のみpush
    }
#-----------------------------------------
# @blocks=grep !/$re/,@blocks if $re; 						   # dir except
# @blocks=map{my @tmp=split("\t",$_);join("\t",shift @tmp,sort @tmp);} sort @blocks; # dir,file sort

$jvs=<<EOT;					# htmFile用全データ生成
<html><meta http-equiv=content-type content=charset=UTF-8><body>
<style type=text/css> span.box{width:80; white-space:-moz-pre-wrap;word-wrap:break-word;} </style>
<script type=text/javascript><!--
dspl="$dsp";
arg=\"\\
EOT
$jvs.=join("\\n",($hdr,@blocks))."\\\n\";\n";	# arg＆_tail( \改行";改行 )生成 #javascript改行escape\
$jvs.=join("",<DATA>);				# jvs_bottom生成

if ($ftpsvr){					# file_ftp_put
	open F0,">${ftpput}"; print F0 $jvs; close F0;
	$ftp->cwd($hmd);  $ftp->put($ftpput,$htmfile);	# ftpPut_Dst
	$ftp->quit;
}
else{						# file_local_create
	open F1,">../${hmd}/${htmfile}";	# cdDir_depth_rootup + homeDir + file
	print F1 $jvs;
	close F1;
}
cgihtmout();
#------------------------------------------
sub cgihtmout(){
print <<EOT;
@{[$cgi->header(-charset=>"utf-8")]}
<html><meta http-equiv=content-type content=charset=UTF-8>
$hdr<br>@{[$_=join("<br>",@blocks),$_=~s/\t/　/g]}<br>
Done <a href=# onClick=history.go(-1)>history.go(-1)</a>　　<a href=@{[ $ftpsvr ? "${htpsvr}${hmd}/${htmfile}" : "../${hmd}/${htmfile}" ]}>Show html</a>
<form action=$itself>$itself<input type=submit value=Gen> header<input type=text name=hdr value=@{[escapeHTML($hdr)]}>　dirListDisplay<input type=checkbox name=dsp value=checked $dsp><br>
homeD<input type=text name=hmd value=$hmd> fileN<input type=text name=fnm value=$htmfile><br>
targetD<input type=text name=tgd value=\"$tgds[0]\"> <input type=text name=tgd value=\"$tgds[1]\"> <input type=text name=tgd value=\"$tgds[2]\"> <br>
exceptD<input type=text name=exd value=\"$exds[0]\"> <input type=text name=exd value=\"$exds[1]\"> <input type=text name=exd value=\"$exds[2]\"><br>
RemtFtp<input type=text name=ftpsvr size=40 value=$ftpsvr0> Http<input type=text name=htpsvr size=30 value=$htpsvr> (/docRoot/)<br>
</form></html>
EOT
}
#------------------------------------------
=head
# revUpPlan(実行時arg表示tr/\t//、sp付dirの処理、wmaタグ＆画像、img自動縮小）
# SYNOPSIS: cb/imgdspl.cgi?hdr=title(tagOK)&dsp=checked&&hmd=hp/adl&fnm=imgdspl.htm&
  tgd=img/adl&tgd=..(複数)&exd=img/adl/av%exd=..(複数)&
  ftpsvr=ftp://usr:pw@ftp.com/public_html/&htpsvr=http://hoo.bar.com/hoge/
# Net::FTP $ftp->dir()の返値 ".",".."を含むdirs filesのリスト(順不同,不再帰)
# File::Find findの返値 (d1,f11..f1m)..(dn,fn1..fnm) 再帰、d1..dn、fn1..fnmは概ねsort済
# File::Find::name dirの場合、最終subdir名まで、find指定pathの場合最終は"."。
# find引数のpathは特定dir除外等のoption無し、全返値から必要時特定dirを無視除外する。
# cgi_var $jvs: @blocks: @tmpblk:  
# jvs_var arg: blocks[dir,files]: files[]:
# javascriptへの引数渡し header区切り：\n、blocks区切り:\n、files区切り:\t、区切り以外の末尾\t\n不可
# $arg="header\ndir1\tfl11\tfl12\t..fl19\ndir2\tfl21\t..."; javascript改行エスケープの行末\利用
# form input未入力でも@inp=$cgi->param("")でfield数分のカラ要素が渡される
# $re= "xx|"、""又はundefでは grep /$re/,() の全てにマッチ即ちgrep !/$re/ の出力が得られない
# 配列スライス書式は@ary[1,3,5]又は(リスト)[1,3,5]、又は((date)[1,3,5])
# undef@blks,@blks=(),my@blks=(),{defined my@blks},{my @blks;undef@blks}等々NG,{my undef@blks}はErr
# 文字列中の展開 ${tmp}[8]は${tmp}と"[8]"、$cgi->headerはHASH()値と"->header"
# 半角→全角UTF-8変換 tr/\t/\x{3000}/(全角spのUTF-8コード\x3000)、xrehbr cmdlのみscriptErr, print
#  `perl tmp.txt`では"Wide character in print"と表示でOK、imgdspl.cgiのresp表示\t→"0"となるがOKとす。
#  s/\t/　/g としないと xrehbr scriptErr、acfhgk 文字化け
# grep の条件式 ""と0 はtrue、form未入力分は@xxx=$cgi->param()に空文字列が渡る
# siteのads_javascriptの都合でjvscrptErrや＜center＞が残る場合がある
# dbg 空白含path名 real smnl img表示OK、span enl()のみ効かない、enl("path") win.open("+path+")でもNG???
=cut
__DATA__
blocks=arg.split("\n").sort();
header=blocks.slice(0,1);	blocks.shift();		// header抽出(未使用
real=["<pre>"];  smnl=[];  filnm=[];			// 実サイズ、サムネール、fileリスト
for(i in blocks){
	files=blocks[i].split("\t").sort();
	dir=files.slice(0,1);	files.shift();
	filnm.push("<br>" + dir + "<br>");
	dsep=dspl ? "<span class=box>" + dir + "</span> " : "：";	//dir区切り部
	real.push(dsep); smnl.push(dsep);
	for(j in files){
		path=dir + "/" + files[j];
		real.push("<img src=\"" + path + "\" title=" + path + "\" align=top>");
		smnl.push("<span onclick=enl(\"" + path + "\") title=\"" + path +
		 "\"><img src=\"" + path + "\" width=80 align=top hspace=2 vspace=2></span>");
		filnm.push(files[j] + "　");
	}
}
real.push("</pre>");
document.write( header,(dspl ? filnm.join("") : ""),"<br><br>",smnl.join(""),real.join(""));

function enl(url){					// anotherWindow生成img表示
	window.open(url,"dmyname","alwaysRaised,width=200,height=200,resizable");
	parent.opener.focus(); 
}
//--></script>
<p>　<p>　<p>　<p>　<p>　<p>　<p>　<p>----------------------------------------------------------<p>
</body></html>
