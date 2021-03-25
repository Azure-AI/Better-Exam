import functools
import simplejson as json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('exam', __name__, url_prefix='/exam')


@bp.route('init', methods=["POST"])
def init_exam():
    print(request.json)
    return json.dumps({"number": "1", "audio": "/static/index.html"})
