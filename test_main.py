import pytest
from unittest.mock import patch
import main


def test_get_winners_losers_positiveTC(input_value_wl, input_value, output_val):
   with patch.object(main, 'yearwise_winner_loser_dict', input_value):
        assert main.get_winners_losers(input_value_wl) == output_val


def test_get_winners_losers_negativeTC(input_value_wl2, input_value, output_val):
   with patch.object(main, 'yearwise_winner_loser_dict', input_value):
        assert main.get_winners_losers(input_value_wl2) != output_val