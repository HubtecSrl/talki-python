"""`talki.documents`' hand-written methods for files (`upload`, `replace_file`,
`download`), against an `httpx.MockTransport`."""

import asyncio
import email.parser
import email.policy
import inspect
import io
import json

import httpx
import pytest

from talki import AsyncTalki, ConflictError, InvalidRequestError, Talki, _documents
from talki.api import documents as generated
from talki.models import (
    Document,
    DocumentAlso,
    DocumentCreate,
    DocumentFileReplace,
    DocumentStatus,
    DocumentUpload,
)
from talki.types import File

DOCUMENT = {
    "id": "3f6b1c9e-8d27-4a5f-b0e4-6c2d9a7f1e83",
    "location_id": "0b7d4e19-8a2c-4f61-9d3e-5c1a7b2f8e40",
    "title": "price-list.pdf",
    "source": "file",
    "mime_type": "application/pdf",
    "size_bytes": 8,
    "chunk_count": 0,
    "file_available": False,
    "status": "processing",
    "status_error": None,
    "enabled": True,
    "faq": False,
    "copy_group_id": None,
    "created_at": "2026-11-02T09:30:12Z",
    "updated_at": "2026-11-02T09:30:12Z",
}
FILE_PATH = f"/v1/documents/{DOCUMENT['id']}/file"
HAND_WRITTEN = ["download", "replace_file", "upload"]


def accepted() -> httpx.Response:
    return httpx.Response(202, json=DOCUMENT)


def envelope(status: int, type_: str, code: str, **headers: str) -> httpx.Response:
    return httpx.Response(
        status,
        json={"error": {"type": type_, "code": code, "message": "m", "request_id": "req_1"}},
        headers=headers,
    )


class Recorder:
    """The handler's answers in order, and every request it saw."""

    def __init__(self, *answers: httpx.Response) -> None:
        self.answers = list(answers)
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        request.read()
        self.requests.append(request)
        return self.answers.pop(0)


def sync_for(recorder: Recorder, **options) -> Talki:
    client = Talki(api_key="talki_test_x", transport=httpx.MockTransport(recorder), **options)
    client.transport._sleep = lambda delay: None
    return client


def async_for(recorder: Recorder) -> AsyncTalki:
    return AsyncTalki(api_key="talki_test_x", transport=httpx.MockTransport(recorder), max_retries=0)


def parts(request: httpx.Request) -> list[tuple[str, str | None, str, bytes]]:
    """Each part of a multipart request: its field name, file name, type and content."""
    head = f"Content-Type: {request.headers['Content-Type']}\r\n\r\n".encode()
    message = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(head + request.content)
    assert message.is_multipart()
    return [
        (
            part.get_param("name", header="content-disposition"),
            part.get_filename(),
            part.get_content_type(),
            part.get_payload(decode=True),
        )
        for part in message.iter_parts()
    ]


def public(resource: type) -> list[str]:
    return sorted(name for name in dir(resource) if not name.startswith("_") and name != "with_raw_response")


# The surface


def test_the_clients_expose_the_hand_written_classes():
    assert isinstance(Talki(api_key="talki_test_x").documents, _documents.DocumentsResource)
    assert isinstance(AsyncTalki(api_key="talki_test_x").documents, _documents.AsyncDocumentsResource)
    client = Talki(api_key="talki_test_x")
    assert isinstance(client.documents.with_raw_response, _documents.DocumentsResourceWithRawResponse)
    # A copy builds its own, on its own client.
    assert client.with_options(timeout=5).documents.with_raw_response._client is not client.client


def test_they_add_the_file_methods_to_the_generated_ones():
    for resource, base in (
        (_documents.DocumentsResource, generated.DocumentsResource),
        (_documents.AsyncDocumentsResource, generated.AsyncDocumentsResource),
    ):
        assert sorted(set(public(resource)) - set(public(base))) == HAND_WRITTEN


def test_the_raw_and_async_classes_mirror_them_signature_for_signature():
    sync = _documents.DocumentsResource
    for other, awaited in (
        (_documents.DocumentsResourceWithRawResponse, False),
        (_documents.AsyncDocumentsResource, True),
        (_documents.AsyncDocumentsResourceWithRawResponse, True),
    ):
        assert public(other) == public(sync)
        for name in HAND_WRITTEN:
            assert list(inspect.signature(getattr(other, name)).parameters) == list(
                inspect.signature(getattr(sync, name)).parameters
            ), name
            assert inspect.iscoroutinefunction(getattr(other, name)) == awaited


# Upload


def test_a_path_is_uploaded_as_its_file_with_its_name(tmp_path):
    path = tmp_path / "price-list.pdf"
    path.write_bytes(b"%PDF-1.7")
    recorder = Recorder(accepted())
    with sync_for(recorder) as client:
        document = client.documents.upload(
            str(path),
            location_id="0b7d4e19-8a2c-4f61-9d3e-5c1a7b2f8e40",
            location_ids=["l2", "l3"],
        )
    assert isinstance(document, Document) and document.status == DocumentStatus.PROCESSING
    (request,) = recorder.requests
    assert (request.method, request.url.path) == ("POST", "/v1/documents")
    assert request.url.params["location_id"] == "0b7d4e19-8a2c-4f61-9d3e-5c1a7b2f8e40"
    assert request.headers["Idempotency-Key"]
    assert request.headers["Content-Type"].startswith("multipart/form-data; boundary=")
    assert "boundary=+++" not in request.headers["Content-Type"]
    assert parts(request) == [
        ("file", "price-list.pdf", "application/pdf", b"%PDF-1.7"),
        ("location_ids", None, "text/plain", b"l2"),
        ("location_ids", None, "text/plain", b"l3"),
    ]


def test_no_other_locations_sends_no_field():
    recorder = Recorder(accepted())
    with sync_for(recorder) as client:
        client.documents.upload(b"a,b", filename="list.csv", location_ids=None)
    (request,) = recorder.requests
    assert [part[0] for part in parts(request)] == ["file"]


def test_bytes_need_a_name_and_take_a_type():
    recorder = Recorder(accepted())
    with sync_for(recorder) as client:
        with pytest.raises(ValueError, match="filename"):
            client.documents.upload(b"a,b\n1,2\n")
        assert recorder.requests == []
        client.documents.upload(b"a,b\n1,2\n", filename="prezzi.csv", content_type="text/csv")
    assert parts(recorder.requests[0]) == [("file", "prezzi.csv", "text/csv", b"a,b\n1,2\n")]


def test_an_open_file_and_a_file_carry_their_name_and_type():
    recorder = Recorder(accepted(), accepted())
    stream = io.BytesIO(b"plain text")
    stream.name = "/somewhere/else/notes.txt"
    with sync_for(recorder) as client:
        client.documents.upload(stream)
        client.documents.upload(File(payload=io.BytesIO(b"PK"), file_name="orari.docx", mime_type="application/x-mine"))
    assert parts(recorder.requests[0])[0][:2] == ("file", "notes.txt")
    assert parts(recorder.requests[1])[0] == ("file", "orari.docx", "application/x-mine", b"PK")


def test_a_file_opened_as_text_is_refused_before_sending():
    recorder = Recorder()
    with sync_for(recorder) as client:
        with pytest.raises(TypeError, match="binary"):
            client.documents.upload(io.StringIO("text"), filename="a.txt")
    assert recorder.requests == []


def test_an_upload_turned_away_unrun_is_sent_again_whole_with_the_same_key():
    recorder = Recorder(envelope(429, "rate_limit_error", "rate_limit_exceeded", **{"Retry-After": "1"}), accepted())
    with sync_for(recorder) as client:
        client.documents.upload(b"%PDF-1.7", filename="a.pdf")
    first, second = recorder.requests
    assert first.content == second.content and first.content
    assert first.headers["Idempotency-Key"] == second.headers["Idempotency-Key"]
    assert first.headers["Content-Type"] == second.headers["Content-Type"]


def test_an_upload_refused_raises_its_class():
    recorder = Recorder(envelope(415, "invalid_request", "unsupported_file_type"))
    with sync_for(recorder) as client:
        with pytest.raises(InvalidRequestError) as raised:
            client.documents.upload(b"MZ", filename="setup.exe")
    assert raised.value.code == "unsupported_file_type"


def test_the_raw_upload_has_the_headers():
    recorder = Recorder(httpx.Response(202, json=DOCUMENT, headers={"X-Request-Id": "req_9"}))
    with sync_for(recorder) as client:
        raw = client.documents.with_raw_response.upload(b"x", filename="a.txt")
    assert (raw.status_code, raw.request_id, raw.parse().id) == (202, "req_9", DOCUMENT["id"])


# Replace


def test_a_file_is_replaced_in_place():
    recorder = Recorder(accepted())
    with sync_for(recorder) as client:
        client.documents.replace_file(DOCUMENT["id"], b"%PDF-2", filename="price-list-2027.pdf", also="copies")
    (request,) = recorder.requests
    assert (request.method, request.url.path) == ("PUT", f"/v1/documents/{DOCUMENT['id']}")
    assert request.url.params["also"] == "copies"
    assert parts(request) == [("file", "price-list-2027.pdf", "application/pdf", b"%PDF-2")]


@pytest.mark.parametrize("also", ["copies", DocumentAlso.COPIES])
def test_replace_file_takes_also_as_the_string_or_the_enum(also):
    recorder = Recorder(accepted())
    with sync_for(recorder) as client:
        client.documents.replace_file(DOCUMENT["id"], b"%PDF-2", filename="a.pdf", also=also)
    (request,) = recorder.requests
    assert request.url.params["also"] == "copies"


def test_a_replacement_not_ready_raises_a_conflict():
    recorder = Recorder(envelope(409, "conflict", "document_not_ready"))
    with sync_for(recorder, max_retries=0) as client:
        with pytest.raises(ConflictError) as raised:
            client.documents.replace_file(DOCUMENT["id"], b"x", filename="a.pdf")
    assert raised.value.code == "document_not_ready"


def test_a_note_still_goes_as_json_through_the_generated_method():
    recorder = Recorder(accepted())
    with sync_for(recorder) as client:
        client.documents.create(body=DocumentCreate(title="Parking", body="Behind the salon."))
    (request,) = recorder.requests
    assert request.headers["Content-Type"] == "application/json"
    assert json.loads(request.content) == {"title": "Parking", "body": "Behind the salon.", "source": "text"}


# The generated methods, given a file


def test_a_file_through_the_generated_create_is_encoded_whole_and_retried():
    # Content holding the generator's fixed boundary still arrives intact.
    content = b"before\r\n--+++\r\nafter"
    recorder = Recorder(envelope(429, "rate_limit_error", "rate_limit_exceeded", **{"Retry-After": "1"}), accepted())
    with sync_for(recorder) as client:
        client.documents.create(
            body=DocumentUpload(file=File(payload=io.BytesIO(content), file_name="a.txt"), location_ids=["l2"])
        )
    first, second = recorder.requests
    assert first.content == second.content
    assert first.headers["Idempotency-Key"] == second.headers["Idempotency-Key"]
    assert "boundary=+++" not in first.headers["Content-Type"]
    assert parts(second) == [("file", "a.txt", "text/plain", content), ("location_ids", None, "text/plain", b"l2")]


def test_a_file_through_the_generated_replace_is_encoded_whole():
    recorder = Recorder(accepted())
    with sync_for(recorder) as client:
        client.documents.replace(
            DOCUMENT["id"], body=DocumentFileReplace(file=File(payload=io.BytesIO(b"%PDF-2"), file_name="b.pdf"))
        )
    (request,) = recorder.requests
    assert isinstance(request.stream, httpx.ByteStream)
    assert parts(request) == [("file", "b.pdf", "application/pdf", b"%PDF-2")]


def test_a_file_without_a_name_is_refused_before_sending():
    recorder = Recorder()
    with sync_for(recorder) as client:
        with pytest.raises(ValueError, match="file_name"):
            client.documents.create(body=DocumentUpload(file=File(payload=io.BytesIO(b"x"))))
    assert recorder.requests == []


# Download


def test_a_download_has_the_name_and_type_it_was_uploaded_with():
    answer = httpx.Response(
        200,
        content=b"a;b\n",
        headers={
            "Content-Type": "text/csv; charset=utf-8",
            "Content-Disposition": "attachment; filename=\"Listino citta.csv\"; filename*=UTF-8''Listino%20citt%C3%A0.csv",
        },
    )
    recorder = Recorder(answer)
    with sync_for(recorder) as client:
        file = client.documents.download(DOCUMENT["id"])
    assert recorder.requests[0].url.path == FILE_PATH
    assert (file.file_name, file.mime_type, file.payload.read()) == ("Listino città.csv", "text/csv", b"a;b\n")


def test_get_file_names_the_file_too():
    answer = httpx.Response(
        200,
        content=b"%PDF",
        headers={"Content-Type": "application/pdf", "Content-Disposition": 'attachment; filename="a.pdf"'},
    )
    recorder = Recorder(answer)
    with sync_for(recorder) as client:
        file = client.documents.get_file(DOCUMENT["id"])
    assert (file.file_name, file.mime_type, file.payload.read()) == ("a.pdf", "application/pdf", b"%PDF")


def test_the_raw_download_keeps_the_headers():
    recorder = Recorder(httpx.Response(200, content=b"%PDF", headers={"Content-Type": "application/pdf"}))
    with sync_for(recorder) as client:
        raw = client.documents.with_raw_response.download(DOCUMENT["id"])
    file = raw.parse()
    assert raw.headers["content-type"] == "application/pdf"
    assert (file.file_name, file.mime_type, file.payload.read()) == (None, "application/pdf", b"%PDF")


def test_a_document_without_a_file_raises_not_found():
    recorder = Recorder(envelope(404, "invalid_request", "resource_not_found"))
    with sync_for(recorder) as client:
        with pytest.raises(InvalidRequestError) as raised:
            client.documents.download(DOCUMENT["id"])
    assert raised.value.code == "resource_not_found"


@pytest.mark.parametrize(
    ("header", "name"),
    [
        ('attachment; filename="a.pdf"', "a.pdf"),
        ("attachment; filename=a.pdf", "a.pdf"),
        ('attachment; filename="say \\"hi\\".txt"', 'say "hi".txt'),
        ("attachment; filename*=UTF-8''%E2%82%AC.pdf; filename=\"EUR.pdf\"", "€.pdf"),
        ("attachment; filename*=iso-8859-1'it'caff%E8.txt", "caffè.txt"),
        # An extended name that does not decode falls back to the plain one.
        ("attachment; filename=\"fallback.pdf\"; filename*=UTF-8''%FF.pdf", "fallback.pdf"),
        # Never a directory, of either kind.
        ('attachment; filename="../../etc/passwd"', "passwd"),
        ("attachment; filename*=UTF-8''..%5C..%5Cboot.ini", "boot.ini"),
        ('attachment; filename=".."', None),
        ("attachment", None),
        ("", None),
    ],
)
def test_the_name_is_read_from_content_disposition(header, name):
    assert _documents.filename_of({"Content-Disposition": header}) == name


# Async


def test_the_async_methods_upload_replace_and_download(tmp_path):
    path = tmp_path / "orari.txt"
    path.write_bytes(b"Lun-Ven 9-19")
    recorder = Recorder(
        accepted(),
        accepted(),
        httpx.Response(
            200, content=b"Lun-Ven 9-19", headers={"Content-Disposition": 'attachment; filename="orari.txt"'}
        ),
    )

    async def run() -> File:
        async with async_for(recorder) as client:
            await client.documents.upload(path, location_ids=["l2"])
            await client.documents.replace_file(DOCUMENT["id"], path)
            return await client.documents.get_file(DOCUMENT["id"])

    file = asyncio.run(run())
    upload, replace, _ = recorder.requests
    assert parts(upload) == [
        ("file", "orari.txt", "text/plain", b"Lun-Ven 9-19"),
        ("location_ids", None, "text/plain", b"l2"),
    ]
    assert replace.method == "PUT" and parts(replace)[0][:2] == ("file", "orari.txt")
    assert (file.file_name, file.payload.read()) == ("orari.txt", b"Lun-Ven 9-19")
