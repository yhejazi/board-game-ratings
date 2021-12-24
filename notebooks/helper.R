### Helper functions to be used for report.Rmd

# Expand column of strings spearated by sep param into spearate columns
explode <- function(data, var, sep = ",", noval = "NoVal") {
  message(paste('Splitting column', var))
  
  # Create a copy
  df <- as.data.frame(data)
  df$temp <- as.character(df[, var])
  
  # Get unique values
  split = unlist(strsplit(df$temp, ",", fixed = TRUE))
  split_df <- as.data.frame(split)
  split_df$clean <- trimws(split_df$split, which = c("both"))
  
  message(paste('Empty count', sum(is.na(df$temp))))
  split_df$clean[is.na(split_df$clean)]<- noval
  unique_vals= unique(split_df$clean)
  message(paste('Unique count', length(unique_vals)))
  
  # Handle missing/empty
  message(paste('Found missing values', sum(is.na(df$temp))))
  df$temp[is.na(df$temp)]<- noval
  message(paste('Replaced missing values', sum(df$temp == noval)))
  
  l <- strsplit(df$temp, sep)
  mat <- NULL
  for (i in seq_along(unique_vals)) {
    which <- unlist(lapply(l, function(x) any(trimws(x) %in% unique_vals[i])))
    mat <- cbind(mat, which)
  }
  
  # Format col names to be <Name>_category
  colnames(mat) <- gsub('"', "", paste(var, unique_vals, sep = "_"))
  df$temp <- NULL
  df <- cbind(df, mat)
  
  return(df)
}

# Clean joined board game data
clean <- function(data) {
  # Drop unused columns
  data <- subset(data, select = -c(comment, description, mechanic, implementation,
                                   expansion, designer, artist, publisher, playing_time))
  
  data$rating_int <- as.integer(data$rating)
  data <- data[data$rating_int > 0, ] 
  data <- data[!is.na(data$rating_int),] 
  data <- data[data$complexity > 0, ] 
  data <- data[data$year_published <= 2021, ]
  data <- data[data$min_players != 0 & data$min_players != 0, ]
  data$max_players[data$max_players > 15] <- 15
  data$min_players[data$min_players > 15] <- 15
  data <- data[data$max_players - data$min_players >= 0,]
  data <- data[data$min_playtime != 0 & data$max_playtime != 0,]
  data <- data[data$max_playtime - data$min_playtime >= 0,]
  data$game_age <- max(data$year_published, na.rm = TRUE) - data$year_published + 1
  
  return(data)
}