class BaseAutoGeneratingException(Exception): pass
class RepoException(BaseAutoGeneratingException): pass
class NoPatternException(BaseAutoGeneratingException): pass
class ServiceException(BaseAutoGeneratingException): pass
class ValidatorException(BaseAutoGeneratingException): pass
