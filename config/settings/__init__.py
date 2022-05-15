from decouple import config

ENVIRONMENT = config("ENVIRONMENT").lower()
if ENVIRONMENT == "local":
    from .local_settings import *  # noqa
elif ENVIRONMENT == "production":
    from .prod import *  # noqa
else:
    print("#####################################################")
    print("Invalid Environment: {}".format(ENVIRONMENT))
    print("#####################################################")
