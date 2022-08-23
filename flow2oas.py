#!/usr/bin/env python3

"""
This script converts a flow file to an OpenAPI Specification file.

Author: Fabio Rotondo <fabio.rotondo@gmail.com>

See:  https://editor.swagger.io/
"""

import argparse
import json
import os
import sys
import yaml

class Flow2OAS:
	flow = None
	oas = None

	def __init__(self ):
		self.oas = {}
		self.flow = {}

	def _init_oas ( self ):
		self.oas = {
			"openapi": "3.0.0",
			"info": {
				"title": "",
				"description": "",
				"version": "",
			},
			"paths": {},
			"components": {
				"schemas": {},
			},
			"tags": [],
		}

	def _parse ( self ):
		self._parse_info()
		self._parse_schemas()
		self._parse_paths()

		self._parse_tags ()

	def _parse_tags ( self ):
		tags = self.oas [ 'tags' ]

		tags.append ( {
			"name": self.flow [ 'name' ].lower(),
			"description": self.flow [ 'short_descr' ],
		} )

		self.oas [ 'tags' ] = tags


	def _parse_info ( self ):
		self.oas [ 'info' ] [ 'title' ] = self.flow [ 'name' ]
		self.oas [ 'info' ] [ 'description' ] = self.flow [ 'short_descr' ]

	def _parse_paths ( self ):
		for k, endpoint in self.flow [ 'endpoints' ].items ():
			self._parse_endpoint ( endpoint )

	def _parse_schemas ( self ):
		for k, schema in self.flow [ 'types' ].items ():
			self._create_schema ( schema [ 'name' ], schema [ 'fields' ] )

	def _parse_endpoint ( self, endpoint ):
		ep = self.oas [ 'paths' ].get ( endpoint [ 'url' ], {} )
		method_name = endpoint [ 'method' ].lower()
		schema_name = ( method_name + '_' + endpoint [ 'url' ] ).replace ( '/', '_' ).replace ( '__', '_' )
		meth = ep.get ( method_name, {} )

		meth [ 'summary' ] = endpoint [ 'short_descr' ]
		meth [ 'description' ] = endpoint [ 'description' ]
		meth [ 'operationId' ] = endpoint [ 'id' ]
		meth [ 'tags' ] = [ self.flow [ 'name' ].lower() ]
		meth [ 'requestBody' ] = {
			"content": {
				"application/json": {
					"schema": {
						"$ref": "#/components/schemas/" + schema_name,
					},
				},
			},
		}

		self._create_schema ( schema_name, endpoint [ 'parameters' ] )

		meth [ 'responses' ] = {
			"200": {
				"description": "Successful operation",
				"content": {
					"application/json": {
						"schema": {
							"$ref": "#/components/schemas/" + schema_name + '_response',
						},
					},
				},
			},
		}

		ep [ method_name ] = meth
		self.oas [ 'paths' ][ endpoint [ 'url' ] ] = ep

	def _create_schema ( self, schema_name, fields ):
		schema = {
			"type": "object",
			"properties": {}
		}
		for param in fields:
			schema [ 'properties' ][ param [ 'name' ] ] = {
				"type": self._map_type ( param [ "type" ] ),
				"description": param [ "description" ],
			}

		self.oas [ 'components' ][ 'schemas' ][ schema_name ] = schema
		self.oas [ 'components' ][ 'schemas' ][ schema_name + '_response' ] = schema

	def _map_type ( self, type_name ):
		if type_name in ( "string", "str" ):
			return "string"
		elif type_name in ( "integer", "int", "num", "float", "double" ):
			return "integer"
		elif type_name in ( "boolean", "bool" ):
			return "boolean"
		else:
			return "string"


	def convert_flow ( self, fname ):
		self._init_oas()
		self.flow = json.load( open( fname, "r" ) )

		self._parse()

		# convert to yaml
		return yaml.dump(
			self.oas,
			default_flow_style=False,
			sort_keys=False,
			indent=2,
		)


if __name__ == "__main__":
	parser = argparse.ArgumentParser( description='Convert a flow file to an OpenAPI Specification file.' )
	parser.add_argument( 'flow', help='Flow file to convert' )
	parser.add_argument( '-o', '--output', help='Output file name' )

	args = parser.parse_args()

	f2o = Flow2OAS()
	res = f2o.convert_flow( args.flow )

	if args.output:
		with open( args.output, "w" ) as f:
			f.write( res )
	else:
		print( res )
