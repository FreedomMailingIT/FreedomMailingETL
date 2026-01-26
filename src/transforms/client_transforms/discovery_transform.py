"""
Discovery Bay is a Tyler Tech customer so use standard Tyler Tech modules.


Using global import usually not good practice but used here to make
Discovery Bay transform a Tyler Tech clone and namespace pollution
not an issue because nothing else here.

If more is needed, create custom transform module.
"""


from transforms.client_transforms.tyler_tech_transform import *  #pylint: disable=W0401:wildcard-import, W0614:unused-wildcard-import
