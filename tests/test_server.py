
"""
This module contains unit tests for the `server.py` file.

The tests use `pytest` and `unittest.mock` to test the functions in `server.py`.
The tests cover the `health_check` endpoint and the `get_puzzle_input` tool,
including success and error cases.

The tests are designed to be run with `pytest` and require the `pytest-asyncio`
plugin to handle the async functions.

The `get_puzzle_input` tool is tested by accessing the original function
through the `.fn` attribute of the `FunctionTool` object created by the
`@mcp.tool` decorator.

The `health_check` endpoint is tested by calling the async function directly.
"""
import os
from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import HTTPError, RequestException

from src.server import get_puzzle, get_puzzle_input_data, health_check


@pytest.fixture
def mock_env():
    """Mock the environment variables."""
    with patch.dict(os.environ, {"AOC_SESSION_COOKIE": "test_cookie"}):
        yield


@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint."""
    mock_request = MagicMock()
    response = await health_check(mock_request)
    assert response.status_code == 200
    assert response.body == b'{"status":"healthy","service":"aoc-utils"}'


@pytest.mark.asyncio
@patch("src.server.requests.get")
async def test_get_puzzle_input_success(mock_get, mock_env):
    """Test get_puzzle_input for a successful response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "puzzle input"
    mock_get.return_value = mock_response

    result = await get_puzzle_input_data.fn(2023, 1)
    assert result == {"result": "success", "content": "puzzle input"}
    mock_get.assert_called_once_with(
        "https://adventofcode.com/2023/day/1/input",
        cookies={"session": "test_cookie"},
        timeout=5,
    )

@pytest.mark.asyncio
async def test_get_puzzle_input_no_session_cookie():
    """Test get_puzzle_input when AOC_SESSION_COOKIE is not set."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(Exception) as excinfo:
            await get_puzzle_input_data.fn(2023, 1)
        assert "AOC_SESSION_COOKIE secret is not set" in str(excinfo.value)

@pytest.mark.asyncio
async def test_get_puzzle_input_missing_params():
    """Test get_puzzle_input with missing year or day."""
    with pytest.raises(ValueError, match=r"'year' and 'day' are required."):
        await get_puzzle_input_data.fn(None, 1)
    with pytest.raises(ValueError, match=r"'year' and 'day' are required."):
        await get_puzzle_input_data.fn(2023, None)

@pytest.mark.asyncio
@patch("src.server.requests.get")
async def test_get_puzzle_input_http_404_error(mock_get, mock_env):
    """Test get_puzzle_input for a 404 HTTP error."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
    mock_get.return_value = mock_response

    with pytest.raises(Exception) as excinfo:
        await get_puzzle_input_data.fn(2023, 1)
    assert "Puzzle input for 2023-12-1 not found" in str(excinfo.value)

@pytest.mark.asyncio
@patch("src.server.requests.get")
async def test_get_puzzle_input_other_http_error(mock_get, mock_env):
    """Test get_puzzle_input for other HTTP errors."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
    mock_get.return_value = mock_response

    with pytest.raises(Exception) as excinfo:
        await get_puzzle_input_data.fn(2023, 1)
    assert "HTTP Error" in str(excinfo.value)

@pytest.mark.asyncio
@patch("src.server.requests.get")
async def test_get_puzzle_input_request_exception(mock_get, mock_env):
    """Test get_puzzle_input for a request exception."""
    mock_get.side_effect = RequestException("Connection error")

    with pytest.raises(Exception) as excinfo:
        await get_puzzle_input_data.fn(2023, 1)
    assert "Failed to fetch data: Connection error" in str(excinfo.value)


@pytest.mark.asyncio
@patch("src.server.requests.get")
async def test_get_puzzle_success(mock_get, mock_env):
    """Test get_puzzle for a successful response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<h1>Puzzle Title</h1><p>Puzzle content.</p>"
    mock_get.return_value = mock_response

    result = await get_puzzle.fn(2023, 1)
    assert result == {"result": "success", "content": "<h1>Puzzle Title</h1><p>Puzzle content.</p>"}
    mock_get.assert_called_once_with(
        "https://adventofcode.com/2023/day/1",
        cookies={"session": "test_cookie"},
        timeout=5,
    )

@pytest.mark.asyncio
async def test_get_puzzle_no_session_cookie():
    """Test get_puzzle when AOC_SESSION_COOKIE is not set."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(Exception) as excinfo:
            await get_puzzle.fn(2023, 1)
        assert "AOC_SESSION_COOKIE secret is not set" in str(excinfo.value)

@pytest.mark.asyncio
async def test_get_puzzle_missing_params():
    """Test get_puzzle with missing year or day."""
    with pytest.raises(ValueError, match=r"'year' and 'day' are required."):
        await get_puzzle.fn(None, 1)
    with pytest.raises(ValueError, match=r"'year' and 'day' are required."):
        await get_puzzle.fn(2023, None)

@pytest.mark.asyncio
@patch("src.server.requests.get")
async def test_get_puzzle_http_404_error(mock_get, mock_env):
    """Test get_puzzle for a 404 HTTP error."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
    mock_get.return_value = mock_response

    with pytest.raises(Exception) as excinfo:
        await get_puzzle.fn(2023, 1)
    assert "Puzzle for 2023-12-1 not found. Is it released yet?" in str(excinfo.value)

@pytest.mark.asyncio
@patch("src.server.requests.get")
async def test_get_puzzle_other_http_error(mock_get, mock_env):
    """Test get_puzzle for other HTTP errors."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
    mock_get.return_value = mock_response

    with pytest.raises(Exception) as excinfo:
        await get_puzzle.fn(2023, 1)
    assert "HTTP Error" in str(excinfo.value)

@pytest.mark.asyncio
@patch("src.server.requests.get")
async def test_get_puzzle_request_exception(mock_get, mock_env):
    """Test get_puzzle for a request exception."""
    mock_get.side_effect = RequestException("Connection error")

    with pytest.raises(Exception) as excinfo:
        await get_puzzle.fn(2023, 1)
    assert "Failed to fetch data: Connection error" in str(excinfo.value)
