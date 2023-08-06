import uuid

import pytest
import requests

import mantik.utils.mantik_api.client as mantik_api


@pytest.mark.parametrize(
    ("status_code", "expected"), [(201, None), (404, requests.HTTPError())]
)
def test_create_data_repository(
    mock_mantik_api_request,
    add_data_repository,
    info_caplog,
    status_code,
    expected,
):
    project_id = uuid.uuid4()
    data_repository_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/mantik-api/projects/{str(project_id)}/data",
        status_code=status_code,
        json_response={"dataRepositoryId": str(data_repository_id)},
        expected_error=expected,
    ) as error:
        mantik_api.create_data_repository(
            add_data_repository=add_data_repository,
            project_id=project_id,
            token="test_token",
        )
        assert info_caplog.messages[0] == (
            f"A new data repository with id: {data_repository_id} "
            f"and name: {add_data_repository.data_repository_name} at "
            f"{add_data_repository.uri} has been created"
        )
    if error:
        assert "Call to Mantik API" in info_caplog.messages[0]


@pytest.mark.parametrize(
    ("status_code", "expected"), [(204, None), (404, requests.HTTPError())]
)
def test_delete_data_repository(
    mock_mantik_api_request, info_caplog, status_code, expected
):
    project_id = uuid.uuid4()
    data_repository_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="DELETE",
        end_point=f"/mantik-api/projects/"
        f"{str(project_id)}/data/{str(data_repository_id)}",
        status_code=status_code,
        json_response={},
        expected_error=expected,
    ) as error:
        mantik_api.delete_data_repository(
            project_id=project_id,
            data_repository_id=data_repository_id,
            token="test_token",
        )
        assert info_caplog.messages[0] == (
            f"Data repository with id: {data_repository_id} has been deleted"
        )
    if error:
        assert "Call to Mantik API" in info_caplog.messages[0]


@pytest.mark.parametrize(
    ("status_code", "expected"), [(200, None), (404, requests.HTTPError())]
)
def test_get_data_repositories(
    mock_mantik_api_request, info_caplog, status_code, expected
):
    project_id = uuid.uuid4()
    name = "data_repo_name"
    with mock_mantik_api_request(
        method="GET",
        end_point=f"/mantik-api/projects/{str(project_id)}/data",
        status_code=status_code,
        json_response={
            "totalRecords": 1,
            "dataRepositories": [
                {
                    "dataRepositoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "dataRepositoryName": name,
                    "uri": "string",
                    "accessToken": "string",
                    "description": "string",
                    "labels": [
                        {
                            "labelId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "scope": "string",
                            "name": "string",
                            "value": "string",
                        }
                    ],
                }
            ],
        },
        expected_error=expected,
    ) as error:
        data_repositories = mantik_api.get_data_repositories(
            project_id=project_id, token="test_token"
        )
        assert data_repositories[0]["dataRepositoryName"] == name
    if error:
        assert "Call to Mantik API" in info_caplog.messages[0]
