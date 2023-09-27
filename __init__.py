import asyncio
from typing import List

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import catch_everything_and_restart

db = Database("ext_pegging")

pegging_ext: APIRouter = APIRouter(prefix="/pegging", tags=["Pegging"])

pegging_static_files = [
    {
        "path": "/pegging/static",
        "name": "pegging_static",
    }
]

scheduled_tasks: List[asyncio.Task] = []

def pegging_renderer():
    return template_renderer(["pegging/templates"])


from .tasks import wait_for_paid_invoices, hedge_loop
from .views import *  # noqa
from .views_api import *  # noqa

def pegging_start():
    loop = asyncio.get_event_loop()
    task = loop.create_task(catch_everything_and_restart(wait_for_paid_invoices))
    task = loop.create_task(catch_everything_and_restart(hedge_loop))
    scheduled_tasks.append(task)
