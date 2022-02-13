from behave import *
import requests


@when("I create a new page")
def step_impl(context):
    r = requests.post("http://127.0.0.1:8000/pages", json={"name": "test"})
    context.created_page_id = r.json()["id"]
    assert r.status_code == 200


@then("it is returned in the get route")
def step_impl(context):
    r = requests.get("http://127.0.0.1:8000/pages")
    assert len(r.json()) == 1
    assert context.created_page_id == r.json()[0]["id"]

@when("I create a new page multiple times")
def step_impl(context):
    context.created_page_ids = []
    for i in range(10):
        r = requests.post("http://127.0.0.1:8000/pages", json={"name": "test"})
        context.created_page_ids.append(r.json()["id"])
        assert r.status_code == 200


@then("they are returned in the get route")
def step_impl(context):
    r = requests.get("http://127.0.0.1:8000/pages")
    def get_id(i):
        return i['id']
    page_ids = map(get_id, r.json())
    for page_id in context.created_page_ids:
        assert page_id in page_ids
