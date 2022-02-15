from behave import *
import requests

BASE_URL = "http://127.0.0.1:8000"


@given("the app is running")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200


@when("I create a new page")
def step_impl(context):
    r = requests.post(f"{BASE_URL}/pages", json={"name": "test"})
    context.created_page_id = r.json()["id"]
    assert r.status_code == 200


@then("it is returned in the get route")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages")
    page_ids = map(lambda x: x["id"], r.json())
    assert context.created_page_id in page_ids


@when("I create a new page multiple times")
def step_impl(context):
    context.created_page_ids = []
    for i in range(10):
        r = requests.post(f"{BASE_URL}/pages", json={"name": "test"})
        context.created_page_ids.append(r.json()["id"])
        assert r.status_code == 200


@then("they are returned in the get route")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages")
    page_ids = list(map(lambda x: x["id"], r.json()))
    for page_id in context.created_page_ids:
        assert page_id in page_ids


@given("I created a page")
def step_impl(context):
    r = requests.post(f"{BASE_URL}/pages", json={"name": "test"})
    context.created_page_id = r.json()["id"]
    assert r.status_code == 200


@when("I publish a page")
def step_impl(context):
    r = requests.post(f"{BASE_URL}/pages/publish/{context.created_page_id}")
    assert r.status_code == 200


@then("the page has a published state")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages/{context.created_page_id}")
    assert r.json()["status"] == "PUBLISHED"


@when("I update the page")
def step_impl(context):
    r = requests.put(
        f"{BASE_URL}/pages/{context.created_page_id}", json={"name": "updated test"}
    )
    assert r.status_code == 200


@then("the page is updated")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages/{context.created_page_id}")
    assert r.json()["name"] == "updated test"


@given("I published a page")
def step_impl(context):
    r = requests.post(f"{BASE_URL}/pages", json={"name": "test"})
    context.created_page_id = r.json()["id"]
    r = requests.post(f"{BASE_URL}/pages/publish/{context.created_page_id}")
    assert r.status_code == 200


@then("a draft is created")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages/{context.created_page_id}")
    assert r.json()["status"] == "DRAFT"
    assert r.json()["name"] == "updated test"
    assert r.json()["version"] == 2
