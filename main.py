import datetime
import time
from typing import Optional, List

from fastapi import FastAPI, Request, Form
from starlette.templating import Jinja2Templates

from db import Database
from regiojet import RegioJet

app = FastAPI()
templates = Jinja2Templates(directory='templates')
regioJet = RegioJet()
database = Database()


def current_milli_time():
    return round(time.time() * 1000)


database.put_in_dummy()


@app.get('/api-search/')
def search(origin, destination, passengers: Optional[int] = 1, date_from=datetime.datetime.now(),
           date_to=datetime.datetime.now() + datetime.timedelta(days=7)):
    now = current_milli_time()
    if type(date_from) is str:
        date_from_string = datetime.datetime.strptime(date_from, "%Y-%m-%d").strftime("%Y-%m-%d")
    else:
        date_from_string = date_from.strftime("%Y-%m-%d")

    if type(date_to) is str:
        date_to_string = datetime.datetime.strptime(date_to, "%Y-%m-%d").strftime("%Y-%m-%d")
    else:
        date_to_string = date_to.strftime("%Y-%m-%d")
    result = regioJet.format_routes(
        regioJet.find_routes(date_from_string, date_to_string,
                             regioJet.find_city_id_by_name(origin, regioJet.find_locations()),
                             regioJet.find_city_id_by_name(destination, regioJet.find_locations()), origin, destination,
                             passengers))
    then = current_milli_time()
    return {
        'time_spent': then - now,
        'results': len(result),
        'data': result
    }


@app.get('/combinations/')
def combinations(source: str, destination: str, date=datetime.datetime.now()):
    now = current_milli_time()
    if type(date) is str:
        date_string = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    else:
        date_string = date.strftime("%Y-%m-%d")
    result = database.find_combinations(source, destination, date_string)
    then = current_milli_time()
    return {
        'time_spent': then - now,
        'results': len(result),
        'data': result
    }


@app.get('/')
def template_test(request: Request):
    return templates.TemplateResponse(
        'main.html',
        {'request': request}
    )


@app.post('/search')
def search(request: Request, origin: str = Form(None), destination: str = Form(None),
           from_date=Form(datetime.datetime.today()), to_date=Form(datetime.datetime.now() + datetime.timedelta(days=7))):
    regioJet.find_routes(from_date, to_date,
                         regioJet.find_city_id_by_name(origin, regioJet.find_locations()),
                         regioJet.find_city_id_by_name(destination, regioJet.find_locations()), origin, destination,
                         passengers=1)


@app.get('/whisperer')
def whisper(term: str) -> List[str]:
    return [name for name in regioJet.get_all_cities_names() if name.startswith(term)]
