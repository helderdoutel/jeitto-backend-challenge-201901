import pytest
import main


def test_answer():
	retorno = main.convert_data(input_query={'_id':1})
	assert isinstance(retorno, str)