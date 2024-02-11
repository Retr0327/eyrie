class RuntimeException(Exception):
    def __init__(self, msg: str = "", *args, **kwargs) -> None:
        self.msg = msg
        super().__init__(self.msg, *args, **kwargs)

    def what(self) -> str:
        return self.msg
