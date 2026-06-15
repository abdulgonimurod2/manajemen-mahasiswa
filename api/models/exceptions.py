class AppException(Exception): pass
class ValidationError(AppException): pass
class DataNotFoundError(AppException): pass
class DuplicateNIMError(AppException): pass
class FileIOError(AppException): pass
class AuthenticationError(AppException): pass
