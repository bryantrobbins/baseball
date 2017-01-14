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
