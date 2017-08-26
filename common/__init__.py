from sikuli import *
Settings.MoveMouseDelay = 0.75
Settings.MinSimilarity = .9
setAutoWaitTimeout(120)

import os
from aft_model import AftModel

myPath = os.path.dirname(getBundlePath()) + os.sep + "libs" 
if not myPath in sys.path: sys.path.append(myPath)

myPath = os.path.dirname(getBundlePath()) + os.sep + "common"
if not myPath in sys.path: sys.path.append(myPath)

from powertools import PowerTools
from project import Project
from workspace import Workspace

from appdescriptor import AppDescriptor
from installer import Installer, InstallerModel
from template import ProjectTemplate
from utils import Shell, XmlUtils, ScreenUtils

from search import flex_label, flex_image, flex_button
