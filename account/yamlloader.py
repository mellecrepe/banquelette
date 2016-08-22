#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import yaml
import pprint

# =============================================================================
def load_yaml(filename):
    """Parse et charge Un fichier de config YAML."""

    with open(filename, 'r') as f:
        data = yaml.load( f.read() )

    return data

# =============================================================================
if __name__ == '__main__':
    yaml_dict = load_yaml( sys.argv[1] )
    pprint.pprint( yaml_dict )
