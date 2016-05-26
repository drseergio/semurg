# engine.R - discover buy situations in the market
#
# 2012 Copyright Sergey Pisarenko (drseergio@gmail.com)
#
# Invoke with following CLI arguments:
# $ Rscript engine.R <START_DATE> <TARGET_DATE> <DO_MC> <DEBUG> <PATH_TO_CONFIG>
#
# <START_DATE> - the starting date of the search
# <TARGET_DATE> - typically today's date
# <DO_MC> - multi-core TRUE/FALSE
# <DEBUG> - provide output in stdout
# <PATH_TO_CONFIG> - path to file with DB configuration (yaml)
#
# The program makes certain assumptions about DB schema


require(quantmod)
require(TTR)
require(RMySQL)
require(FinancialInstrument)
require(blotter)
require(quantstrat)
require(yaml)


# arguments
args      <- commandArgs(TRUE)
if (length(args) > 0) {
  from      <- args[1]              # begin date of search
  target    <- as.Date(args[2])     # today's date
  domc      <- as.logical(args[3])  # use multicore
  dodiag    <- as.logical(args[4])  # print-out progress
  config    <- args[5]
}


db_config = yaml.load_file(config)

SRC_DB_NAME = db_config$db$q_db
SRC_DB_USER = db_config$db$user
SRC_DB_PASS = db_config$db$pass

DST_DB_NAME = db_config$db$s_db
DST_DB_USER = db_config$db$user
DST_DB_PASS = db_config$db$pass


# load screened stocks from DB
src       <- dbConnect(dbDriver('MySQL'),
    dbname=SRC_DB_NAME,
    user=SRC_DB_USER,
    password=SRC_DB_PASS)
watched   <- dbListTables(src)
#watched   <- c('AAPL')


# configuartion of the gullwing
setDefaults(getSymbols.MySQL, user=SRC_DB_USER, password=SRC_DB_PASS, dbname=SRC_DB_NAME)
if (domc == TRUE) {
  require(parallel)
  options(mc.cores=12) # number of cores on CPU
}


# constants
shortSMA  <- 5                               # short SMA
longSMA   <- 40                              # long SMA
volSMA    <- 10                              # volume SMA
volMult   <- 2.5                             # expect at least X fold increase in volume
buyAfter  <- 10                              # only buy after X days since breakout occurred
macdMult  <- 1.05                            # expect MACD to be X-fold higher than signal MACD
closeMult <- 1.02                            # close price must be X-fold higher than lowest low
prcTrade  <- 0.25                            # maximum % of any single instrument to buy
startDay  <- max(shortSMA, longSMA, volSMA)  # minimum amount of days data we need for calculations


# results database
conn      <- dbConnect(dbDriver('MySQL'),
    dbname=DST_DB_NAME,
    user=DST_DB_USER,
    password=DST_DB_PASS)
dbSendQuery(conn, 'DELETE FROM breakouts')
dbSendQuery(conn, 'DELETE FROM buys')
dbDisconnect(conn)


# unset any existing strategies
try(rm(list=ls(pos=.blotter), pos=.blotter), silent=TRUE)
try(rm(list=ls(pos=.strategy) ,pos=.strategy), silent=TRUE)


# iterate through tickers and make them available to strategy
load_symbol <- function(symbol) {
  ubars    <- tryCatch(getSymbols(symbol, src='MySQL', auto.assign=FALSE), error=function(e) NULL)
  # skip if we don't have enough data
  if (is.null(ubars) || nrow(ubars) < startDay) return(NULL)
  bars     <- ubars[index(ubars) >= as.Date(from)]
  # skip if we don't have enough after filtering
  if (nrow(bars) < startDay) return(NULL)
  if (dodiag == TRUE) print(paste('Loaded', symbol))
  return(list(symbol=symbol, bars=bars))
}
dbDisconnect(src)

symbols <- c()
if (domc == TRUE) {
  to_load <- mclapply(watched, load_symbol)
} else {
  to_load <- lapply(watched, load_symbol)
}

for (data in to_load) {
  if (!is.null(data)) {
    symbols <- c(symbols, data$symbol)
    assign(data$symbol, data$bars)
  }
}


# detects price drops and increases in trading volume (stateful)
breakoutSig <- function(label, data, symbol=symbol, dodiag=dodiag) {
  n        <- nrow(data)
  points   <- vector(length=n)
  dates    <- vector(length=n)
  bdates   <- vector(length=n)
  minPrice <- -1  # current smallest price after a breakout

  smaLong  <- match.names('SMA40', colnames(data))
  smaShort <- match.names('SMA5', colnames(data))
  vma      <- match.names('VMA', colnames(data))
  closeCol <- match.names('Close', colnames(data))
  volCol   <- match.names('Volume', colnames(data))

  for (i in seq(startDay, n)) {
    close    <- data[i, closeCol]
    volume   <- data[i, volCol]
    today    <- index(close)

    # breakout detected
    if (close             < data[i, smaLong] &&
        volume            > (data[i, vma] * volMult) &&
        data[i, smaShort] < data[i, smaLong]) {

      row        <- data.frame(symbol, today, close)
      names(row) <- c('symbol', 'date', 'close')

      conn       <- dbConnect(dbDriver('MySQL'),
        dbname=DST_DB_NAME,
        user=DST_DB_USER,
        password=DST_DB_PASS)
      dbWriteTable(conn, 'breakouts', value=row, row.names=FALSE, append=TRUE)
      dbDisconnect(conn) 
      print(paste('Breakout', symbol, '@', close, today))

      minPrice   <- as.vector(close)
      minDate    <- today
      bDate      <- today
    }

    # find entry range
    if (minPrice != -1) {
      if (minPrice > as.vector(close)) {
        minPrice <- as.vector(close)
        minDate  <- today
      }
      points[i] <- minPrice            # lowest price since breakout
      dates[i]  <- as.vector(minDate)  # date when the lowest price occurred
      bdates[i] <- as.vector(bDate)    # date of original breakout
      # stop searching beyond 3 months from breakout
      delta     <- index(close) - minDate
      if (delta > 90) {
        minPrice <- -1
      }
    }
  }
  return(xts(cbind(points, dates, bdates), order.by=index(data)))
}


# finds buy signals (stateless)
buySig <- function(label, data, symbol=symbol, dodiag=dodiag, target=target) {
  n           <- nrow(data)
  buys        <- vector(length=n)

  buy_day     <- function(i, data) {
    smaShort    <- match.names('SMA5', colnames(data))
    macd        <- match.names('MACD.macd', colnames(data))
    macdSig     <- match.names('MACD.signal', colnames(data))
    breakoutCol <- match.names('breakoutSig.points', colnames(data))
    breakoutDa  <- match.names('breakoutSig.dates', colnames(data))
    breakoutBd  <- match.names('breakoutSig.bdates', colnames(data))
    closeCol    <- match.names('Close', colnames(data))

    close    <- as.vector(data[i, closeCol])
    breakout <- data[i, breakoutCol]
    ddate    <- as.Date(as.vector(data[i, breakoutDa]))
    bdate    <- as.Date(as.vector(data[i, breakoutBd]))
    today    <- index(data[i, closeCol])

    # is this a buy situation
    if (breakout      != 0 &&                              # inside of a breakout zone
        close         > (breakout * closeMult) &&          # price higher than LOWEST LOW by X%
        today         > (ddate + buyAfter) &&              # at least X days since LOWEST LOW
        data[i, macd] > data[i, macdSig] &&                # MACD is higher than signal
        close         > (data[i, smaShort] * macdMult)) {  # X% higher than short SMA

      row        <- data.frame(symbol, today + 1, ddate, bdate, data[i, closeCol])
      names(row) <- c('symbol', 'date', 'ddate', 'bdate', 'price')
      conn       <- dbConnect(dbDriver('MySQL'),
        dbname=DST_DB_NAME,
        user=DST_DB_USER,
        password=DST_DB_PASS)
      dbWriteTable(conn, 'buys', value=row, row.names=FALSE, append=TRUE)
      dbDisconnect(conn)
      print(paste('Buy', symbol, '@', today, data[i, closeCol]))

      return(TRUE)
    }
    return(FALSE)
  }

  if (domc == TRUE) {
    buys[startDay:n] <- mclapply(seq(startDay, n), buy_day, data)
  } else {
    buys[startDay:n] <- lapply(seq(startDay, n), buy_day, data)
  }
  return(xts(buys, order.by=index(data)))
}


# create strategy and indicators
s <- strategy('s')

s <- add.indicator(strategy=s, name='SMA', arguments=list(x=quote(Cl(mktdata)), n=shortSMA), label='SMA5')
s <- add.indicator(strategy=s, name='SMA', arguments=list(x=quote(Cl(mktdata)), n=longSMA), label='SMA40')
s <- add.indicator(strategy=s, name='SMA', arguments=list(x=quote(Vo(mktdata)), n=volSMA), label='VMA')
s <- add.indicator(strategy=s, name='MACD', arguments=list(x=quote(Cl(mktdata))), label='MACD')

s <- add.signal(strategy=s, name='breakoutSig', arguments=list(data=quote(mktdata)), label='breakoutSig')
s <- add.signal(strategy=s, name='buySig', arguments=list(data=quote(mktdata)), label='buySig')

run_signals <- function(symbol, dodiag, target) {
  mktdata    <- get(symbol, envir=.GlobalEnv)
  indicators <- applyIndicators(strategy='s', mktdata=mktdata)
  signals    <- applySignals(strategy='s', mktdata=indicators, indicators, symbol=symbol)
  return(TRUE)
}

if (domc == TRUE) {
  out <- mclapply(symbols, run_signals, dodiag=dodiag, target=target)
  return(TRUE)
} else {
  if (dodiag == FALSE) {
    lapply(symbols, run_signals, dodiag=dodiag, target=target)
  } else {
    for (symbol in symbols) {
      run_signals(symbol, dodiag, target)
    }
  }
}
