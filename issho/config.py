import os

ISSHO_CONFIG_OPTS = {
    'HIVE_JDBC': None,
    'HIVE_OPTS': '--maxHistoryRows=1000000 --outputformat=tsv2'
}

ISSHO_CONFIG = {
    k: os.environ.get(k) for k in ISSHO_CONFIG_OPTS
}



def load_profile(hostname):
    return


def _get_conf_variable(var_name):

