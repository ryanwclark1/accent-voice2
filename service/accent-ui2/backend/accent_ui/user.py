from fastapi import Request


class UserUI:
    def __init__(self, token: str, uuid: str | None = None, session: dict | None = None):
        """
        Initializes a new User instance.

        Args:
            token (str): The user's token.
            uuid (str, optional): The user's UUID.
            session (dict, optional): The user's session data.
        """
        self.token = token
        self.uuid = uuid
        self._session = session or {"config": {}, "tenants": []}

    def get_id(self) -> str:
        """
        Returns the user's token.

        Returns:
            str: The user's token.
        """
        return self.token

    def get_user(self) -> dict | None:
        """
        Returns the user information from the session.

        Returns:
            dict | None: The user information if available, otherwise None.
        """
        return self._session.get("user")

    def get_user_tenant_uuid(self) -> str | None:
        """
        Returns the user's tenant UUID.

        Returns:
            str | None: The user's tenant UUID if available, otherwise None.
        """
        user = self.get_user()
        return user.get("tenant_uuid") if user else None

    def get_displayname(self) -> str | None:
        """
        Returns the user's display name.

        Returns:
            str | None: The user's display name if available, otherwise None.
        """
        user = self.get_user()
        return user.get("username") if user else None

    def get_tenant_uuid(self) -> str | None:
        """
        Returns the current working tenant UUID or the user's default tenant UUID.

        Returns:
            str | None: The tenant UUID if available, otherwise None.
        """
        if "working_tenant_uuid" in self._session:
            return self._session["working_tenant_uuid"]
        return self.get_user_tenant_uuid()

    def get_user_index_url(self, request: Request) -> str:
        """
        Returns the user's index URL.

        Args:
            request (Request): The request object.

        Returns:
            str: The user's index URL.
        """
        return request.url_for("accent_engine:user_index")  # Adjust the route name as needed

    def get_current_tenants(self) -> list:
        """
        Returns the list of tenants.

        Returns:
            list: The list of tenants.
        """
        return self._session.get("tenants", [])

    def reset(self):
        """
        Resets the user's session data.
        """
        self._session["config"] = {}
        self._session["tenants"] = []

    def get_config(self) -> dict:
        """
        Returns the user's configuration.

        Returns:
            dict: The user's configuration.
        """
        return self._session.get("config", {})

    def set_config(self, config: dict):
        """
        Sets the user's configuration.

        Args:
            config (dict): The configuration data to set.
        """
        self._session["config"] = {"websocketd": config.get("websocketd")}

    @property
    def is_active(self) -> bool:
        """
        Indicates whether the user is active.

        Returns:
            bool: True if the user is active, otherwise False.
        """
        return True

    @property
    def is_authenticated(self) -> bool:
        """
        Indicates whether the user is authenticated.

        Returns:
            bool: True if the user is authenticated, otherwise False.
        """
        return True

    @property
    def is_anonymous(self) -> bool:
        """
        Indicates whether the user is anonymous.

        Returns:
            bool: True if the user is anonymous, otherwise False.
        """
        return False
