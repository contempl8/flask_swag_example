#!/usr/bin/env python3

from flask import Flask, render_template, make_response, url_for, request
from flask_restx import Resource, Api, fields
import sys

print("Initializing")
def journal_print(*args,**kwargs):
    print(*args,**kwargs,file=sys.stderr)

def make_endpoints(ein_api):
    n_space = ein_api.namespace('NamenSpace', description='Das ist gut')
    home_name_space = ein_api.namespace('HomeSpace', description='This is Home')
    guten_model = ein_api.model('Ein Model',{
        'var0': fields.Integer(readonly=True, description='A read only variable of type Int'),
        'var1': fields.String(required=True, description='A read/write required variable of type String')
    })
    second_name_space = ein_api.namespace('SecondSpace', description='This is another namespace')

    lowest_fields = ein_api.model('Lower Values',
    {
        'val0': fields.Integer(),
        'spaces': fields.String(required=True),
        'unit4': fields.Boolean()
    })

    mid_fields = ein_api.model('Mid Values',
    {
        'mid0': fields.Nested(lowest_fields),
        'mid1': fields.Nested(lowest_fields)
    })

    outer_fields = ein_api.model('Outer Value',
    {
        'outer': fields.Nested(mid_fields)
    })
    @second_name_space.route('/')
    class Home_Space(Resource):
        def get(self):
            return make_response(render_template('second_index.html'))

    @second_name_space.route('/test')
    class Second_Name(Resource):
        '''Second NameSpace'''
        @second_name_space.expect(outer_fields)
        def put(self):
            data=ein_api.payload
            journal_print(data)
            return data
    @home_name_space.route('/')
    class Home_Space(Resource):
        def get(self):
            return make_response(render_template('index.html'))

    @home_name_space.route('/button_actions')
    class Button_Handler(Resource):
        @home_name_space.doc('Button Handler GET/PUT')
        def get(self):
            return "Button Handler GET"
        @home_name_space.expect(guten_model)
        @home_name_space.marshal_with(guten_model)
        def put(self):
            print(ein_api.payload)
            return request

    @n_space.route('/')
    class Endpoints0(Resource):
        '''An endpoint class providing get and PUT calls for the API'''

        @n_space.doc('Endpoint0 GET/PUT')
        def get(self):
            return "Endpoints0 GET"
        @n_space.doc('Endpoint0 GET/PUT')
        @n_space.expect(guten_model)
        @n_space.marshal_with(guten_model)
        def put(self):
            return ein_api.payload

def make_app():
    '''An app factory. Can be named create_app as well. Automatically detected by flask at start'''
    app = Flask(__name__)
    api = Api(app, version='1.0', title='TBD API',
                description='A breadcrumb API')
    make_endpoints(api)

    return app

