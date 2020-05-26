from transition_probabilities import TransitionProbabilities


def test_get_probability():
    transition_probabilities = TransitionProbabilities(lambda_value=4, max_cars=20, epsilon=0.1)
    assert transition_probabilities.start_index == 2
    assert transition_probabilities.end_index == 7


def test_get_probability_all_entries():
    transition_probabilities = TransitionProbabilities(lambda_value=4, max_cars=20, epsilon=0)
    assert transition_probabilities.start_index == 0
    assert transition_probabilities.end_index == 20


def test_get_probability_no_entries():
    transition_probabilities = TransitionProbabilities(lambda_value=4, max_cars=20, epsilon=1)
    assert transition_probabilities.start_index == 20
    assert transition_probabilities.end_index == 20
