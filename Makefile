urakata.sqlite:
	urakata initialize development.ini

season.json:
	urakata scan development.ini demo/season -overrides=demo/overrides.season.json > season.json

clean:
	rm urakata.sqlite season.json

register: season.json urakata.sqlite
	@urakata register development.ini season.json --debug

codegen: season.json urakata.sqlite
	@urakata codegen development.ini my-scaffold --debug

.PHONTY: clean register codegen
