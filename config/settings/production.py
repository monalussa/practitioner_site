from .base import *  # noqa: F401, F403

DEBUG = False

# Behind a PaaS TLS terminator (Render/Railway/Fly), Django only sees plain HTTP.
# Trust the proxy's forwarded-proto header so SECURE_SSL_REDIRECT doesn't loop.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Required by Django for admin/form POSTs over HTTPS on the deployed domain(s).
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
