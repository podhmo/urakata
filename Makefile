urakata.sqlite:
	@urakata initialize development.ini

season.json:
	@urakata scan development.ini demo/season > season.json
