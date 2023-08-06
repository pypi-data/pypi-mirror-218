class TapOrTargetError(RuntimeError):
    def __init__(self, message: str):
        super().__init__([message])
        self.message = message

    def __str__(self):
        return self.message


class TapError(TapOrTargetError):
    def __init__(self, message: str):
        super().__init__(message)

    @staticmethod
    def from_exception(e: Exception) -> "TapError":
        if isinstance(e, TapError):
            return e
        return TapError(f"Error in Cherre Tap: {str(e)}")


class TargetError(TapOrTargetError):
    def __init__(self, message: str):
        super().__init__(message)

    @staticmethod
    def from_exception(e: Exception) -> "TargetError":
        if isinstance(e, TargetError):
            return e
        return TargetError(f"Error in Cherre Target: {str(e)}")


class MissingTapConfigValueError(TapError):
    def __init__(
        self,
        key: str,
        tap_name: str,
        file: str = "",
    ):
        self.message = f"Error in Cherre Tap: Key {key} missing for tap {tap_name}"
        if file:
            self.message += f" from {file}"
        super().__init__(self.message)


class MissingTargetConfigValueError(TapError):
    def __init__(self, key: str, file: str, target_name: str):
        self.message = f"Error in Cherre Target: Key {key} missing from {file} for target {target_name}"
        super().__init__(self.message)
