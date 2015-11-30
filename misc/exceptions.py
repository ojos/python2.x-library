# -*- coding: utf-8 -*-


class ResponseException(Exception):
    code = None
    message = None
    url = None
    header_code = True
    query = None
    data = None

    def __init__(self, code=None, message=None, url=None, header_code=None, query=None, data=None):
        self.code = self.code if code is None else code
        self.message = self.message if message is None else message
        self.url = self.url if url is None else url
        self.header_code = self.header_code if header_code is None else header_code
        self.query = self.query if query is None else query
        self.data = self.data if data is None else data

    def __str__(self):
        return 'code : %s, message : %s, url : %s, header_code : %s, query : %s, data : %s' %\
            (self.code, self.message, self.url, self.header_code, self.query, self.data)


class BaseException(ResponseException):
    code = 999
    message = 'ERROR'
    header_code = False


class BadRequestException(BaseException):
    code = 400
    message = 'BAD REQUEST'


class UnauthorizedException(BaseException):
    code = 401
    message = 'UNAUTHORIZED'


class PaymentRequiredException(BaseException):
    code = 402
    message = 'PAYMENT REQUIRED'


class ForbiddenException(BaseException):
    code = 403
    message = 'FORBIDDEN'


class NotFoundException(BaseException):
    code = 404
    message = 'NOT FOUND'


class MethodNotAllowedException(BaseException):
    code = 405
    message = 'METHOD NOT ALLOW'


class NotAcceptableException(BaseException):
    code = 406
    message = 'NOT ACCEPTABLE'


class ProxyAuthenticationRequiredException(BaseException):
    code = 407
    message = 'PROXY AUTHENTICATION REQUIRED'


class RequestTimeoutException(BaseException):
    code = 408
    message = 'REQUEST TIMEOUT'


class ConflictException(BaseException):
    code = 409
    message = 'CONFLICT'


class GoneException(BaseException):
    code = 410
    message = 'GONE'


class LengthRequiredException(BaseException):
    code = 411
    message = 'LENGTH REQUIRED'


class PreconditionFailedException(BaseException):
    code = 412
    message = 'PRECONDITION FAILED'


class RequestEntityTooLargeException(BaseException):
    code = 413
    message = 'REQUEST ENTITY TOO LARGE'


class RequestUriTooLongException(BaseException):
    code = 414
    message = 'REQUEST-URI TOO LONG'


class UnsupportedMediaTypeException(BaseException):
    code = 415
    message = 'UNSUPPORTED MEDIA TYPE'


class RequestedRangeNotSatisfiableException(BaseException):
    code = 416
    message = 'REQUESTED RANGE NOT SATISFIABLE'


class ExpectationFailedException(BaseException):
    code = 417
    message = 'EXPECTATION FAILED'


class InternalServerErrorException(BaseException):
    code = 500
    message = 'INTERNAL SERVER ERROR'


class NotImplementedException(BaseException):
    code = 501
    message = 'NOT IMPLEMENTED'


class BadGatewayException(BaseException):
    code = 502
    message = 'BAD GATEWAY'


class ServiceUnavailableException(BaseException):
    code = 503
    message = 'SERVICE UNAVAILABLE'


class GatewayTimeoutException(BaseException):
    code = 504
    message = 'GATEWAY TIMEOUT'

STATUS_CODES = {
    999: BaseException.message,
    400: BadRequestException.message,
    401: UnauthorizedException.message,
    402: PaymentRequiredException.message,
    403: ForbiddenException.message,
    404: NotFoundException.message,
    405: MethodNotAllowedException.message,
    406: NotAcceptableException.message,
    407: ProxyAuthenticationRequiredException.message,
    408: RequestTimeoutException.message,
    409: ConflictException.message,
    410: GoneException.message,
    411: LengthRequiredException.message,
    412: PreconditionFailedException.message,
    413: RequestEntityTooLargeException.message,
    414: RequestUriTooLongException.message,
    415: UnsupportedMediaTypeException.message,
    416: RequestedRangeNotSatisfiableException.message,
    417: ExpectationFailedException.message,
    500: InternalServerErrorException.message,
    501: NotImplementedException.message,
    502: BadGatewayException.message,
    503: ServiceUnavailableException.message,
    504: GatewayTimeoutException.message,
}


def status_message(code=None):
    if code:
        return STATUS_CODES[code]
    else:
        return STATUS_CODES[500]
