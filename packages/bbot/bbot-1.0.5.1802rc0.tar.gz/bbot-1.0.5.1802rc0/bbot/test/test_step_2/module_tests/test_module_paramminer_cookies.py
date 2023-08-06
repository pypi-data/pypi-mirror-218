from .test_module_paramminer_headers import *


class TestParamminer_Cookies(TestParamminer_Headers):
    modules_overrides = ["httpx", "paramminer_cookies"]
    config_overrides = {"modules": {"paramminer_cookies": {"wordlist": tempwordlist(["junkcookie", "admincookie"])}}}

    cookies_body = """
    <html>
    <title>the title</title>
    <body>
    <p>Hello null!</p>';
    </body>
    </html>
    """

    cookies_body_match = """
    <html>
    <title>the title</title>
    <body>
    <p>Hello AAAAAAAAAAAAAA!</p>';
    </body>
    </html>
    """

    async def setup_after_prep(self, module_test):
        module_test.scan.modules["paramminer_cookies"].rand_string = lambda *args, **kwargs: "AAAAAAAAAAAAAA"
        module_test.monkeypatch.setattr(
            helper.HttpCompare, "gen_cache_buster", lambda *args, **kwargs: {"AAAAAA": "1"}
        )
        expect_args = dict(headers={"Cookie": "admincookie=AAAAAAAAAAAAAA"})
        respond_args = {"response_data": self.cookies_body_match}
        module_test.set_expect_requests(expect_args=expect_args, respond_args=respond_args)

        respond_args = {"response_data": self.cookies_body}
        module_test.set_expect_requests(respond_args=respond_args)

    def check(self, module_test, events):
        assert any(
            e.type == "FINDING" and e.data["description"] == "[Paramminer] Cookie: [admincookie] Reasons: [body]"
            for e in events
        )
        assert not any(
            e.type == "FINDING" and e.data["description"] == "[Paramminer] Cookie: [junkcookie] Reasons: [body]"
            for e in events
        )
