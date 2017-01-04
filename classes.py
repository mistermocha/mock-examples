from collections import namedtuple
from subprocess import Popen, PIPE
import re
import shlex


defaults = {"source": "yum", "version": "latest", "requires": []}
required_fields = defaults.keys() + ["name"]
valid_versions = {
  "yum", "^\d+(\.\d+)*$",
  "pip", "^=[<=>]\d+(\.d+)$",
  "gem", "^=[<=>]\d+(\.d+)$",
}
default_source = "yum"

class InstallerException(Exception):
  pass


class InstallConfig(namedtuple("InstallConfig", required_fields)):
  def __init__(self, data):
    if data.get("source", default_source) not in valid_versions.keys():
      raise InstallerException(
        "{} is not a valid source. Valid sources are {}".format(valid_versions.keys()))
    self._valid_version(data)
    try:
      super(self, InstallConfig).__init__(*[data[key] for key in required_fields])
    except KeyError:
      raise InstallerException(
        "Config is missing a value. These are required: {}".format(required_fields))
    self._requires = data.get("requires", [])
    if type(self._requires) is str:
      self._requires = [self._requires]

  def _valid_version(self, data):
    version_regex = valid_versions.get(data['source'])
    version = data.get('version')
    if not re.match(version_regex, version):
      raise InstallerException(
        "Invalid version pattern {} for source type {}".format(
          version_regex, version))

  @property
  def requires(self):
    return self._requires

class Installer(InstallConfig):
  def _run(self, cmd):
    out = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    out.wait()
    return out

  def _yum_install(self):
    cmd = "yum install {}".format(self.name)
    if self.version != self.latest:
      cmd += " version={}".format(self.version)
    return self._run(cmd)

  def _pip_install(self):
    cmd = "pip install {}".format(self.name)
    if self.version != 'latest':
      cmd += "{}".format(self.version)
    return self._run(cmd)

  def _gem_install(self):
    cmd = "gem install {}".format(self.name)
    if self.version != 'latest':
      cmd += "--version '{}'".format(self.version)
    return self._run(cmd)

  def install(self):
    install_func = getattr(self, '_{}_install'.format(self.source))
    if install_func(self).return_code():
      return True
    return False
