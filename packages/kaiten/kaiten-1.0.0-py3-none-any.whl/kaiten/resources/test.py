# Push в тест
# python setup.py sdist bdist_wheel
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*


# Push в прод
# python setup.py sdist bdist_wheel
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*


class Test:
    def __init__(self, data):
        self.__dict__.update(data)

    def __getattr__(self, name):
        return self.__dict__[name]

class SubTest(Test):

    def __init__(self, client, card_id):
        self.api_url = 123
        super().__init__({"a":23, "b":34})


from kaiten.resources.ListOf import ListOf
if __name__ == '__main__':
    s = SubTest(123, 456)
    print(1)
    list_of_users = ListOf.users()
    print(list_of_users)