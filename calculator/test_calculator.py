import numpy
import pytest
from calculator import validate, calculate_colour


sample_image_array = [[[105, 104, 200], [105, 104, 200]], [[105, 104, 200], [105, 104, 200]]]
sample_black_image = numpy.array([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]]])
sample_image = numpy.array(sample_image_array)
colour_test_data = [(sample_image, [200, 104, 105]),
                    (sample_black_image, [0, 0, 0])]
validate_test_data = [(('test.jpg', sample_image_array), ('test.jpg', sample_image_array, sample_image)),
                      (('test.jpg', []),(None, None, None)),
                      (('test.jpg', [0,0,0]),(None, None, None)),
                      ((0, sample_image_array),(None, None, None)),
                      (('', sample_image_array), (None, None, None))]


@pytest.mark.parametrize('test_input, expected', colour_test_data)
def test_calculate_colour(test_input, expected):
    assert calculate_colour(test_input) == expected


@pytest.mark.parametrize('test_input, expected', validate_test_data)
def test_validate(test_input, expected):
    result = validate(test_input)
    assert result[0] == expected[0]
    assert result[1] == expected[1]
    # workaround due to python's inability to compare numpy ndarrays
    comparison = result[2] == expected[2]
    if expected[2] is not None:
        assert comparison.all()
    else:
        assert comparison
