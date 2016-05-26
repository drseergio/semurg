# exterior.R - generates a chart given a buy situation
#
# 2012 Copyright Sergey Pisarenko (drseergio@gmail.com)
#
# Invoke with following CLI arguments:
# $ Rscript exterior.R <DATE> <SYMBOL> <FILENAME> <PATH_TO_CONFIG>
#
# <DATE> - the date when the buy situation occurred
# <SYMBOL> - the instrument we are working with
# <FILENAME> - where to save the chart
# <PATH_TO_CONFIG> - path to file with DB configuration (yaml)
#
# This program expects that engine.R has done its work


require(quantmod)
require(RMySQL)
require(yaml)


# command line parameters
args     <- commandArgs(TRUE)
today    <- as.Date(args[1])
symbol   <- args[2]
filename <- args[3]
config   <- args[4]


db_config = yaml.load_file(config)

DB_NAME = db_config$db$s_db
DB_USER = db_config$db$user
DB_PASS = db_config$db$pass


# load market instrument data
bars <- getSymbols(src='yahoo', Symbols=c(symbol), auto.assign=FALSE)
assign(symbol, bars)


# load buy situations from DB
conn       <- dbConnect(dbDriver('MySQL'),
  dbname=DB_NAME,
  user=DB_USER,
  password=DB_PASS)
data       <- dbReadTable(conn, paste(
    "`buys` WHERE `date` = '", today, "' AND `symbol` = '", symbol, "'", sep=''))
dbDisconnect(conn)

# make sell chart
if (nrow(data) == 0) {
  before   <- today - 180
  finish   <- today + 90

  chartSeries(bars, subset=paste(before, '::', finish, sep=''), TA=paste(sep='',
      'addSMA(10);',
      'addSMA(5, col="blue");',
      'addVo();',
      'addMACD()'))
} else {
  # make chart
  bdate    <- as.Date(data$bdate)
  ddate    <- as.Date(data$ddate)

  before   <- bdate - 90
  finish   <- today + 90

  chartSeries(bars, subset=paste(before, '::', finish, sep=''), TA=paste(sep='',
      'addSMA(10);',
      'addSMA(5, col="blue");',
      'addVo();',
      'addMACD();',
      'addTA(xts(TRUE, bdate), on=-(1:2), col="222222");',
      'addTA(xts(TRUE, ddate), on=-(1:2), col="555555")'))
  #    'addTA(xts(TRUE, today), on=-(1:2), col="333333")'))
}

saveChart('png', file=filename, width=1000, height=1000)
dev.off()
