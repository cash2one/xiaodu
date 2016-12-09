<?php

/**
 * @file 
 * @brief 
 *
 * 对nshead的操作的PHP版本
 *
 * nshead C结构体:
 * typedef struct _nshead_t
 * {
 *   unsigned short id;              
 *   unsigned short version;         
 *   unsigned int   log_id;
 *   char           provider[16];
 *   unsigned int   magic_num;
 *   unsigned int   reserved;       
 *   unsigned int   body_len;
 * } nshead_t;
 *
**/
class NsHead
{
    /**
     * 创建nshead包
     *
     * 传入的是一个表示nshead数据的array
     *
     *  array(
     *       'id'        => 0,
     *       'version'   => 0,
     *       'log_id'    => 0,
     *       'provider'  => ""
     *       'magic_num' => 0xfb709394, #魔鬼数字, 这个外部不需要填写程序自动填充
     *       'reserved'  => 0,
     *       'body_len'  => 0
     *   );
     *
     * 
     *
     * 组装一个可以发送的nshead头数据包,不包括数据，数据在外部拼装
     *
     * @param $vars_arr 需要发送nshead头数据包,不包括数据
     * @return 返回一个可以发送的nshead头数据包,不包括数据，数据在外部拼装
     */
    public function build_nshead($vars_arr)
    {
        $nshead_arr = array(
            'id'        => 0,
            'version'   => 0,
            'log_id'    => 0,
            'provider'  => str_pad("", 16, "\0", STR_PAD_BOTH),
            'magic_num' => 0xfb709394, //魔鬼数字
            'reserved'  => 0,
            'body_len'  => 0,
        );
        foreach ($vars_arr as $key => $value)
        {
            if (isset($nshead_arr[$key]))
            {
                $nshead_arr[$key] = $value;
            }
        }
        $nshead  = "";
        $nshead  = pack("L*", (($nshead_arr['version'] << 16) + ($nshead_arr['id'])), $nshead_arr['log_id']);
        //最多取15个字节的provider
        $nshead .= str_pad(substr($nshead_arr['provider'], 0, 15), 16, "\0");
        $nshead .= pack("L*", $nshead_arr['magic_num'], $nshead_arr['reserved']);
        $nshead .= pack("L", $nshead_arr['body_len']);
        return $nshead;
    }
    
    /**
     * 解析nshead包，并将buf放入返回数组的buf字段中
     * 一般的nshead数据包都是 nshead + buf
     *
     * 返回一个nshead的array, 
     * 
     *  array(
     *       'id'        => 
     *       'version'   => 
     *       'log_id'    => 
     *       'provider'  => 
     *       'magic_num' =>
     *       'reserved'  => 
     *       'body_len'  => 
     *       'buf' =>
     *   );

     *
     * 其中'buf' 是表示实际的数据
     *
     * @param $head 接收到的nshead 数据包
     * @param $get_buf 需要解析出后续的数据，如果get_buf == false, 'buf'不存在
     * @param 返回一个nshead结果的array
     * @return $ret_arr array
     */
    public function split_nshead($head, $get_buf = true)
    {
        $ret_arr = array(
            'id'        => 0,
            'version'   => 0,
            'log_id'    => 0,
            'provider'  => "",
            'magic_num' => 0,
            'reserved'  => 0,
            'body_len'  => 0,
            'buf'       => "",
        );
        
        $ret = unpack("v1id/v1version/I1log_id", substr($head, 0, 8));
        if ($ret == false) {
            return false;
        }
        foreach ($ret as $key => $value)
        {
            $ret_arr[$key] = $value;
        }
        $ret_arr['provider'] = substr($head, 8, 16);
        $ret = unpack("I1magic_num/I1reserved/I1body_len", substr($head, 24, 12));
        if ($ret == false) {
            return false;
        }
        foreach ($ret as $key => $value)
        {
            $ret_arr[$key] = $value;
        }
        //36是nshead_t结构体大小
        if ($get_buf) {
            $ret_arr['buf'] = substr($head, 36, $ret_arr['body_len']);
        }
        return $ret_arr;
    }
    
    /**
     *  将 nshead 通过socket $msgsocket 发送出去
     *
     *  @param $msgsocket 需要写的socket
     *  @param $vars_arr 需要发送的nshead头
     *  @param $buf 需要发送的实际数据
     *  @return 发送的实际数据长度
     */
    public function nshead_write($msgsocket, $vars_arr, $buf)
    {
        $nshead = $this->build_nshead($vars_arr);
        if ($nshead == false) {
            return false;
        }
        $nshead .= $buf;
        return fwrite($msgsocket, $nshead, strlen($nshead));
    }
    
    /**
     * 由 socket $msgsocket 获取nshead数据包
     *
     * @param $msgsocket 需要接收的socket
     * @param $nshead_check_magicnum 是否检查MAGICNUM, 默认检查
     * @return 
     */
    public function nshead_read($msgsocket, $nshead_check_magicnum = true)
    {
        $temp_out = "";
        $this->socket_read_buf = "";
        //先读nshead头部
        $temp_out = fread($msgsocket, 36);
        if (strlen($temp_out) != 36)
        {
            error_log("read nshead error" );
            return false;
        }
        $nshead = $this->split_nshead($temp_out, false);
        //检查 msgic num
        if ($nshead_check_magicnum == true 
            && $nshead['magic_num'] != 0xfb709394 
            && $nshead['magic_num'] != -76508268) 
        //部分php版本在unpack的时候存在bug，所以这里再判断一下负数的情况
        {
            error_log("magic num mismatch: ret ".$nshead['magic_num']." want 0xfb709394");
            return false;
        }
        //读nshead的数据
        $left_bytes = $nshead['body_len'];
        while ($left_bytes > 0) {
            $recv_data = fread($msgsocket, $left_bytes);
            if ($recv_data == false) {
                error_log("recv buff error");
                return false;
            }
            $recv_size = strlen($recv_data);
            if ($recv_size > 0 && $recv_size <= $left_bytes) {
                $nshead['buf'] .= $recv_data;
                $left_bytes -= $recv_size;
            } else {
                error_log("recv buff error");
                return false;
            }
        }
        return $nshead;
    }
}

// mcpack 包装类
class MCPack 
{
    /**
     * @param
     * @return
     */
    public function __construct()
    {
    }
    /**
     * @param
     * @return
     */
    public function GetServiceData($strIP, $strPort, $arrParam)
    {
        $oNSHead = new NsHead();
        // 将参数转成 mcpack 字符串形式
        $arrParamString = array();
        foreach($arrParam AS $key => $value)
        {
            $arrParamString["$key"] = "$value";
        }
        $strSendMCPack = mc_pack_array2pack($arrParamString);
        // 将要发送的 nshead 
        $arrSendNSHead = array(
            'id' => 0,
            'log_id' => 1,
            'provider' => 'ui2ac',
            'body_len' => strlen($strSendMCPack),
        );

        // 打开套接字
        $hSocket = @fsockopen($strIP, $strPort, $iErrorNo, $strErrorMsg, 1);
        if($hSocket === false)
        {
            return array('-1', "failed to open[$strIP:$strPort]", array());
        }
        // 设置套接字读写超时
        stream_set_timeout($hSocket, 1, 5000);

        // 从网络上发送出去
        $iRet = $oNSHead->nshead_write($hSocket, $arrSendNSHead, $strSendMCPack);

        // 从网络上读取回来
        $arrRecvNSHeadPacket = $oNSHead->nshead_read($hSocket);    

        // nshead 合法性检测
        if(!is_array($arrRecvNSHeadPacket) || count($arrRecvNSHeadPacket) != 8 ||
            !array_key_exists('id', $arrRecvNSHeadPacket) ||
            !array_key_exists('version', $arrRecvNSHeadPacket) ||
            !array_key_exists('log_id', $arrRecvNSHeadPacket) ||
            !array_key_exists('provider', $arrRecvNSHeadPacket) ||
            !array_key_exists('magic_num', $arrRecvNSHeadPacket) ||
            !array_key_exists('reserved', $arrRecvNSHeadPacket) ||
            !array_key_exists('body_len', $arrRecvNSHeadPacket) ||
            !array_key_exists('buf', $arrRecvNSHeadPacket))
        {
            fclose($hSocket);
            $hSocket = null;

            return array('-2', "invalid pack read", array());
        }
        // 空的 mcpack 包
        if(intval($arrRecvNSHeadPacket['body_len']) <= 0 || 
            strlen($arrRecvNSHeadPacket['buf']) <= 0)
        {
            fclose($hSocket);
            $hSocket = null;
            
            return array('-3', 'empty mcpack received', array()); 
        }
            
        // 将 MCPack 从 buf里转出来
        $arrRecvMCPack = mc_pack_pack2array($arrRecvNSHeadPacket['buf']);
        if($arrRecvMCPack === false)
        {
            fclose($hSocket);
            $hSocket = null;
            return array('-4', 'mc_pack_pack2array error', array());
        }
        // all the fucking mcpack success, then return 

        // 关闭套接字
        if($hSocket !== null)
        {
            fclose($hSocket);
        }
        
        $iBodyLen = $arrRecvNSHeadPacket['body_len'];

        return array('0', 'success', $arrRecvMCPack);
    }
}
