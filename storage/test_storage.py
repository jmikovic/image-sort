import numpy
import pytest
from storage import get_colour_name, validate


colour_test_data = [([0, 0, 0], 'black'),
                    ([255, 255, 255], 'white'),
                    ([255, 0, 255], 'magenta'),
                    ([154, 205, 50], 'yellowgreen'),
                    ([0, 0, 250], 'blue'),
                    ([100, 100, 100], 'dimgray')]

sample_image_array = [[[105, 104, 200], [105, 104, 200]], [[105, 104, 200], [105, 104, 200]]]
sample_image = numpy.array(sample_image_array)
validate_test_data = [(('test.jpg',sample_image_array,[255, 255, 255]),('test.jpg',sample_image,[255, 255, 255])),
                      (('test.jpg',[0, 0, 0], [155, 155, 155]),(None, None, None)),
                      ((0,sample_image_array, [0, 0, 0]),(None, None, None)),
                      (('test.jpg','',[0, 0, 0]),(None, None, None)),
                      (('test.jpg', sample_image_array, [300, 300, 300]),(None, None, None))]


@pytest.mark.parametrize('test_input, expected', colour_test_data)
def test_calculate_colour(test_input, expected):
    assert get_colour_name(test_input) == expected


@pytest.mark.parametrize('test_input, expected', validate_test_data)
def test_validate(test_input, expected):
    result = validate(test_input)
    assert result[0] == expected[0]
    assert result[2] == expected[2]
    # workaround due to python's inability to compare numpy ndarrays
    comparison = result[1] == expected[1]
    if expected[1] is not None:
        assert comparison.all()
    else:
        assert comparison
