#!/usr/bin/python
# -*- coding:UTF-8

class WXCode(object):
    WX_OK = 0
    WX_ERR_EXCEPTION = 1
    WX_ERR_BUSY = -1
    WX_ERR_APPSECRET = 40001
    WX_ERR_TOKEN = 40002
    WX_ERR_OPENID = 40003
    WX_ERR_MEDIATYPE = 40004
    WX_ERR_FILETYPE = 40005
    WX_ERR_FILESIZE = 40006
    WX_ERR_MEDIAID = 40007
    WX_ERR_MSGTYPE = 40008
    WX_ERR_PICSIZE = 40009
    WX_ERR_VOICESIZE = 40010
    WX_ERR_VIDEOSIZE = 40011
    WX_ERR_THUMBNAILSIZE = 40012
    WX_ERR_APPID = 40013
    WX_ERR_TOKEN1 = 40014
    WX_ERR_MENU = 40015
    WX_ERR_BUTTON_SIZE = 40016
    WX_ERR_BUTTON_SIZE1 = 40017
    WX_ERR_BUTTON_LEN = 40018
    WX_ERR_BUTTON_KEY = 40019
    WX_ERR_BUTTON_URL = 40020
    WX_ERR_MENU_VER = 40021
    WX_ERR_MENU_LEVEL = 40022
    WX_ERR_MENU_NUM = 40023
    WX_ERR_MENU_TYPE = 40024
    WX_ERR_MENU_LEN = 40025
    WX_ERR_MENU_KEY = 40026
    WX_ERR_MENU_URL = 40027
    WX_ERR_MENU_USER = 40028
    WX_ERR_MENU_AUTH = 40029
    WX_ERR_REFRESHTOKEN = 40030
    WX_ERR_OID_LIST = 40031
    WX_ERR_OID_LIST_LEN = 40032
    WX_ERR_CFORMAT = 40033
    WX_ERR_PARAM = 40035
    WX_ERR_REQ_FORAMT = 40038
    WX_ERR_URL_LEN = 40039
    WX_ERR_GROUP = 40050
    WX_ERR_GROUP_NAME = 40051
    WX_LACK_TOKEN = 41001
    WX_LACK_APPID = 41002
    WX_LACK_REFRESHTOKEN = 41003
    WX_LACK_SECRET = 41004
    WX_LACK_MEDIA_DATA = 41005
    WX_LACK_MEDIA_ID = 41006
    WX_LACK_MENU_DATA = 41007
    WX_LACK_AUTH = 41008
    WX_LACK_OID = 41009
    WX_EXPIRE_TOKEN = 42001
    WX_EXPIRE_REFRESHTOKEN = 42002
    WX_EXPIRE_AUTH = 42003
    WX_NEED_GET = 43001
    WX_NEED_POST = 43002
    WX_NEED_HTTPS = 43003
    WX_NEED_USERLIKE = 43004
    WX_NEED_FRIENDS = 43005
    WX_EMPTY_MEDIA = 44001
    WX_EMPTY_POST_DATA = 44002
    WX_EMPTY_PIC = 44003
    WX_EMPTY_TEXT = 44004
    WX_LIMIT_MEDIA = 45001
    WX_LIMIT_TEXT = 45002
    WX_LIMIT_TITLE = 45003
    WX_LIMIT_FIELD = 45004
    WX_LIMIT_LINK = 45005
    WX_LIMIT_PIC_LINK = 45006
    WX_LIMIT_VOICE_TIME = 45007
    WX_LIMIT_PIC = 45008
    WX_LIMIT_API = 45009
    WX_LIMIT_MENU = 45010
    WX_LIMIT_TIME = 45015
    WX_LIMIT_GROUP = 45016
    WX_LIMIT_GROUP_LEN = 45017
    WX_LIMIT_GROUP_NUM = 45018
    WX_NO_MEDIA = 46001
    WX_NO_MENU_VER = 46002
    WX_NO_MENU_DATA = 46003
    WX_NO_USER = 46004
    WX_ERR_JSON = 47001
    WX_UNAUTH_API = 48001
    WX_UNAUTH_USER_API = 50001

WXErrInfo = {
    WXCode.WX_OK : 'ok',
    WXCode.WX_ERR_EXCEPTION : 'app exception',
    WXCode.WX_ERR_BUSY : 'wx system busy',
    WXCode.WX_ERR_APPSECRET : 'app_secret err or token invalid',
    WXCode.WX_ERR_TOKEN : 'token invald',
    WXCode.WX_ERR_OPENID : 'open_id invalid',
    WXCode.WX_ERR_MEDIATYPE : 'the type of media file is invalid',
    WXCode.WX_ERR_FILETYPE : 'the type of file is invalid',
    WXCode.WX_ERR_FILESIZE : 'the length of file is invalid',
    WXCode.WX_ERR_MEDIAID : 'the ID of media file is invalid',
    WXCode.WX_ERR_MSGTYPE : 'the type of msg is invalid',
    WXCode.WX_ERR_PICSIZE : 'the size of picture is invalid',
    WXCode.WX_ERR_VOICESIZE : 'the size of voice file is invalid',
    WXCode.WX_ERR_VIDEOSIZE : 'the size of video file is invalid',
    WXCode.WX_ERR_THUMBNAILSIZE : 'the size of thumbnail is invalid',
    WXCode.WX_ERR_APPID : 'the app_id is invalid',
    WXCode.WX_ERR_TOKEN1 : 'the token is invalid 1',
    WXCode.WX_ERR_MENU : 'the type of menu is invalid',
    WXCode.WX_ERR_BUTTON_SIZE : 'the number of button is invalid',
    WXCode.WX_ERR_BUTTON_SIZE1 : 'the number of button is invalid 1',
    WXCode.WX_ERR_BUTTON_LEN : 'the length of button name is invalid',
    WXCode.WX_ERR_BUTTON_KEY : 'the length of button key is invalid',
    WXCode.WX_ERR_BUTTON_URL : 'the length of button url is invalid',
    WXCode.WX_ERR_MENU_VER : 'the version of menu is invalid',
    WXCode.WX_ERR_MENU_LEVEL : 'the level of child-menu is invalid',
    WXCode.WX_ERR_MENU_NUM : 'the number of child=menu is invalid',
    WXCode.WX_ERR_MENU_TYPE : 'the type of menu is invalid',
    WXCode.WX_ERR_MENU_LEN : 'the length of child-menu name is invalid',
    WXCode.WX_ERR_MENU_KEY : 'the length of child-menu key is invalid',
    WXCode.WX_ERR_MENU_URL : 'the length of child-menu url is invalid',
    WXCode.WX_ERR_MENU_USER : 'the user of self-def menu is invalid',
    WXCode.WX_ERR_MENU_AUTH : 'oauth-code is invalid',
    WXCode.WX_ERR_REFRESHTOKEN : 'refresh token is invalid',
    WXCode.WX_ERR_OID_LIST : 'open-id list is invalid',
    WXCode.WX_ERR_OID_LIST_LEN : 'the length of open-id list is invalid',
    WXCode.WX_ERR_CFORMAT : 'the format of character is invalid',
    WXCode.WX_ERR_PARAM : 'the parameter is invalid',
    WXCode.WX_ERR_REQ_FORAMT : 'the format of request is invalid',
    WXCode.WX_ERR_URL_LEN : 'the length of url is invalid',
    WXCode.WX_ERR_GROUP : 'the open-id group is invalid',
    WXCode.WX_ERR_GROUP_NAME : 'the name of group is invalid',
    WXCode.WX_LACK_TOKEN : 'lack token',
    WXCode.WX_LACK_APPID : 'lack app-ip',
    WXCode.WX_LACK_REFRESHTOKEN : 'lack refresh token',
    WXCode.WX_LACK_SECRET : 'lack secret',
    WXCode.WX_LACK_MEDIA_DATA : 'lack media data',
    WXCode.WX_LACK_MEDIA_ID : 'lack media id',
    WXCode.WX_LACK_MENU_DATA : 'lack menu data',
    WXCode.WX_LACK_AUTH : 'lack oauth-code',
    WXCode.WX_LACK_OID : 'lack open-id',
    WXCode.WX_EXPIRE_TOKEN : 'token expired',
    WXCode.WX_EXPIRE_REFRESHTOKEN : 'refresh token expired',
    WXCode.WX_EXPIRE_AUTH : 'oauth-code expired',
    WXCode.WX_NEED_GET : 'need get request',
    WXCode.WX_NEED_POST : 'need post request',
    WXCode.WX_NEED_HTTPS : 'need https',
    WXCode.WX_NEED_USERLIKE : 'need user like',
    WXCode.WX_NEED_FRIENDS : 'need friend-relationship',
    WXCode.WX_EMPTY_MEDIA : 'media file is empty',
    WXCode.WX_EMPTY_POST_DATA : 'post data is empty',
    WXCode.WX_EMPTY_PIC : 'picture-text message is mepty',
    WXCode.WX_EMPTY_TEXT : 'text message is empty',
    WXCode.WX_LIMIT_MEDIA : 'the size of media file is exceed limit',
    WXCode.WX_LIMIT_TEXT : 'the size of msg is exceed limit',
    WXCode.WX_LIMIT_TITLE : 'the size of title is exceed limit',
    WXCode.WX_LIMIT_FIELD : 'the size of describe exceed limit',
    WXCode.WX_LIMIT_LINK : 'link limit',
    WXCode.WX_LIMIT_PIC_LINK : 'pic link limit',
    WXCode.WX_LIMIT_VOICE_TIME : 'voice time limit',
    WXCode.WX_LIMIT_PIC : 'pic limit',
    WXCode.WX_LIMIT_API : 'api limit',
    WXCode.WX_LIMIT_MENU : 'menu limit',
    WXCode.WX_LIMIT_TIME : 'time limit',
    WXCode.WX_LIMIT_GROUP : 'group limit',
    WXCode.WX_LIMIT_GROUP_LEN : 'the length of group limit',
    WXCode.WX_LIMIT_GROUP_NUM : 'the number of group limit',
    WXCode.WX_NO_MEDIA : 'not exist media',
    WXCode.WX_NO_MENU_VER : 'not exist menu version',
    WXCode.WX_NO_MENU_DATA : 'not exist menu data',
    WXCode.WX_NO_USER : 'not exist user',
    WXCode.WX_ERR_JSON : 'parse json/xml err',
    WXCode.WX_UNAUTH_API : 'un-auth api',
    WXCode.WX_UNAUTH_USER_API : 'un-auth user api',
}

class WXUrl(object):
    ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'
    MENU_PUT_URL = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s'
    MENU_GET_URL = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s'
    MENU_DEL_URL = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s'
    FOLLOWER_URL = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s'
    ACCESS_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'
    SERVICE_URL = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s'



if __name__ == '__main__':
    print WXErrInfo[0]

