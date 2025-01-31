# Necessary packages

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.base import BaseEstimator
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from tqdm import tqdm
from time import time
from typing import Any, Callable, Dict, List, Set, Tuple, Union
import numpy as np

try:
    from DataLab.GAIN.utils import binary_sampler
except ModuleNotFoundError:
    from DataLab.GAIN.utils import binary_sampler

from typing import Dict, List


DATASETS: Dict[str, Dict[str, Any]] = {

**{ # outlier-removed datasets
        f"{year}.{country}.urban": {
            "name": f"{year} {country} data",
            "url": "",
            "header": [0],
            "drop_cols": ["year", "country", "admin1", "admin2","hhid", "hhweight"], #climatezone
            "categorical_vars": {
                "head_literate": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "head_male": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "elec_any": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "fridge": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "tv": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "music": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "scooter": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "car": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "publictransport": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "washmach": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
            },
            "target": "elec_cons",
            "scaler": {
                "class": MinMaxScaler,
                "feature_range": (-1, 1),
            },
            "model": {
                "class": HistGradientBoostingRegressor,
                "kwargs": {
                    "max_iter": 3000,
                    "max_depth": 5,
                },
            }

        }
        for year, country in [

        [2002, 'BRA'],
        [2004, 'IND'],
        [2005, 'GHA'],
        [2008, 'BRA'],
        [2010, 'MNG'],
        [2010, 'VNM'],
        [2011, 'IND'],
        [2014, 'GTM'],
        [2014, 'KHM'],
        [2017, 'BRA'],
        [2017, 'GHA'],
        [2018, 'ARM'],
        [2018, 'ETH'],
        [2018, 'NGA'],
        [2019, 'KHM'],
        [2019, 'NPL'],
        [2019, 'UGA'],
        [2020, 'MEX'],
        [2020, 'RUS'],
        [2020, 'VNM'],
        [2021, 'MNG'],
        [2014, 'ZAF']
        ]
    },
**{ # outlier-removed datasets
        f"{year}.{country}.rural": {
            "name": f"{year} {country} data",
            "url": "",
            "header": [0],
            "drop_cols": ["year", "country", "hhid", "hhweight"], #climatezone
            "categorical_vars": {
                "head_literate": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "head_male": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "elec_any": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "fridge": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "tv": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "music": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "scooter": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "car": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "publictransport": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
                "washmach": {
                    "class": LabelEncoder,
                    "kwargs": {},
                },
            },
            "target": "elec_cons",
            "scaler": {
                "class": MinMaxScaler,
                "feature_range": (-1, 1),
            },
            "model": {
                "class": HistGradientBoostingRegressor,
                "kwargs": {
                    "max_iter": 3000,
                    "max_depth": 5,
                },
            }

        }
        for year, country in [

        [2002, 'BRA'],
        [2004, 'IND'],
        [2005, 'GHA'],
        [2008, 'BRA'],
        [2010, 'MNG'],
        [2011, 'IND'],
        [2010, 'VNM'],
        [2014, 'GTM'],
        [2014, 'KHM'],
        [2017, 'BRA'],
        [2017, 'GHA'],
        [2018, 'ARM'],
        [2018, 'ETH'],
        [2018, 'NGA'],
        [2019, 'KHM'],
        [2019, 'NPL'],
        [2019, 'UGA'],
        [2020, 'MEX'],
        [2020, 'RUS'],
        [2020, 'VNM'],
        [2021, 'MNG'],
        [2014, 'ZAF']
        ]
    },
            **{
                f"{country}{year}_subset1": {
                    "name": f"{country} {year} data round 1",
                    "url": "",
                    "header": [0],
                    "drop_cols": ["year", "country", "hhid", "hhweight"],
                    "categorical_vars": {
                        "head_literate": {
                            "class": LabelEncoder,
                            "kwargs": {},
                        },

                        "fridge": {
                            "class": LabelEncoder,
                            "kwargs": {},
                        },
                        "tv": {
                            "class": LabelEncoder,
                            "kwargs": {},
                        },
                        "music": {
                            "class": LabelEncoder,
                            "kwargs": {},
                        },


                    },
                    "target": "exp",
                    "scaler": {
                        "class": MinMaxScaler,
                        "feature_range": (-1, 1),
                    },
                    "model": {
                        "class": HistGradientBoostingRegressor,
                        "kwargs": {
                            "max_iter": 3000,
                            "max_depth": 5,
                        },
                    },

                }
        for country, year in [
            ['ARM', 2018],
            ['BRA', 2002],
            ['BRA', 2008],
            ['BRA', 2017],
            ['ETH', 2018],
            ['GHA', 2005],
            ['GHA', 2017],
            ['GTM', 2014],
            ['IND', 2004],
        ]
    },
    'ARM2018_subset4_eval': {
        "name": "evaluation data round 4",
        "url": "",
        "header": [0],
        "drop_cols": [ "year","country","hhid","hhweight", "climatezone"],  # columns to drop
        "categorical_vars": {  # categorical variables that need to be encoded
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "elec_cons",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    'GHA2017_subset4_eval': {
        "name": "evaluation data round 4",
        "url": "",
        "header": [0],
        "drop_cols": [ "year","country","hhid","hhweight", "climatezone"],  # columns to drop
        "categorical_vars": {  # categorical variables that need to be encoded
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "elec_cons",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    'ETH2018_subset4_eval': {
        "name": "evaluation data round 4",
        "url": "",
        "header": [0],
        "drop_cols": [ "year","country","hhid","hhweight", "climatezone"],  # columns to drop
        "categorical_vars": {  # categorical variables that need to be encoded
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "elec_cons",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    'GHA2017_subset4_noNA': {
        "name": "evaluation data round 4",
        "url": "",
        "header": [0],
        "drop_cols": [ "year","country","hhid","hhweight", "climatezone"],  # columns to drop
        "categorical_vars": {  # categorical variables that need to be encoded
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "elec_cons",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    'ARM2018_subset4_noNA': {
        "name": "evaluation data round 4",
        "url": "",
        "header": [0],
        "drop_cols": [ "year","country","hhid","hhweight", "climatezone"],  # columns to drop
        "categorical_vars": {  # categorical variables that need to be encoded
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "elec_cons",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    'ARM2018_subset1_eval': {
        "name": "subset 1 evaluation data",
        "url": "",
        "header": [0],
        "drop_cols": ["year", "country", "hhid", "hhweight"],
        "categorical_vars": {
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },

            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },


        },
        "target": "exp",
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1),
        },
        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,
                "max_depth": 5,
            },
        },

    },
    'ARM2018_subset1_eval_log': {
        "name": "subset 1 evaluation data",
        "url": "",
        "header": [0],
        "drop_cols": ["year", "country", "hhid", "hhweight"],
        "categorical_vars": {
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },

            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },


        },
        "target": "exp",
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1),
        },
        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,
                "max_depth": 5,
            },
        },

    },
    'GHA2017_subset1_eval': {
        "name": "subset 1 evaluation data",
        "url": "",
        "header": [0],
        "drop_cols": ["year", "country", "hhid", "hhweight"],
        "categorical_vars": {
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },

            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },


        },
        "target": "exp",
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1),
        },
        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,
                "max_depth": 5,
            },
        },

    },
    'ARM2018_subset1_noNA': {
        "name": "subset 1 evaluation data",
        "url": "",
        "header": [0],
        "drop_cols": ["year", "country", "hhid", "hhweight"],
        "categorical_vars": {
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },

            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },


        },
        "target": "exp",
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1),
        },
        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,
                "max_depth": 5,
            },
        },

    }

}



DATASETS.keys()

'''DATASETS: Dict[str, Dict[str, Any]] = {

    "BRA2002_subset4": {
        "name": "Brazil 2002 data round 4",
        "url": "",
        "header": [0],
        "drop_cols": [ "year","country","hhid","hhweight", "climatezone"],  # columns to drop
        "categorical_vars": {  # categorical variables that need to be encoded
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "elec_cons",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    "ARM2018_subset4": {
        "name": "Armenia 2018 data round 4",
        "url": "",
        "header": [0],
        "drop_cols": [ "year","country","hhid","hhweight", "climatezone"],  # columns to drop
        "categorical_vars": {  # categorical variables that need to be encoded
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "elec_cons",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    }
}




'''

'''DATASETS: Dict[str, Dict[str, Any]] = {
    "dataAllYear": {
        "name": "data ALL YEARs",
        "url": "",
        "header": [0],
        "drop_cols": ["admin1", "admin2", "psu", "hhid", "uhid", "hhweight", "country"],  # columns to drop
        "categorical_vars": {  # the cat. (i.e., discrete) vars. (i.e., features) that need to be encoded
            "urban": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "climatezone": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "basiceduc": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "seceduc": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fixedwater": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fixedtoilet": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "quintile": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "singlefam": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "floor": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "wall": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "roof": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "health_insur": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "collectbiom": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_grid": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_re": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_dg": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "stove_biom": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "stove_krsn": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "stove_gas": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "stove_elec": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "waterheat_biom": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "waterheat_centr": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "waterheat_krsn": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "waterheat_gas": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "waterheat_elec": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "spaceheat_biom": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "spaceheat_centr": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "spaceheat_krsn": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "spaceheat_gas": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "spaceheat_elec": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "aircool_accool": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "aircool_fan": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "freezer": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "dishwash": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "dryer": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "iron": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "phone": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "vacclean": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "pc": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "bicycle": {
                "class": LabelEncoder,
                "kwargs": {},
            }
        },
        "target": "fixedwater",  # the  label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (0, 1)
        },
        "model": {
            "class": LogisticRegression,
            "kwargs": {
                "class_weight": None,  # class_weight: dict or ‘balanced’, default=None
                "max_iter": 3000,  # max_iter: int, default=100
                "n_jobs": -1  # -1 means using all processors
            }
        }
    },
    "2002_BRA_clean": {
        "name": "2002 Brazil Round 1 evaluation",
        "url": "TBD",
        "header": [0],
        "drop_cols": ["ID"],  # columns to drop
        "categorical_vars": {  # the cat. (i.e., discrete) vars. (i.e., features) that need to be encoded
            "urban": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "hhsize": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "head_literate": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "tv": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "music": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "fridge": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            },
        },
        "target": "exp",  # the  label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },
        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    "2002_BRA": {
        "name": "2002 Brazil Round 1",
        "url": "TBD",
        "header": [0],
        "drop_cols": ["ID"],  # columns to drop
        "categorical_vars": {  # the cat. (i.e., discrete) vars. (i.e., features) that need to be encoded
            "urban": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "hhsize": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "head_literate": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "tv": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "music": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            }, "fridge": {
                "class": OneHotEncoder,
                "kwargs": {"dtype": int}
            },
        },
        "target": "exp",  # the  label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },
        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    "Brazil_2002_round2": {
        "name": "2002 Brazil Round 2 evaluation",
        "url": "TBD",
        "header": [0],
        "drop_cols": ["hhid"],  # columns to drop
        "categorical_vars": {  # the categorical variables that need to be encoded
            "urban": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_grid": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "stove_biom": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "stove_gas": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "aircool_accool": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            #"phone": {
             #   "class": OneHotEncoder,
              #  "kwargs": {"dtype": int}
            #},
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "pc": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "exp",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    "Brazil_2002_round3": {
        "name": "2002 Brazil Round 2 evaluation",
        "url": "TBD",
        "header": [0],
        "drop_cols": ["hhid"],  # columns to drop
        "categorical_vars": {  # the categorical variables that need to be encoded
            "urban": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_grid": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "stove_biom": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "stove_gas": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "aircool_accool": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            #"phone": {
             #   "class": OneHotEncoder,
              #  "kwargs": {"dtype": int}
            #},
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "pc": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "exp",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    "BRA2002_subset4": {
        "name": "non-NA Brazil data round 4",
        "url": "",
        "header": [0],
        "drop_cols": [ "year","country","hhid","hhweight", "climatezone"],  # columns to drop
        "categorical_vars": {  # categorical variables that need to be encoded
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "elec_cons",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    },
    "ARM2018_subset4": {
        "name": "Armenia data round 4",
        "url": "",
        "header": [0],
        "drop_cols": [ "year","country","hhid","hhweight", "climatezone"],  # columns to drop
        "categorical_vars": {  # categorical variables that need to be encoded
            "head_literate": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "head_male": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "elec_any": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "fridge": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "tv": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "music": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "scooter": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "car": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "publictransport": {
                "class": LabelEncoder,
                "kwargs": {},
            },
            "washmach": {
                "class": LabelEncoder,
                "kwargs": {},
            },
        },
        "target": "elec_cons",  # the label of the dependent variable (i.e., feature)
        "scaler": {
            "class": MinMaxScaler,
            "feature_range": (-1, 1)
        },

        "model": {
            "class": HistGradientBoostingRegressor,
            "kwargs": {
                "max_iter": 3000,  # max_iter: int, default=100
                "max_depth": 5,
            }
        }
    }
}'''

