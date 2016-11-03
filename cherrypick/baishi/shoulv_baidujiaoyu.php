<?php
require_once("shoulv_api.php");
class shoulu_baidujiaoyu extends shoulu_api {

	public $mapCategoryLevel1 = array(
		"工作"=>"职业培训",
		"生活"=>"实用教程",
	);
	public $mapCategoryLevel2 = array(
		"IT培训"=>"IT培训",
		"资格认证"=>"资格认证",
		"管理培训"=>"管理培训",
		"技能培训"=>"技能培训",
		"留学"=>"留学",
		"公开课"=>"公开课",
		"文体艺术"=>"文体艺术",
		"兴趣"=>"兴趣",
		"生活技能"=>"生活技能",
		"理财"=>"生活理财",
	);
	public $mapCategoryLevel3 = array(
		"英语培训"=>"英语培训",
		"公共英语"=>"公共英语",
		"英语口语"=>"英语口语",
		"商务英语"=>"商务英语",
		"托福(Toefl)"=>"托福",
		"雅思(IELTS)"=>"雅思",
		"CET"=>"CET",
		"SAT"=>"SAT",
		"少儿英语"=>"少儿英语",
		"职称英语"=>"职称英语",
		"成人英语"=>"成人英语",
		"alevel"=>"alevel",
		"其他"=>"其他",
		"韩语"=>"小语种",
		"小语种"=>"小语种",
		"日语"=>"日语",
		"韩语"=>"韩语",
		"其他"=>"其他",
		"IT培训"=>"IT培训",
		"计算机等级"=>"职称证书",
		"会计职称"=>"职称证书",
		"会计从业资格"=>"职称证书",
		"职称证书"=>"职称证书",
		"office"=>"电脑基础",
		"电脑基础"=>"电脑基础",
		"页面设计"=>"设计制作",
		"网络技术"=>"设计制作",
		"设计制作"=>"设计制作",
		"CAD"=>"设计制作",
		"UI"=>"设计制作",
		"PhotoShop"=>"设计制作",
		"FLASH"=>"设计制作",
		"平面设计"=>"设计制作",
		"网站建设"=>"编程开发",
		"PHP"=>"编程开发",
		"Linux"=>"编程开发",
		"Java"=>"编程开发",
		"IOS"=>"编程开发",
		"C/C++"=>"编程开发",
		"嵌入式培训"=>"编程开发",
		"编程开发"=>"编程开发",
		"数据库管理"=>"数据库管理",
		"公务员"=>"公务员",
		"咨询工程"=>"建筑工程",
		"建筑设计及装饰"=>"建筑工程",
		"安全工程师"=>"建筑工程",
		"建筑工程"=>"建筑工程",
		"CFA"=>"金融会计",
		"房产估价"=>"金融会计",
		"支出预算"=>"金融会计",
		"审计师"=>"金融会计",
		"注册税务师"=>"金融会计",
		"注册会计师"=>"金融会计",
		"acca"=>"金融会计",
		"会计证"=>"金融会计",
		"会计研究生"=>"金融会计",
		"会计实务"=>"金融会计",
		"金融会计"=>"金融会计",
		"护士"=>"医药培训",
		"口腔"=>"医药培训",
		"卫生资格"=>"医药培训",
		"临床助理"=>"医药培训",
		"临床"=>"医药培训",
		"医师"=>"医药培训",
		"医药培训"=>"医药培训",
		"国际贸易研究生"=>"贸易外贸",
		"贸易外贸"=>"贸易外贸",
		"人力资源师"=>"企业管理",
		"企业法律顾问"=>"企业管理",
		"企业管理"=>"企业管理",
		"公共营养师"=>"健康保健",
		"健康保健"=>"健康保健",
		"监理工程师"=>"职业资格",
		"质量工程师"=>"职业资格",
		"城市规划师"=>"职业资格",
		"''期货从业"=>"职业资格",
		"商务单证员"=>"职业资格",
		"银行从业"=>"职业资格",
		"职业资格"=>"职业资格",
		"管理培训"=>"管理培训",
		"项目管理"=>"管理通用",
		"管理技能"=>"管理通用",
		"战略管理"=>"管理通用",
		"管理通用"=>"管理通用",
		"市场营销"=>"企业运营",
		"人力资源"=>"企业运营",
		"企业运营"=>"企业运营",
		"电脑培训"=>"技能培训",
		"技能培训"=>"技能培训",
		"传媒"=>"媒体艺术",
		"影视制作"=>"媒体艺术",
		"影视设计"=>"媒体艺术",
		"媒体艺术"=>"媒体艺术",
		"二级建造师"=>"工程维修",
		"一级建造师"=>"工程维修",
		"专业维修"=>"工程维修",
		"工程维修"=>"工程维修",
		"实用技能"=>"实用技能",
		"求职"=>"创业求职",
		"创业求职"=>"创业求职",
		"考研辅导"=>"考研",
		"考研"=>"考研",
		"项目管理研究生"=>"项目管理研究生",
		"法律研究生"=>"法律研究生",
		"工程研究生"=>"工程研究生",
		"教育研究生"=>"教育研究生",
		"心理学研究生"=>"心理学研究生",
		"金融研究生"=>"金融研究生",
		"专科"=>"其他",
		"本科"=>"其他",
		"成考辅导"=>"其他",
		"MPA"=>"其他",
		"MBA"=>"其他",
		"人力资源研究生"=>"其他",
		"其他"=>"其他",
		"sat"=>"留学",
		"留学"=>"留学",
		"其他"=>"其他",
		"高中"=>"高中",
		"高一"=>"高一",
		"高二"=>"高二",
		"高三"=>"高三",
		"高考"=>"高考",
		"素质教育"=>"素质教育",
		"其他"=>"其他",
		"初中"=>"初中",
		"初一"=>"初一",
		"初二"=>"初二",
		"初三"=>"初三",
		"中考"=>"中考",
		"素质教育"=>"素质教育",
		"其他"=>"其他",
		"小学"=>"小学",
		"学前班"=>"学前班",
		"一年级"=>"一年级",
		"二年级"=>"二年级",
		"三年级"=>"三年级",
		"四年级"=>"四年级",
		"五年级"=>"五年级",
		"六年级"=>"六年级",
		"小升初"=>"小升初",
		"素质教育"=>"素质教育",
		"其他"=>"其他",
		"兴趣"=>"文体艺术",
		"文体艺术"=>"文体艺术",
		"乐器演奏"=>"声乐培训",
		"声乐培训"=>"声乐培训",
		"美工培训"=>"美术培训",
		"美术培训"=>"美术培训",
		"健身培训"=>"健身培训",
		"影视艺术"=>"影视艺术",
		"proe培训"=>"其他",
		"其他"=>"其他",
		"演讲与口才"=>"演讲与口才",
		"特殊技能"=>"特殊技能",
		"驾驶"=>"驾驶",
		"美食"=>"美食",
		"养生"=>"养生",
		"美容"=>"美容",
		"风水"=>"风水",
		"励志"=>"励志",
		"生活技能"=>"生活技能",
		"孕妇培训"=>"孕妇培训",
		"生存逃生"=>"生存逃生",
		"其他"=>"其他",
		"公开课"=>"公开课",
		"历史"=>"历史",
		"公共管理研究生"=>"公共管理研究生",
		"心理咨询师"=>"心理咨询师",
		"Android"=>"it培训",
		"it培训"=>"it培训",
		"游戏动漫"=>"it培训",
		"社会"=>"社会",
		"美容护肤"=>"美容护肤",
		"舞蹈培训"=>"舞蹈培训",
		"理财规划师"=>"生活理财",
		"证劵投资"=>"生活理财",
		"金融风险管理师"=>"生活理财",
	);

	public $apiFormat ="http://jiaoyu.baidu.com/platform/rs/shipinCourse/detail?url=";
	public $site ="jiaoyu.baidu.com";
	public $site_name ="百度教育";
	#public $fileInputUrls ="./data/urls_baidujiaoyu";
	public $fileInputUrls ="data/urls_jiaoyu.baidu.com";
	public $needRelLink = true;
	public $relItems ="albumStreams";
	public $needUrlEncode = true;
	public $hotRelLinkSigns = "0231677206174668258$$07413555981252672029$$7377255004481779085$$02615020107983407047$$1031808723220287101$$7625985938832952256$$7330799107188738798$$01591927338806027159$$1585924471885847059$$02320766705263870181$$04373092668851452626$$08395857596595809324$$4103537198894119099";
	public $useInnerUrl = true;
}

?>
