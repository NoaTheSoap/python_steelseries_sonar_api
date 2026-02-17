class SonarError(Exception):
    """Base exception for all Sonar related errors."""
    pass

class CorePropsNotFoundError(SonarError):
    def __init__(self, path):
        super().__init__(f"coreProps.json not found at: {path}")

class SonarConnectionError(SonarError):
    def __init__(self, status_code):
        super().__init__(f"Could not connect to : {status_code}")

class SonarNotEnabled(SonarError):
    def __init__(self):
        super().__init__(f"Sonar is not enabled, please enable it in SteelSeries GG settings")

class SonarNotReady(SonarError):
    def __init__(self):
        super().__init__(f"Sonar is not ready")

class SonarNotRunning(SonarError):
    def __init__(self):
        super().__init__(f"Sonar is not running")

class SonarNotAccessible(SonarError):
    def __init__(self, status_code):
        super().__init__(f"Sonar is not accessible or received invalid values: {status_code}")

class InvalidChannel(SonarError):
    def __init__(self, channel):
        super().__init__(f"Invalid channel: {channel}")

class InvalidVolume(SonarError):
    def __init__(self, volume):
        super().__init__(f"Invalid volume, use value between 0 and 1: {volume}")