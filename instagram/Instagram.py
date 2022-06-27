from playwright.sync_api import BrowserContext, Page
import utils
import os


class Insta:

    pages = list()

    def __init__(self, ctx, username):
        self.ctx = ctx
        self.username = username

    def get_user(self, username):
        page = self.ctx.new_page()
        self.pages.append(page)
        return User(page, username)

    def get_my(self):
        return self.get_user(self.username)


class User:

    _username: str
    _fullname: str
    _followers: list
    _following: list
    _is_friend = False
    _posts: list = list()

    def __init__(self, page: Page, username):
        self.page = page
        self._username = username
        os.makedirs(f"instagram/users/{self._username}", exist_ok=True)
        
        self.page.on("requestfinished", self._on_request_finished)
        self.page.goto(f"https://www.instagram.com/{username}/")
        page.locator("a[role=\"link\"]:has-text(\"Posts\")").click()

    def _on_request_finished(self, request):
        if 'web_profile_info/?username' in request.url:
            utils.process_profile(self, request)

    @property
    def username(self):
        return self._username

    @property
    def posts(self):
        return self._posts

    @property
    def followers(self):
        return self._followers

    @property
    def following(self):
        return self._following

    @property
    def fullname(self):
        return self._fullname

    @property
    def get_username(self):
        return self._username

    @property
    def is_friend(self):
        return self._is_friend

    def follow(self):
        pass

    def unfollow(self):
        pass

    def __str__(self):
        return f"{self._username} - {self._fullname}"

    def __del__(self):
        self.page.close()


def login(ctx: BrowserContext, username, password):

    if is_login(ctx):
        return Insta(ctx, username)

    page = ctx.new_page()
    page.goto("https://www.instagram.com/accounts/login/")
    page.type("input[name='username']", username)
    page.type("input[name='password']", password)
    page.click("button[type='submit']")
    page.wait_for_navigation()
    ctx.storage_state(path=f"sesiones/instagram_{username}.json")

    return Insta(ctx, username)


def is_login(ctx: BrowserContext):
    return True
