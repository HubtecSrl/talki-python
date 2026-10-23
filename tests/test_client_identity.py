"""What `Talki` says about itself and where it finds its key: the version, the
`User-Agent`, `TALKI_API_KEY`, and the `talki` logger."""

import asyncio
import logging
import tomllib
from pathlib import Path

import httpx
import pytest

import talki
from talki import AsyncTalki, Talki
from talki.oauth import OAuthApp

ROOT = Path(__file__).resolve().parent.parent


class Recorder:
    def __init__(self, *answers: httpx.Response | Exception) -> None:
        self.answers = list(answers)
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        answer = self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]
        if isinstance(answer, Exception):
            raise answer
        return answer


def count(total: int = 7, **headers: str) -> httpx.Response:
    return httpx.Response(200, json={"total": total}, headers=headers)


def client_for(recorder: Recorder, **options) -> Talki:
    client = Talki(transport=httpx.MockTransport(recorder), **{"api_key": "talki_test_x", **options})
    client.transport._sleep = lambda delay: None
    return client


# Version and User-Agent


def test_the_version_is_the_one_released():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert talki.__version__ == pyproject["project"]["version"]


def test_every_request_says_which_client_sent_it():
    recorder = Recorder(count())
    with client_for(recorder) as client:
        client.calls.count()
    agent = recorder.requests[0].headers["User-Agent"]
    assert agent.startswith(f"talki-python/{talki.__version__} python/")
    assert f"httpx/{httpx.__version__}" in agent


def test_the_async_client_says_it_too():
    recorder = Recorder(count())

    async def run() -> None:
        async with AsyncTalki(api_key="talki_test_x", transport=httpx.MockTransport(recorder)) as client:
            await client.calls.count()

    asyncio.run(run())
    assert recorder.requests[0].headers["User-Agent"].startswith(f"talki-python/{talki.__version__} ")


def test_token_requests_say_it_too():
    request = OAuthApp("talki_cid_x", "talki_cs_x").token_request({"grant_type": "refresh_token"})
    assert request.headers["User-Agent"].startswith(f"talki-python/{talki.__version__} ")


# TALKI_API_KEY


def test_with_no_credential_the_key_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("TALKI_API_KEY", "talki_test_from_env")
    recorder = Recorder(count())
    with Talki(transport=httpx.MockTransport(recorder)) as client:
        client.calls.count()
    assert recorder.requests[0].headers["Authorization"] == "Bearer talki_test_from_env"
    assert AsyncTalki().client.token == "talki_test_from_env"


@pytest.mark.parametrize("given", [{"api_key": "talki_test_given"}, {"access_token": "talki_test_given"}])
def test_a_credential_passed_wins_over_the_environment(monkeypatch, given):
    monkeypatch.setenv("TALKI_API_KEY", "talki_test_from_env")
    assert Talki(**given).client.token == "talki_test_given"


@pytest.mark.parametrize("value", [None, "", "  "])
def test_no_credential_anywhere_says_where_to_put_one(monkeypatch, value):
    if value is None:
        monkeypatch.delenv("TALKI_API_KEY", raising=False)
    else:
        monkeypatch.setenv("TALKI_API_KEY", value)
    with pytest.raises(ValueError, match="TALKI_API_KEY"):
        Talki()


# Logging


def test_an_answer_is_logged_at_debug_without_its_query_or_headers(caplog):
    recorder = Recorder(httpx.Response(200, json={"data": [], "has_more": False, "next_cursor": None}))
    with caplog.at_level(logging.DEBUG, logger="talki"):
        with client_for(recorder) as client:
            client.calls.list(phone="+390000000001", q="Rossi")
    (record,) = [record for record in caplog.records if record.name == "talki._transport"]
    assert record.levelno == logging.DEBUG
    assert record.getMessage().startswith("GET /v1/calls: 200 in ")
    assert "0000000001" not in caplog.text and "Rossi" not in caplog.text
    assert "talki_test_x" not in caplog.text


def test_a_retry_is_logged_at_info_with_the_request_id(caplog):
    recorder = Recorder(httpx.Response(503, headers={"X-Request-Id": "req_1"}), count())
    with caplog.at_level(logging.INFO, logger="talki"):
        with client_for(recorder) as client:
            client.calls.count()
    messages = [record.getMessage() for record in caplog.records if record.name == "talki._transport"]
    assert len(messages) == 1
    assert messages[0].startswith("GET /v1/calls/count: 503, request req_1; retry 1 of 2 in ")


def test_a_connection_error_retried_and_then_given_up_on(caplog):
    recorder = Recorder(httpx.ConnectError("refused"))
    with caplog.at_level(logging.DEBUG, logger="talki"):
        with client_for(recorder, max_retries=1) as client:
            with pytest.raises(httpx.ConnectError):
                client.calls.count()
    messages = [record.getMessage() for record in caplog.records if record.name == "talki._transport"]
    assert messages[0].startswith("GET /v1/calls/count: ConnectError; retry 1 of 1 in ")
    assert messages[1].startswith("GET /v1/calls/count: ConnectError after ")


def test_nothing_is_logged_at_info_for_a_plain_answer(caplog):
    with caplog.at_level(logging.INFO, logger="talki"):
        with client_for(Recorder(count())) as client:
            client.calls.count()
    assert [record for record in caplog.records if record.name.startswith("talki")] == []
