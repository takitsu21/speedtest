import unittest
import unittest.mock

import pytest
from pytest_mock import MockerFixture

from speedtest.core import speedtest


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


@unittest.mock.patch("speedtest.core.speedtest.client")
def test_download(mock_client, my_speedtest_object, mocker: MockerFixture):
    my_speedtest_object._download()
    mock_client.assert_called_once()
    mock_client.assert_called_with()
    mock_client.return_value.get.assert_called_once()
    mock_client.return_value.get.assert_called_with(f"{my_speedtest_object.url}/__down", params={"bytes": my_speedtest_object.download_size})

def test_update_progress(my_speedtest_object, mocker: MockerFixture):
    # Test the update progress method
    bar = mocker.MagicMock()
    my_speedtest_object._update_progress(10, 20, bar)
    bar.assert_called_once()
    bar.assert_called_with(10)
    assert bar.text == "Speed: 10.00 Mbps  | Jitter: 20.00 ms"

def test_data_blocks(my_speedtest_object):
    data_blocks = my_speedtest_object.data_blocks
    assert data_blocks == b"0" * my_speedtest_object.upload_size

@unittest.mock.patch("time.perf_counter")
@unittest.mock.patch("speedtest.core.speedtest.client")
def test_http_latency(mock_client, mock_perf_counter, my_speedtest_object):
    # Test the http latency method
    mock_perf_counter.side_effect = [1, 2]
    response = my_speedtest_object._http_latency("my_url")
    assert mock_perf_counter.call_count == 2
    assert mock_perf_counter.call_args_list == [unittest.mock.call(), unittest.mock.call()]
    mock_client.assert_called_once()
    mock_client.assert_called_with()
    mock_client.return_value.head.assert_called_once()
    mock_client.return_value.head.assert_called_with("my_url")
    assert response == 1000

    # Test the http latency method with kwargs
    mock_perf_counter.reset_mock()
    mock_client.reset_mock()
    mock_perf_counter.side_effect = [1, 2]
    response = my_speedtest_object._http_latency("my_url", params={"bytes": 0})
    assert mock_perf_counter.call_count == 2
    assert mock_perf_counter.call_args_list == [unittest.mock.call(), unittest.mock.call()]
    mock_client.assert_called_once()
    mock_client.assert_called_with()
    mock_client.return_value.head.assert_called_once()
    mock_client.return_value.head.assert_called_with("my_url", params={"bytes": 0})
    assert response == 1000

def test_download_latency(my_speedtest_object, mocker: MockerFixture):
    # Test the download latency property
    mocker.patch("speedtest.core.speedtest.SpeedTest._http_latency", return_value=1000)
    response = my_speedtest_object.download_latency
    assert response == 1000

def test_upload_latency(my_speedtest_object, mocker: MockerFixture):
    mocker.patch("speedtest.core.speedtest.SpeedTest._http_latency", return_value=1000)
    response = my_speedtest_object.upload_latency
    assert response == 1000

def test_ping(my_speedtest_object, mocker: MockerFixture):
    # Test the ping method with a Windows system
    mock_system = mocker.patch("platform.system", return_value="Windows")
    mock_shutil_ping = mocker.patch("shutil.which", return_value="ping")
    mock_subprocess = mocker.patch("subprocess.run", return_value=unittest.mock.Mock(returncode=0, stdout="Average = 100ms"))
    mock_urllib_parse = mocker.patch("urllib.parse.urlparse", return_value=unittest.mock.Mock(hostname="my_url"))
    mock_re_search = mocker.patch("re.search")
    mock_re_search.return_value.groups.return_value = ["100"]
    mock_rich_print = mocker.patch("rich.print")
    my_speedtest_object.ping()
    assert mock_system.call_count == 3
    assert mock_system.call_args_list == [unittest.mock.call(), unittest.mock.call(), unittest.mock.call()]
    mock_shutil_ping.assert_called_once()
    mock_shutil_ping.assert_called_with("ping")
    mock_urllib_parse.assert_called_once()
    mock_urllib_parse.assert_called_with("my_url")
    mock_subprocess.assert_called_once()
    mock_subprocess.assert_called_with(["ping", "-n", "3", "-w", "3", "my_url"], capture_output=True, text=True)
    mock_re_search.assert_called_once()
    mock_re_search.assert_called_with(r"Average = (\d+)ms", "Average = 100ms")
    assert mock_rich_print.call_count == 0


    # Test the ping method with a Linux system
    mocker.resetall()
    mock_system.return_value = "Linux"
    mock_shutil_ping.return_value = "/usr/bin/ping"
    my_speedtest_object.ping()
    assert mock_system.call_count == 3
    assert mock_system.call_args_list == [unittest.mock.call(), unittest.mock.call(), unittest.mock.call()]
    mock_shutil_ping.assert_called_once()
    mock_shutil_ping.assert_called_with("ping")
    mock_urllib_parse.assert_called_once()
    mock_urllib_parse.assert_called_with("my_url")
    mock_subprocess.assert_called_once()
    mock_subprocess.assert_called_with(["/usr/bin/ping", "-c", "3", "-W", "3", "my_url"], capture_output=True, text=True)
    mock_re_search.assert_called_once()
    mock_re_search.assert_called_with(r"time=(\d+\.?\d*) ms", "Average = 100ms")
    assert mock_rich_print.call_count == 0

    # Test the ping method with a Linux system and no latency
    mocker.resetall()
    mock_system.return_value = "Linux"
    mock_shutil_ping.return_value = "/usr/bin/ping"
    mock_re_search.return_value = None
    mock_subprocess.return_value.stdout = "Hostname not available"
    my_speedtest_object.ping()
    assert mock_system.call_count == 3
    assert mock_system.call_args_list == [unittest.mock.call(), unittest.mock.call(), unittest.mock.call()]
    mock_shutil_ping.assert_called_once()
    mock_shutil_ping.assert_called_with("ping")
    mock_urllib_parse.assert_called_once()
    mock_urllib_parse.assert_called_with("my_url")
    mock_subprocess.assert_called_once()
    mock_subprocess.assert_called_with(["/usr/bin/ping", "-c", "3", "-W", "3", "my_url"], capture_output=True, text=True)
    mock_re_search.assert_called_once()
    mock_rich_print.assert_called_once()
    mock_rich_print.assert_called_with("Ping successful, but unable to extract latency. => Hostname not available")

    # Test the ping method with a missing ping command
    mocker.resetall()
    mock_shutil_ping.side_effect = FileNotFoundError("Ping command not found")
    my_speedtest_object.ping()
    assert mock_system.call_count == 2
    assert mock_system.call_args_list == [unittest.mock.call(), unittest.mock.call()]
    mock_shutil_ping.assert_called_once()
    mock_shutil_ping.assert_called_with("ping")
    mock_rich_print.assert_called_once()
    mock_rich_print.assert_called_with("Ping command not found. Ensure it is available on your system.")
