/*=========================================================================

  Program:   ParaView
  Module:    vtkSMPropertyGroup.h

  Copyright (c) Kitware, Inc.
  All rights reserved.
  See Copyright.txt or http://www.paraview.org/HTML/Copyright.html for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/

#ifndef __vtkSMPropertyGroup_h
#define __vtkSMPropertyGroup_h

#include "vtkPVServerManagerCoreModule.h" //needed for exports
#include "vtkSMObject.h"

class vtkPVXMLElement;
class vtkSMDocumentation;
class vtkSMProperty;
class vtkSMPropertyGroupInternals;
class vtkSMProxy;

class VTKPVSERVERMANAGERCORE_EXPORT vtkSMPropertyGroup : public vtkSMObject
{
public:
  static vtkSMPropertyGroup* New();
  vtkTypeMacro(vtkSMPropertyGroup, vtkSMObject)
  void PrintSelf(ostream& os, vtkIndent indent);

  // Description:
  // Sets the name of the property group to \p name.
  vtkSetStringMacro(Name)

  // Description:
  // Returns the name of the property group.
  vtkGetStringMacro(Name)

  // Description:
  // Sets the name of the property group to \p name.
  vtkSetStringMacro(XMLLabel)

  // Description:
  // Returns the name of the property group.
  vtkGetStringMacro(XMLLabel)

  // Description:
  // Sets the name of the panel widget to use for the property group.
  vtkSetStringMacro(PanelWidget)

  // Description:
  // Gets the name of the panel widget to use for the property group.
  vtkGetStringMacro(PanelWidget)

  // Description:
  // Sets the panel visibility for the property group.
  //
  // \see vtkSMProperty::SetPanelVisibility()
  vtkSetStringMacro(PanelVisibility)

  // Description:
  // Returns the panel visibility for the property group.
  vtkGetStringMacro(PanelVisibility)

  // Description:
  // Returns true if the property group contains zero properties.
  bool IsEmpty() const;

  // Description:
  // Adds \p property to the group. function can be NULL.
  void AddProperty(const char* function, vtkSMProperty *property);

  // Description:
  // Returns the property at \p index.
  vtkSMProperty* GetProperty(unsigned int index) const;

  // Description:
  // Returns the property associated with a given function, if any.
  vtkSMProperty* GetProperty(const char* function) const;

  // Description:
  // Given property in the group, returns its function. Will return NULL if the
  // property is not present in this group.
  const char* GetFunction(vtkSMProperty* property) const;

  // Description:
  // Returns the number of properties in the group.
  unsigned int GetNumberOfProperties() const;

  // Description:
  // Returns the documentation for this proxy.
  vtkGetObjectMacro(Documentation, vtkSMDocumentation);

protected:
  vtkSMPropertyGroup();
  ~vtkSMPropertyGroup();

  friend class vtkSMProxy;
  virtual int ReadXMLAttributes(vtkSMProxy* parent, vtkPVXMLElement* element);

  vtkSMDocumentation* Documentation;
private:
  vtkSMPropertyGroup(const vtkSMPropertyGroup&); // Not implemented
  void operator=(const vtkSMPropertyGroup&); // Not implemented

  char *Name;
  char *XMLLabel;
  char *PanelWidget;
  char *PanelVisibility;

  vtkSMPropertyGroupInternals* const Internals;
};

#endif
