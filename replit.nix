# Replit configuration
# Automatically runs Python app

[deployment]
run = "python bloomberg_simple.py"

[env]
TELEGRAM_TOKEN = "8122220616:AAFI8xFd2O0X1UiJWBWvO8j5-pgeysLCbpc"
GEMINI_API_KEY = "AIzaSyAPYV-zu5bNVFcTeElaXYWokZEk_wlAWms"

[nix]
channel = "stable-22_11"

[nix.deps]
pkgs = ["python310Full", "python310Packages.pip"]
