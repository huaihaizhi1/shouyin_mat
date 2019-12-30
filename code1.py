class ResponseCode(object):
    SUCCESS = 200  # 成功
    FAIL = 403  # 失败
    NO_RESOURCE_FOUND = 40001  # 未找到资源
    INVALID_PARAMETER = 40002  # 参数无效
    ACCOUNT_OR_PASS_WORD_ERR = 401  # 账户或密码错误
# 401: "未经授权",
#   403: "无权操作",
#   404: "接口未找到",
#   500: "服务器错误",
#   502: "网关错误",
#   503: "服务不可用",
#   504: "网关超时"
###ceshixiugai


class ResponseMessage(object):
    SUCCESS = "成功"
    FAIL = "失败"
    NO_RESOURCE_FOUND = "未找到资源"
    INVALID_PARAMETER = "参数无效"
    ACCOUNT_OR_PASS_WORD_ERR = "账户或密码错误"