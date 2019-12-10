AUTH_URL = "https://vafs.nus.edu.sg/adfs/oauth2/authorize"
CLIENT_ID = "E10493A3B1024F14BDC7D0D8B9F649E9-234390"
REDIRECT_URI = "https://luminus.nus.edu.sg/auth/callback"
RESOURCE = "sg_edu_nus_oauth"

OCP_SUBSCRIPTION_KEY = "6963c200ca9440de8fa1eede730d8f7e"
API_BASE_URL = "https://luminus.nus.edu.sg/v2/api/"

from enum import Enum, auto


class ErrorTypes(Enum):
    Error = auto()
    UnexpectedResponse = auto()
    NodeCodeInQuery = auto()
    FileExists = auto()
    InvalidCredentials = auto()
