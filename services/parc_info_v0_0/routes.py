from flask import request, abort
from flask_restx import Resource, fields
from core.utils import ApiNamespace


ns = ApiNamespace('parc-info', description="Gestion du parc informatique")
