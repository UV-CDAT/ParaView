r"""
    This module is a ParaViewWeb server application.
    The following command line illustrate how to use it::

        $ pvpython .../pv_web_file_loader.py --data-dir /.../path-to-your-data-directory --file-to-load /.../any-vtk-friendly-file.vtk

    --file-to-load is optional and allow the user to pre-load a given dataset.
    --data-dir is used to list that directory on the server and let the client
               choose a file to load.

    Any ParaViewWeb executable script come with a set of standard arguments that
    can be overriden if need be::

        --port 8080
             Port number on which the HTTP server will listen to.

        --content /path-to-web-content/
             Directory that you want to server as static web content.
             By default, this variable is empty which mean that we rely on another server
             to deliver the static content and the current process only focus on the
             WebSocket connectivity of clients.

        --authKey vtkweb-secret
             Secret key that should be provided by the client to allow it to make any
             WebSocket communication. The client will assume if none is given that the
             server expect "vtkweb-secret" as secret key.
"""

# import to process args
import sys
import os

# import paraview modules.
from paraview import simple
from paraview.web import wamp      as pv_wamp
from paraview.web import protocols as pv_protocols
from vtk.web import protocols as vtk_protocols

from vtk.web import server
from vtkWebCorePython import *

# import annotations
from autobahn.wamp import exportRpc

try:
    import argparse
except ImportError:
    # since  Python 2.6 and earlier don't have argparse, we simply provide
    # the source for the same as _argparse and we use it instead.
    import _argparse as argparse

# =============================================================================
# Create custom File Opener class to handle clients requests
# =============================================================================

class _FileOpener(pv_wamp.PVServerProtocol):

    # Application configuration
    reader     = None
    fileToLoad = None
    pathToList = "."
    view       = None
    authKey    = "vtkweb-secret"

    def initialize(self):
        # Bring used components
        self.registerVtkWebProtocol(vtk_protocols.vtkWebFileBrowser(_FileOpener.pathToList, "Home"))
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebMouseHandler())
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPort())
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPortImageDelivery())
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPortGeometryDelivery())
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebTimeHandler())

        # Update authentication key to use
        self.updateSecret(_FileOpener.authKey)

        # Create default pipeline
        if _FileOpener.fileToLoad:
            _FileOpener.reader = simple.OpenDataFile(_FileOpener.fileToLoad)
            simple.Show()

            _FileOpener.view = simple.Render()
            _FileOpener.view.ViewSize = [800,800]
            # If this is running on a Mac DO NOT use Offscreen Rendering
            #view.UseOffscreenRendering = 1
            simple.ResetCamera()
        else:
            _FileOpener.view = simple.GetRenderView()
            simple.Render()
            _FileOpener.view.ViewSize = [800,800]
        simple.SetActiveView(_FileOpener.view)

    def openFile(self, file):
        id = ""
        if _FileOpener.reader:
            try:
                simple.Delete(_FileOpener.reader)
            except:
                _FileOpener.reader = None
        try:
            _FileOpener.reader = simple.OpenDataFile(file)
            simple.Show()
            simple.Render()
            simple.ResetCamera()
            id = _FileOpener.reader.GetGlobalIDAsString()
        except:
            _FileOpener.reader = None
        return id

    @exportRpc("openFileFromPath")
    def openFileFromPath(self, file):
        file = os.path.join(_FileOpener.pathToList, file)
        return self.openFile(file)

# =============================================================================
# Main: Parse args and start server
# =============================================================================

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="ParaView/Web file loader web-application")

    # Add default arguments
    server.add_arguments(parser)

    # Add local arguments
    parser.add_argument("--file-to-load", help="relative file path to load based on --data-dir argument", dest="data")
    parser.add_argument("--data-dir", default=os.getcwd(), help="Base path directory", dest="path")

    # Exctract arguments
    args = parser.parse_args()

    # Configure our current application
    _FileOpener.fileToLoad = args.data
    _FileOpener.pathToList = args.path
    _FileOpener.authKey    = args.authKey

    # Start server
    server.start_webserver(options=args, protocol=_FileOpener)