import os

from pqapi import (
    AnswerResponse,
    QueryRequest,
    UploadMetadata,
    agent_query,
    delete_bibliography,
    get_bibliography,
    upload_files,
)


def test_query_str():
    response = agent_query("default", "How are bispecific antibodies engineered?")
    assert isinstance(response, AnswerResponse)


def test_query_model():
    response = agent_query(
        "default",
        QueryRequest(query="How are bispecific antibodies engineered?"),
    )
    assert isinstance(response, AnswerResponse)


def test_delete_after():
    response = agent_query(
        "tmp",
        QueryRequest(query="How are bispecific antibodies engineered?"),
        delete_after=True,
    )
    assert isinstance(response, AnswerResponse)
    assert get_bibliography("tmp").doc_count == 0


def test_upload_files():
    script_dir = os.path.dirname(__file__)
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")
    response = upload_files(
        "default",
        [file],
        [UploadMetadata(filename="paper.pdf", citation="Test Citation")],
    )

    assert isinstance(response, list)
    assert len(response) == 1


def test_upload_public():
    # create a public bibliography
    script_dir = os.path.dirname(__file__)
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")
    response = upload_files(
        "api-test-public",
        [file],
        [UploadMetadata(filename="paper.pdf", citation="Test Citation")],
        public=True,
    )

    assert isinstance(response, list)
    assert len(response) == 1

    # get status of public bibliography
    status = get_bibliography("api-test-public", public=True)

    assert status.writeable is True
    assert status.doc_count == 1

    # delete public bibliography
    delete_bibliography("api-test-public", public=True)
