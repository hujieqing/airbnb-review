airbnb <- read.csv("./t/laohu/air_train.csv", stringsAsFactors = F)
sample <- airbnb[1:4, ]


clean <- function(airbnb) {
  a <- function(x) sapply(strsplit(gsub('[{}\"]', '', tolower(x)), ','), trimws)
  airbnb$tfAmenities <- sapply(airbnb$amenities, a)
  allAmenities <- unique(unlist(airbnb$tfAmenities))
  populate <- function(row) {
    for (col in allAmenities) {
      if (col %in% row$tfAmenities) {
        row$col <- 1
      }    
    }
    return(row)
  }
  
  additionalCols <- setNames(data.frame(matrix(ncol = length(allAmenities), nrow = nrow(airbnb))), allAmenities)
  additionalCols[is.na(additionalCols)] <- 0
  newData <- as.data.frame(apply(data.frame(airbnb, additionalCols), 1, populate))
  return(newData)
}

finalData <- clean(airbnb)


