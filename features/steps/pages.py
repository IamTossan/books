from behave import *
import requests

BASE_URL = "http://127.0.0.1:8000"

@when("I create a new page")
def step_impl(context):
    r = requests.post(f"{BASE_URL}/pages", json={"name": "test"})
    context.created_page_id = r.json()["id"]
    assert r.status_code == 200


@then("it is returned in the get route")
def step_impl(context):
    r = requests.get(f"{BASE_URL}/pages")
    page_ids = map(lambda x: x['id'], r.json())
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
    page_ids = map(lambda x: x['id'], r.json())
    for page_id in context.created_page_ids:
        assert page_id in page_ids
