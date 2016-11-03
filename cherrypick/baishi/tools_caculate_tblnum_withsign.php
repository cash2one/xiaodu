<?php

$input=$argv[1];
$flag=$argv[2];
$signs=$input;

//sign64 -> sign1 sign2 tblNum
if($flag==1){
echo "signs:$signs \n";

$low=$signs>>32;
$high=$signs& 0xFFFFFFFF;
$tblNum=($low + $high) % 64 + 1;

echo "low:$low high:$high \n";
echo "tblNum:$tblNum \n";
echo "select * from tbl_video_$tblNum where play_link_sign64=\"$signs\";\n";

}else if($flag==2){
	//$sign = creat_sign_fs64($input);
	$sign = creat_sign_fs64($input);
        $sign64 = str_replace("-","0",$sign[2]);
	$tblNum =( ($sign[0] + $sign[1]) % 64 ) + 1;
	echo "sign1 ".$sign[0]." sign2 ".$sign[1]." sign64 ".$sign[2]." tblNum $tblNum\n";
	echo "select * from tbl_video_$tblNum where play_link_sign64=\"$sign64\";\n";

}else{
	echo "bad input: \n";
	var_dump($argv);
}


?>
