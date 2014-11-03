from paraview.simple import *
import paraview

# This test tests backwards compatibility for ColorArrayName and ColorAttributeType
# properties.

assert (paraview.compatibility.GetVersion().GetVersion() == None),\
    "ParaView modules should never force backwords compatibility to any version"
assert ((paraview.compatibility.GetVersion() < 4.1) == False),\
    "less-than test should always fail when version is not specified."
assert ((paraview.compatibility.GetVersion() <= 4.1) == False),\
    "less-equal test should always fail when version is not specified."
assert ((paraview.compatibility.GetVersion() > 4.1) == True),\
    "greater-than test should always fail when version is not specified."
assert ((paraview.compatibility.GetVersion() >= 4.1) == True),\
    "greater-equal test should always fail when version is not specified."

Sphere()
r = Show()
assert (len(r.ColorArrayName) == 2),\
    "'ColorArrayName' must be a 2-tuple"

raisedException = False
try:
  a = r.ColorAttributeType
except AttributeError:
  raisedException = True

assert raisedException, "Accessing ColorAttributeType must have raised an exception."


# Now switch backwards compatibility to 4.1
paraview.compatibility.major = 4
paraview.compatibility.minor = 1
assert ((paraview.compatibility.GetVersion() < 4.1) == False), "version comparison failed"
assert ((paraview.compatibility.GetVersion() <= 4.1) == True), "version comparison failed"
assert ((paraview.compatibility.GetVersion() > 4.1) == False), "version comparison failed"
assert ((paraview.compatibility.GetVersion() >= 4.1) == True), "version comparison failed"

a = r.ColorAttributeType
assert (type(a) == str), "'ColorAttributeType' must return a string"

a = r.ColorArrayName
assert (type(a) == str), "'ColorArrayName' must return a string"

r.ColorAttributeType = "CELL_DATA"
r.ColorArrayName = "Alpha"

paraview.compatibility.major = None
paraview.compatibility.minor = None
assert (r.ColorArrayName[:] == ["CELLS", "Alpha"]), "'ColorArrayName' value is not as expected."
