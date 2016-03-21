import groovy.io.FileType
import groovy.json.*


void saveUrlToFile(String url, String localFile) {
  def file = new File(localFile).newOutputStream()
  file << new URL(url).openStream()
  file.close()
}

void extractZip(String zipFileName, String dir) {
  def zipFile = new java.util.zip.ZipFile(new File(zipFileName))
  zipFile.entries().each {
    new File("${dir}/${it}").append(zipFile.getInputStream(it))
  }
}

void combineZipsToFile(String filesDir, String headerFile, String outFile) {
  def filesDirObj = new File(filesDir)
  // Combine regular season event logs
  new File(outFile).withWriter { out ->
    out.write new File(headerFile).text
    filesDirObj.eachFile(FileType.FILES) {
      def f = new File(filesDirObj.getPath() + File.separator + it.name)
      out.write f.text.replaceAll("\\r\\n", "\n")
    }
  }
}

void downloadGamelogs(def remoteZips, String filesDir) {

  // Declare directories
  def zips_dir = new File('tmp_zips')
  def files_dir = new File(filesDir)

  // Delete directories, if existing
  zips_dir.deleteDir()  
  files_dir.deleteDir()  

  // Make directories
  zips_dir.mkdir()
  files_dir.mkdir()

  // Download and extract each zip
  remoteZips.each {
    zipName = "gl${it}.zip"
    localZip = "${zips_dir.path}${File.separator}${zipName}"
    feedUrl = "http://www.retrosheet.org/gamelogs/${zipName}"
    saveUrlToFile(feedUrl, localZip)
    extractZip(localZip, files_dir.path)
  }
  
  // Remove zips dir, now that files extacted
  zips_dir.deleteDir()
}

void downloadLahman(String url, String filesDir) {

  // Declare directories
  def zips_dir = new File('tmp_zips')
  def files_dir = new File(filesDir)

  // Delete directories, if existing
  zips_dir.deleteDir()  
  files_dir.deleteDir()  

  // Make directories
  zips_dir.mkdir()
  files_dir.mkdir()

  // Download and extract each zip
  zipName = "lahman.zip"
  localZip = "${zips_dir.path}${File.separator}${zipName}"
  saveUrlToFile(url, localZip)
  extractZip(localZip, files_dir.path)
  
  // Remove zips dir, now that files extacted
  zips_dir.deleteDir()
}

def urlToJson(String url){
  def stream = new URL(url).openStream()
  def responseText =new StringBuffer()
  def reader = stream.newReader()
  int charactersRead = 0
  def charArray = new char[1024]
  while((charactersRead = reader.read(charArray,0, 1024))!= -1){
    responseText.append(charArray,0,charactersRead);
  }
  def response = new JsonSlurper().parseText(responseText.toString())
  return response  
}

void downloadMLB(String url, String stat, String gameType, String year) {
  // Declare directories
  String filesDir= stat+"\\"+gameType + '-' + year
  def dataDirectory = new File("mlbData")
  def directory = new File("mlbData\\"+stat)
  def headerDir = new File("mlbData\\headers")
  dataDirectory.mkdir()
  directory.mkdir()
  headerDir.mkdir()

  // Making necessary data fule
  def files_dir = new File("mlbData\\"+filesDir+".csv")
  files_dir.delete()  
  


  // Retrieving JSON from mlb API and storing it into a CSV file 
  def jsonResponse = urlToJson(url)
  if(jsonResponse.stats_sortable_player.queryResults.row){
    def columns  = jsonResponse.stats_sortable_player.queryResults.row*.keySet().flatten().unique()
    def headerFile = new File("mlbData\\headers\\"+stat+".csv")
    headerFile.delete()
    def headers = columns.collect().join(',')
    headerFile.append('year,game_type')
    headerFile.append(headers)

    def data = jsonResponse.stats_sortable_player.queryResults.row.collect { row ->
         year+ ','+gameType+','+columns.collect { colName -> row[colName] }.join(',')
    }.join('\n') 
    files_dir.append(data)
  }
}


void downloadIntoSingle(def remoteZips, String headersPath, String outputPath) {
  downloadGamelogs(remoteZips, "tmp_files")
  combineZipsToFile("tmp_files", headersPath, outputPath)
  new File("tmp_files").deleteDir()
}

// Download and extract Retrosheet gamelogs
String headerFilePath = new File('metadata/gl_headers.csv').path
new File("gamelogs").mkdir()
downloadIntoSingle(['1871_99','1900_19','1920_39','1940_59','1960_69','1970_79','1980_89','1990_99','2000_09','2010_15'],
                    headerFilePath,
                    "gamelogs/gl_regular.csv")

downloadIntoSingle(['ws', 'wc', 'dv', 'lc'],
                    headerFilePath,
                    "gamelogs/gl_post.csv")

downloadIntoSingle(['as'],
                    headerFilePath,
                    "gamelogs/gl_allstar.csv")

// Download Lahman database CSVs
String lahmanUrl = "http://seanlahman.com/files/database/lahman-csv_2015-01-24.zip"
downloadLahman(lahmanUrl, "lahman")



String[] stats = ['hitting','pitching','fielding']
String[] seasons = ['2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000','1999','1998','1997','1996','1995','1994','1993','1992','1991','1990','1989','1988','1987','1986','1985','1984','1983','1982','1981','1980','1979','1978','1977','1976','1975','1974','1973','1972','1971','1970','1969','1968','1967','1966','1965','1964','1963','1962','1961','1960','1959','1958','1957','1956','1955','1954','1953','1952','1951','1950','1949','1948','1947','1946','1945','1944','1943','1942','1941','1940','1939','1938','1937','1936','1935','1934','1933','1932','1931','1930','1929','1928','1927','1926','1925','1924','1923','1922','1921','1920','1919','1918','1917','1916','1915','1914','1913','1912','1911','1910','1909','1908','1907','1906','1905','1904','1903','1902','1901','1900','1899','1898','1897','1896','1895','1894','1893','1892','1891','1890','1889','1888','1887','1886','1885','1884','1883','1882','1881','1880','1879','1878','1877','1876']
String [] gameTypes = ['S','R','A','F','D','L','W']
def aggregate  = new File("mlbData\\aggregate")
aggregate.delete()
aggregate.mkdir()
for(season in seasons){
  for(stat in stats){
    for(game in gameTypes){
      String mlbUrl = "http://mlb.mlb.com/pubajax/wf/flow/stats.splayer?season={{season}}&stat_type={{stat_type}}&page_type=SortablePlayer&game_type=%27{{game_type}}%27&player_pool=ALL&season_type=ANY&sport_code=%27mlb%27&results=1000000"
      downloadMLB(mlbUrl.replace("{{season}}", season).replace("{{stat_type}}", stat).replace("{{game_type}}", game), stat,game,season)
    }
   aggregateData(stat,gameTypes)
  }
}

void aggregateData(String stat, String[] gameTypes){
  def aggregate  = new File("mlbData\\aggregate\\"+stat+".csv")
  combineZipsToFile("mlbData\\"+stat, "mlbData\\headers\\"+stat+".csv", "mlbData\\aggregate\\MLB-"+stat+".csv")

}
