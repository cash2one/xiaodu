<?php 
	require_once("lib/mcpack.class.php");

	require_once("conf/Conf.php");
	@set_time_limit(0);
class SendMola{


	var $_fileInfo;
    public function getInfo ()
    {
        return $this->_fileInfo;
    }
	public function emptyInfo()
    {
		$this->_fileInfo["filesize"]=0;
		$this->_fileInfo["width"]=0;
		$this->_fileInfo["height"]=0;
		$this->_fileInfo["contsign"]=0;
    }

    public function check ($img_path)
    {
        
            $imageInfo = getimagesize($img_path);
            if ($imageInfo !== false) {
                $this->_fileInfo["width"] = $imageInfo[0];
                $this->_fileInfo["height"] = $imageInfo[1];
            } else {
                return false;
            }
        
        return true;
    }

	public function sendOneForMola($img_path)
    {
        $request = Array();
     //   $request['CONTENT_LENGTH'] = filesize($img_path);
        $file_content = file_get_contents($img_path);
        if ($file_content === false) {
            return false;
		}
		$this->_fileInfo["filesize"]=strlen($file_content);
		$request['CONTENT_LENGTH']=$this->_fileInfo["filesize"];
		$request['FILE'] = $file_content;
//-------------------------------------------------------------
//			echo $request['CONTENT_LENGTH'];
//			echo "-------";
//-------------------------------------------------------------
        $uploadPack = new MCPack();
        $response = $uploadPack->GetServiceData(MolaConfig::$PrecmIp, MolaConfig::$PrecmPort,$request);
        if ($response[0] != 0) {
            return false;
        }
        $this->_fileInfo["contsign"] = $response[2]["s1"] . "," .$response[2]["s2"];
        $ret =$this->_waitForUploadSuceeded($this->_fileInfo["contsign"]);
//-------------------------------------------------------------
		//echo $this->_fileInfo["contsign"];
//-------------------------------------------------------------
        return $ret;
    }
	private function _waitForUploadSuceeded($cont_sign)
    {
        $checkRes = false;
        for ($i = 0; $i < MolaConfig::$CheckUploadRetryTimes && !$checkRes; ++$i) {
			$imageUrl = sprintf(MolaConfig::$ImageUrl, $cont_sign);
            $checkRes = $this->_checkUrlAvailable($imageUrl, "image.baidu.com");
            usleep(MolaConfig::$CheckUploadIntervalInMS * 1000);
        } 
        return $checkRes;
    }
	private function _checkUrlAvailable($url, $referer) 
    {
        $refererLine = "Referer: " . $referer;
        $default_opts = array(
                'http' => array(
                        'method' => "GET",
                        'header' => $refererLine
                )
        );
        stream_context_get_default($default_opts);
        $header = get_headers($url);
        if (!isset($header[0])) {
            return false;
        }
        $httpStatusArr = explode(" ", $header[0]);
        if (!isset($httpStatusArr[1])) {
            return false;
        }
        $httpStatus = $httpStatusArr[1];
        if ($httpStatus == "200") {
            return true;
        }
        
        return false;
    }
    function getFileSize($url){
    $url = parse_url($url);
    if($fp = @fsockopen($url['host'],empty($url['port'])?80:$url['port'],$error)){
        fputs($fp,"GET ".(empty($url['path'])?'/':$url['path'])." HTTP/1.1\r\n");
        fputs($fp,"Host:$url[host]\r\n\r\n");
        while(!feof($fp)){
            $tmp = fgets($fp);
            if(trim($tmp) == ''){
                break;
            }else if(preg_match('/Content-Length:(.*)/si',$tmp,$arr)){
                return trim($arr[1]);
            }
        }
        return null;
    }else{
        return null;
    }
} 


}
?>
