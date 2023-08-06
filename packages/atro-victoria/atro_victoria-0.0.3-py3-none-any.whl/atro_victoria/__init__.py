from datetime import datetime
from pydantic_core import Url
import requests
from pydantic import AnyHttpUrl, PastDatetime
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

def strigify_datetime(dt: datetime):
  return int(dt.timestamp() * 1000)

class VmCsvRowBase(BaseSettings):
  job: str 
  name: str
  timestamp: PastDatetime = datetime.now()
  url: AnyHttpUrl = Url("http://localhost:8480/")
  model_config = SettingsConfigDict(env_prefix='ATRO_VM_', env_file=[(Path.home() / ".config" / "atro" / "vm.env").as_posix(), ".env"]
)
    
  def format(self):
    vals = self.model_dump()
    counter = 0
    output = ""
    vals.pop('url')
    for val in vals:
      counter+=1
      if val == "timestamp":
        output += "," + str(counter) + ":time:unix_ms"
        continue
      if isinstance(vals[val], (int, float)):
        output += "," + str(counter) + ":metric:" + val
      else:
        output += "," + str(counter) + ":label:" + val
    if output == "":
      raise Exception("No values to format")
    return output[1:]

  def data_as_csv(self):
    vals = self.model_dump()
    vals.pop('url')
    vals['timestamp'] = strigify_datetime(vals['timestamp'])
    output = ""
    for val in vals.values():
      
      output += "," + str(val)
    if output == "":
      raise Exception("No values to format")
    return output[1:]

  def post(self):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = self.data_as_csv()

    url = str(self.url) + 'insert/0/prometheus/api/v1/import/csv?format=' + self.format()

    response = requests.post(
        url,
        headers=headers,
        data=data,
    )
    return response
