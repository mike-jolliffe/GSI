import requests
import csv

class Getter():
  """Get specified data via Water Quality Data Portal API"""

  def __init__(self, bbox, type='Sta', start_date=None, end_date=None):
      self.base_url = 'https://www.waterqualitydata.us/data/Station/search'
      self.type = type
      self.headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept-Content": "gzip",
        "Accept-Language": "en-US,en;q=0.8"
      }

      self.payload = {
        "bBox": bbox,
        "startDateLo": start_date,
        "startDateHi": end_date,
        "mimeType": "csv"
      }

  def make_request(self):
      """Send WQP an HTTP request, write valid response content to JSON file
      :return: True if successfully wrote to file, False or Exception otherwise
      :rtype: Boolean
      """
      # Repurpose Getter for groundwater API
      if self.type == 'Res':
          # Set parameterCd to "depth to groundwater"
          self.base_url = 'https://www.waterqualitydata.us/data/Result/search'

      resp = requests.get(self.base_url, params=self.payload, headers=self.headers)
      if resp.status_code == 200:
          print("Request, successful. Parsing to csv file...")
          decoded = resp.content.decode('utf-8')
          cr = csv.reader(decoded.splitlines(), delimiter=',')
          my_list = list(cr)
          fname = 'WaterQuality_Res_01-01-1950_01-01-1960.csv'
          # fname = 'WaterQuality_' + self.type + '_' + self.payload['startDateLo'] + '_' + self.payload['startDateHi'] + '.csv'
          with open(fname, 'a') as f:
              writer = csv.writer(f, delimiter=',')
              for row in my_list:
                   writer.writerow(row)
          return True
      else:
          print(
            f"HTTP STATUS CODE: {resp.status_code} -- REASON: {resp.reason}"
          )
          return False


if __name__ == '__main__':
    getter = Getter('-120.63,34.67,-120.11,34.86', 'Res', '01-01-2015', '07-01-2018')
    getter.make_request()
