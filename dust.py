import urllib.request

class GetData:
    
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey=qdk7vKRWwWmAlv5Zx3V5bMU%2FWm5uMvZLF2vrjS8WzGgU2DHkIUcGPzbA7Rwoa%2BmHnOU70idPNJfrWD85pbdgJA%3D%3D&numOfRows=1&pageNo=1&stationName=%EC%86%A1%EB%82%B4%EB%8C%80%EB%A1%9C(%EC%A4%91%EB%8F%99)&dataTerm=DAILY&ver1.3"

    def main(self):
        data = urllib.request.urlopen(self.url).read()

        f = open("sample.xml", "wb")
        f.write(data)
        f.close

#end of class

getData = GetData()
getData.main()
