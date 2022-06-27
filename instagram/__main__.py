from playwright.sync_api import sync_playwright
from pyvirtualdisplay import Display
import Instagram

display = Display(visible=0, size=(1920, 1080))
display.start()

p = sync_playwright().start()
browser = p.chromium.launch(headless=False, devtools=False)
ctx = browser.new_context(storage_state="insta.json")


perfil1 = Instagram.login(ctx, "username", "password")
