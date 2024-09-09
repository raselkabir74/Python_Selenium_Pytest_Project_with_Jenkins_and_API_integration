import os
import time
import io
import redis

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

from configurations import configurations
from pages.index.index import DspDashboardIndex
from configurations import mysql
from configurations import generic_modules

debug_mode = "JENKINS_URL" not in os.environ


@pytest.fixture(scope='session')
def config():
    config = configurations.load_config_by_usertype()
    return config


@pytest.fixture(scope='session')
def setup():
    config = configurations.load_config_by_usertype()
    access_token, api_base_url, config = generic_modules.get_api_access_token(config['api']['oauth'],
                                                                              config['credential'])
    return access_token, api_base_url, config


@pytest.fixture(scope='session')
def redis_connection(config):
    max_retries = 20
    retries = 0

    if "qa-testing" in config['credential']['url']:
        redis_host = config['redis']['qa-host']
    else:
        redis_host = config['redis']['stage-host']
    while retries < max_retries:
        try:
            return redis.StrictRedis(redis_host, port=6379, decode_responses=True)
        except Exception as e:
            retries += 1
            if retries < max_retries:
                print(f"Failed to establish Redis connection. Retrying ({retries}/{max_retries})...")
                time.sleep(5)
            else:
                raise RuntimeError("Failed to establish Redis connection after multiple attempts." + str(e))

    raise RuntimeError("Failed to establish Redis connection.")


@pytest.fixture
def driver(config, request):
    attempts = 0
    driver = None

    while attempts < 10:
        try:
            # selenium_container_download_dir = "/home/seluser/downloads"
            download_dir = os.path.join(os.getcwd(), "downloads")

            c_options = Options()
            c_options.add_argument('--headless')
            c_options.add_argument('--no-sandbox')
            c_options.add_argument('--disable-gpu')
            c_options.add_argument('--disable-dev-shm-usage')
            c_options.add_argument("--window-size=1920,1080")
            c_options.add_argument('ignore-certificate-errors')
            c_options.add_argument('--disable-search-engine-choice-screen')
            c_options.add_experimental_option('prefs', {
                'download.default_directory': download_dir,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
                # 'profile.managed_default_content_settings.images': 2
            })

            driver = webdriver.Chrome(options=c_options)
            driver.implicitly_wait(int(config['wait']['implicit']))
            driver.set_page_load_timeout(1200000)

            # driver = webdriver.Chrome(options=c_options)
            # else:
            # driver = webdriver.Remote(
            #     command_executor="http://localhost:4444/wd/hub",
            #     options=c_options
            # )
            break
        except Exception as e:
            print(e)
            attempts += 1
            time.sleep(3)

    if driver is None:
        pytest.fail("Could not initialize driver after multiple attempts.")

    try:
        yield driver
    finally:
        # Teardown code
        screenshot_dir = os.path.join(os.getcwd(), "reports_screenshot")
        zip_folder_dir = os.path.join(os.getcwd(), "report-screenshot-zip")
        os.makedirs(screenshot_dir, exist_ok=True)
        os.makedirs(zip_folder_dir, exist_ok=True)

        if debug_mode:
            if request.session.testsfailed:
                screenshot_path = os.path.join(screenshot_dir, request.node.name + ".png")
                capture_full_page_screenshot(driver, screenshot_path)
        else:
            shot_attempts = 0
            while shot_attempts < 10:
                try:
                    screenshot_path = os.path.join(screenshot_dir, request.node.name + ".png")
                    capture_full_page_screenshot(driver, screenshot_path)
                    break
                except Exception as e:
                    print(f"Screenshot attempt {shot_attempts + 1} failed: {e}")
                    shot_attempts += 1
                    time.sleep(1)

        print('Exiting driver!')
        quit_attempts = 0
        while quit_attempts < 10:
            try:
                driver.execute_script("window.localStorage.clear();")
                driver.execute_script("window.sessionStorage.clear();")
                driver.delete_all_cookies()
                driver.quit()
                break
            except Exception as e:
                print(f"Quit attempt {quit_attempts + 1} failed: {e}")
                quit_attempts += 1
                time.sleep(1)


def capture_full_page_screenshot(driver, screenshot_path):
    total_width = driver.execute_script("return document.body.parentNode.scrollWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")

    # Set window size and scroll position
    driver.set_window_size(total_width, total_height)
    for y in range(0, total_height, 1000):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        time.sleep(0.2)

    # Take screenshot of the body element (avoids scrollbars)
    # body = driver.find_element(By.TAG_NAME, 'body')
    # body.screenshot(screenshot_path)

    # Capture the full page screenshot
    full_page_screenshot_bytes = driver.get_screenshot_as_png()
    full_page_screenshot = Image.open(io.BytesIO(full_page_screenshot_bytes))

    original_size = driver.get_window_size()
    driver.set_window_size(original_size['width'], original_size['height'])

    # Save the full-page screenshot
    with open(screenshot_path, "wb") as f:
        full_page_screenshot.save(f, format="PNG")


@pytest.fixture
def login_by_user_type(request, driver, redis_connection, env='stage'):
    marker = request.node.get_closest_marker("fixt_data")
    if marker is None:
        config = configurations.load_config_by_usertype()
    else:
        config = configurations.load_config_by_usertype(marker.args[0])
    index_page = DspDashboardIndex(config, driver, env)
    start = time.time()
    index_page.login()
    print('LOGGED IN: {}s'.format(int(time.time() - start)))
    return config, driver, redis_connection


@pytest.fixture(scope="session")
def open_database_connection():
    attempts = 0
    connection = None
    while attempts < generic_modules.MYSQL_MAX_RETRY:
        try:
            connection = mysql.get_mysql_client()
            connection_test = mysql.connection_test(connection)
            if connection_test:
                break
            else:
                attempts += 1
        except Exception as e:
            print("Error in DB Connection", e)
            attempts += 1
            time.sleep(2)
            continue
    if connection is not None:
        print("open connection")
    else:
        print("DB connection was not established")
    yield connection
    print("closing connection")
    connection.close()


@pytest.fixture(scope="session")
def open_audience_database_connection():
    attempts = 0
    connection = None
    while attempts < generic_modules.MYSQL_MAX_RETRY:
        try:
            connection = mysql.get_mysql_client_for_audiences_db()
            connection_test = mysql.connection_test(connection)
            if connection_test:
                break
            else:
                attempts += 1
        except Exception as e:
            print("Error in Audience DB Connection", e)
            attempts += 1
            time.sleep(2)
            continue
    if connection is not None:
        print("open audience connection")
    else:
        print("Audience DB connection was not established")
    yield connection
    print("closing audience connection")
    connection.close()
