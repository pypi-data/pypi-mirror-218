"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the ``napari_get_reader`` hook specification, (to create
a reader plugin) but your plugin may choose to implement any of the hook
specifications offered by napari.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below accordingly.  For complete documentation see:
https://napari.org/docs/dev/plugins/for_plugin_developers.html
"""
from acquifer.utils import array_from_directory
import os

def napari_get_reader(path):
    """This function is responsible for providing a suitable viewer function, depending on what file, directory is selected.

    Parameters
    ----------
    path : str
        Path to an IM dataset directory.

    Returns
    -------
    function or None
        If the path is a directory, return the reader function. Otherwise (list of path to files, or directories), return None.
    """
    if not isinstance(path, str):
        return None # our reader except a single path to a directory only
    
    if not os.path.isdir(path):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function


def reader_function(path):
    """
    Take a path to an IM dataset directory, and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : path to an IM directory.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of layer.
        Both "meta", and "layer_type" are optional. napari will default to
        layer_type=="image" if not provided
    """
    array6D = array_from_directory(path)
    
    DEFAULT_CHANNEL_COLORS = ["cyan", "green","yellow", "red", "magenta", "gray"] # ordered from CO1 to CO6
    
    listNames     = [] # as shown in left channel-panel in napari, default Cx with x in [1,6]
    listColormaps = [] # color map/LUT for the channels
    listOpacities = [] # default opacities (1 for BF, 0.5 for Fluo to hava good blend)
    
    for channel in array6D["Channel"].values:
        listNames.append( "C" + str(channel) )
        listColormaps.append( DEFAULT_CHANNEL_COLORS[channel-1] ) # channel-1 since IM-channels are 1-based while positional-indexes are 0-base
        listOpacities.append( 1 if channel==6 else 0.5)
    
    metadata = {"channel_axis" : 0,
                "name"     : listNames,
                "colormap" : listColormaps,
                "opacity"  : listOpacities
                }
    
    return [ (array6D, metadata ) ]