import usersettings

settings = usersettings.Settings("org.aleksis.apps.kort.client")
settings.add_setting("client_id", str, default="")
settings.add_setting("client_secret", str, default="")
settings.add_setting("base_url", str, default="")
settings.load_settings()
