
class KeywordNotFound(Exception):
    def __init__(self, keyword):
        super(KeywordNotFound, self).__init__("Incorrect keyword: " + keyword)


class TypeRequestNotFound(Exception):
    pass


class URLNotFound(Exception):
    def __init__(self, url):
        super(URLNotFound, self).__init__("Incorrect URL Address: " + url)


class InvalidRelationalOperator(Exception):
    def __init__(self, keyword):
        super(InvalidRelationalOperator, self).__init__("Invalid relational operator: " + keyword)
