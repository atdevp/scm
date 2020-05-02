
# GIT 
class GitWorkSpacePathNotFind(Exception):
    pass


class CloneError(Exception):
    pass


class PullError(Exception):
    pass


class CheckoutError(Exception):
    pass


class CommitError(Exception):
    pass

# MAVEN

class MvnParametersNotFind(Exception):
    pass


class MvnProjectNotFind(Exception):
    pass


class MvnModPathNotFind(Exception):
    pass


class MvnPomFileNotFind(Exception):
    pass


class MvnFinalNameFieldNotFind(Exception):
    pass


class MvnPackagingFieldNotFind(Exception):
    pass

# other

class GeneratePakcageCommandError(Exception):
    pass