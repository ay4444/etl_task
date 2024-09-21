import pytest


@pytest.fixture
def input_value():
    input_value = {
                    "1990": {
                        "Winner": "teamA",
                        "Winner Num. of Wins": 20,
                        "Loser": "teamB",
                        "Loser Num. of Wins": 9
                    },
                    "2005": {
                        "Winner": "teamA",
                        "Winner Num. of Wins": 30,
                        "Loser": "teamC",
                        "Loser Num. of Wins": 11
                    },
                    "2010": {
                        "Winner": "teamF",
                        "Winner Num. of Wins": 35,
                        "Loser": "teamC",
                        "Loser Num. of Wins": 21
                    }
                    }
    
    return input_value

@pytest.fixture
def input_value_wl():
    return ["Boston Bruins", "1990", "44", "24", "0.55", "299",	"264", "35"]

@pytest.fixture
def input_value_wl2():
    return ["Boston Bruins", "1990", "20", "24", "0.55", "299",	"264", "35"]

@pytest.fixture
def output_val():
    output_val = {
                    "1990": {
                        "Winner": "Boston Bruins",
                        "Winner Num. of Wins": 44,
                        "Loser": "teamB",
                        "Loser Num. of Wins": 9
                    },
                    "2005": {
                        "Winner": "teamA",
                        "Winner Num. of Wins": 30,
                        "Loser": "teamC",
                        "Loser Num. of Wins": 11
                    },
                    "2010": {
                        "Winner": "teamF",
                        "Winner Num. of Wins": 35,
                        "Loser": "teamC",
                        "Loser Num. of Wins": 21
                    }
                    }
    return output_val