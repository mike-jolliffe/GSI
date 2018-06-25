import requests
import json

class Getter():
  """Get specified data via USGS's NWIS API"""

  def __init__(self, bbox, type='S', start_date=None, end_date=None):
      self.base_url = 'https://waterservices.usgs.gov/nwis/dv/?format=json'
      self.type = type
      self.headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept-Content": "gzip",
        "Accept-Language": "en-US,en;q=0.8"
      }

      self.payload = {
        "bbox": bbox,
        "startDT": start_date,
        "endDT": end_date,
        "parameterCd": "00060,00065"
      }

  def make_request(self):
      """Send NWIS an HTTP request, write valid response content to JSON file
      :return: True if successfully wrote to file, False or Exception otherwise
      :rtype: Boolean
      """
      # Repurpose Getter for groundwater API
      if self.type == 'G':
          # Set parameterCd to "depth to groundwater"
          self.payload["parameterCd"] = "72019"
          self.base_url = 'https://waterservices.usgs.gov/nwis/gwlevels?format=json'

      resp = requests.get(self.base_url, params=self.payload, headers=self.headers)
      if resp.status_code == 200:
          data = resp.json()
          fname = self.type + '_water_' + self.payload['startDT'] + '_' + self.payload['endDT'] + '.json'
          with open(fname, 'w') as f:
              json.dump(data, f, indent=4)
          return True
      else:
          print(
            f"HTTP STATUS CODE: {resp.status_code} -- REASON: {resp.reason}"
          )
          return False


if __name__ == '__main__':
    getter = Getter('-120.63,34.67,-120.11,34.86', 'G', '1950-01-01', '2018-06-22')
    getter.make_request()
