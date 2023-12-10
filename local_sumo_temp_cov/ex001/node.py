# node.py
# Author: Quentin Goss
# Last Modified. 10/17/19

class node(object):
    def __init__(self, type):
        type = type.lower
        if not type in ['spawn','sink','reward']:
            print("Invalid type. Must be 'spawn','sink', or 'reward'")
            raise SyntaxError
        self.type = type
        return

