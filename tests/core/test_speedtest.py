import unittest
import unittest.mock

import pytest
from pytest_mock import MockerFixture

from speedtest_cloudflare_cli.core import speedtest


@pytest.fixture
def my_speedtest_object(mocker: MockerFixture) -> speedtest.SpeedTest:
    mocker.patch("threading.Thread")
    my_speedtest = speedtest.SpeedTest("my_url", 1024, 1024, 3)
    return my_speedtest


@unittest.mock.patch("threading.Thread")
def test_init(mock_thread):
    # Test the initialization of the SpeedTest object
    my_speedtest = speedtest.SpeedTest("my_url", 1024, 1024, 3)
    mock_thread.assert_called_once()
    mock_thread.assert_called_with(target=my_speedtest.ping, daemon=True)
    mock_thread.return_value.start.assert_called_once()
    mock_thread.return_value.start.assert_called_with()
    assert my_speedtest.url == "my_url"
    assert my_speedtest.download_size == 1024
    assert my_speedtest.upload_size == 1024
    assert my_speedtest.attempts == 3
    assert my_speedtest.latency is None


def test_wait(my_speedtest_object, mocker: MockerFixture):
    # Test when the ping thread is alive
    my_speedtest_object._ping_thread.is_alive.return_value = True
    my_speedtest_object._wait()
    my_speedtest_object._ping_thread.is_alive.assert_called_once()
    my_speedtest_object._ping_thread.is_alive.assert_called_with()
    my_speedtest_object._ping_thread.join.assert_called_once()
    my_speedtest_object._ping_thread.join.assert_called_with()

    # Test when the ping thread is not alive
    mocker.resetall()
    my_speedtest_object._ping_thread.is_alive.return_value = False
    my_speedtest_object._wait()
    my_speedtest_object._ping_thread.is_alive.assert_called_once()
    my_speedtest_object._ping_thread.is_alive.assert_called_with()
    my_speedtest_object._ping_thread.join.assert_not_called()


# @unittest.mock.patch("speedtest_cloudflare_cli.core.speedtest.client")
# def test_download(mock_client, my_speedtest_object, mocker: MockerFixture):
#     my_speedtest_object._download()
#     mock_client.assert_called_once()
#     mock_client.assert_called_with()
#     mock_client.return_value.get.assert_called_once()
#     mock_client.return_value.get.assert_called_with(
#         f"{my_speedtest_object.url}/__down", params={"bytes": my_speedtest_object.download_size}
#     )


def test_upload_chunk(my_speedtest_object):
    from speedtest_cloudflare_cli.core.speedtest import CHUNK_SIZE

    upload_chunk = my_speedtest_object.upload_chunk
    assert upload_chunk == b"0" * CHUNK_SIZE


# @unittest.mock.patch("time.perf_counter")
# @unittest.mock.patch("speedtest_cloudflare_cli.core.speedtest.client")
# def test_http_latency(mock_client, mock_perf_counter, my_speedtest_object):
#     # Test the http latency method
#     mock_perf_counter.side_effect = [1, 2]
#     response = my_speedtest_object._http_latency("my_url")
#     assert mock_perf_counter.call_count == 2
#     assert mock_perf_counter.call_args_list == [unittest.mock.call(), unittest.mock.call()]
#     mock_client.assert_called_once()
#     mock_client.assert_called_with()
#     mock_client.return_value.head.assert_called_once()
#     mock_client.return_value.head.assert_called_with("my_url")
#     assert response == 1000

#     # Test the http latency method with kwargs
#     mock_perf_counter.reset_mock()
#     mock_client.reset_mock()
#     mock_perf_counter.side_effect = [1, 2]
#     response = my_speedtest_object._http_latency("my_url", params={"bytes": 0})
#     assert mock_perf_counter.call_count == 2
#     assert mock_perf_counter.call_args_list == [unittest.mock.call(), unittest.mock.call()]
#     mock_client.assert_called_once()
#     mock_client.assert_called_with()
#     mock_client.return_value.head.assert_called_once()
#     mock_client.return_value.head.assert_called_with("my_url", params={"bytes": 0})
#     assert response == 1000


# def test_ping(my_speedtest_object, mocker: MockerFixture):
#     # Test the ping method
#     mock_ping = mocker.patch("ping3.ping", return_value=20.0)
#     mock_rich = mocker.patch("rich.print")
#     my_speedtest_object.ping()
#     mock_ping.assert_called_once()
#     mock_ping.assert_called_with("google.com", unit="ms")
#     mock_rich.assert_not_called()
#     assert my_speedtest_object.latency == 20.0

#     # Test the ping method with None value
#     mocker.resetall()
#     mock_ping.return_value = None
#     my_speedtest_object.ping()
#     mock_ping.assert_called_once()
#     mock_ping.assert_called_with("google.com", unit="ms")
#     mock_rich.assert_not_called()
#     assert my_speedtest_object.latency == "N/A"

#     # Test the ping method with exception
#     mocker.resetall()
#     mock_ping.side_effect = ping3.errors.PingError("error")
#     my_speedtest_object.ping()
#     mock_ping.assert_called_once()
#     mock_ping.assert_called_with("google.com", unit="ms")
#     mock_rich.assert_called_once()
#     mock_rich.assert_called_with("Unable to ping the server. => error")
#     assert my_speedtest_object.latency == "N/A"
