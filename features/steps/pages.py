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


@given("I got {n} page(s) created")
def step_impl(context, n):
    context.created_page_ids = []
    for i in range(int(n)):
        r = requests.post(f"{BASE_URL}/pages", json={"name": "test"})
        context.created_page_ids.append(r.json()["id"])
        assert r.status_code == 200


@when("I publish a page")
def step_impl(context):
    r = requests.post(f"{BASE_URL}/pages/publish/{context.created_page_ids[-1]}")
    assert r.status_code == 200


@then("the page has a published state")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages/{context.created_page_ids[-1]}")
    assert r.json()["status"] == "PUBLISHED"


@when("I update the page")
def step_impl(context):
    r = requests.put(
        f"{BASE_URL}/pages/{context.created_page_ids[-1]}",
        json={"name": "updated test"},
    )
    assert r.status_code == 200


@then("the page is updated")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages/{context.created_page_ids[-1]}")
    assert r.json()["name"] == "updated test"


@then("a draft is created")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages/{context.created_page_ids[-1]}")
    assert r.json()["status"] == "DRAFT"
    assert r.json()["name"] == "updated test"
    assert r.json()["version"] == 2


@when("I make a comment on that page")
def step_impl(context):
    r = requests.post(
        f"{BASE_URL}/pages/comment/{context.created_page_ids[-1]}",
        json={"author": "test user", "comment": "test comment"},
    )
    assert r.status_code == 200


@then("the comment is created")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages/{context.created_page_ids[-1]}")
    assert r.json()["comments"] == [{"author": "test user", "comment": "test comment"}]


@given("I got {n} page(s) published")
def step_impl(context, n):
    context.created_page_ids = []
    for i in range(int(n)):
        r = requests.post(f"{BASE_URL}/pages", json={"name": "test"})
        context.created_page_ids.append(r.json()["id"])
        r = requests.post(f"{BASE_URL}/pages/publish/{context.created_page_ids[-1]}")
        assert r.status_code == 200


@when("I create a chapter with the pages")
def step_impl(context):
    r = requests.post(
        f"{BASE_URL}/chapters",
        json={"name": "test chapter", "pages": context.created_page_ids},
    )
    context.created_chapter_id = r.json()["id"]
    assert r.status_code == 200


@then("I have a chapter with pages")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/chapters/{context.created_chapter_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "test chapter"
    for i, page_id in enumerate(context.created_page_ids):
        r.json()["pages"][i]["id"] == page_id
