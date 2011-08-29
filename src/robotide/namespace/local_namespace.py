#  Copyright 2008-2011 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from robotide.spec.iteminfo import VariableInfo

def LocalNamespace(controller, namespace, row=None):
   if row is not None: # can be 0!
       return LocalRowNamespace(controller, namespace, row)
   return LocalMacroNamespace(controller, namespace)

class LocalMacroNamespace(object):

    def __init__(self, controller, namespace):
        self._controller = controller
        self._namespace = namespace

    def get_suggestions(self, start):
        return self._namespace.get_suggestions_for(self._controller, start)

    def has_name(self, value):
        for sug in self._namespace.get_suggestions_for(self._controller, value):
            if sug.name == value:
                return True
        return False

class LocalRowNamespace(LocalMacroNamespace):

    def __init__(self, controller, namespace, row):
        LocalMacroNamespace.__init__(self, controller, namespace)
        self._row = row

    def get_suggestions(self, start):
        suggestions = LocalMacroNamespace.get_suggestions(self, start)
        if start.startswith('$') or start.startswith('@'):
            matching_assignments = []
            for row, step in enumerate(self._controller.steps):
                if self._row == row:
                    break
                matching_assignments += [val.replace('=', '').strip() for val in step.assignments if val.startswith(start)]
            if matching_assignments:
                suggestions = suggestions + [VariableInfo(name, '?', self._controller.display_name) for name in matching_assignments]
                suggestions = sorted(suggestions)
        return suggestions

    def has_name(self, value):
        if self._row:
            for row, step in enumerate(self._controller.steps):
                if self._row == row:
                    break
                if step.is_assigning(value):
                    return True
        return LocalMacroNamespace.has_name(self, value)