library(dplyr)
library(tidyr)
library(sae)
library(truncnorm)

# Set seed for reproducibility
set.seed(56324)

# List of files to process
file_names <- c(
  "2002.BRA.imputation.csv",
  "2004.IND.imputation.csv",
  "2005.GHA.imputation.csv",
  "2008.BRA.imputation.csv",
  "2010.MNG.imputation.csv",
  "2010.VNM.imputation.csv",
  "2011.IND.imputation.csv",
  "2014.GTM.imputation.csv",
  "2014.KHM.imputation.csv",
  "2014.ZAF.imputation.csv",
  "2017.BRA.imputation.csv",
  "2017.GHA.imputation.csv",
  "2018.ARM.imputation.csv", 
  "2018.ETH.imputation.csv",
  "2018.NGA.imputation.csv",
  "2019.KHM.imputation.csv",
  "2019.NPL.imputation.csv",
  "2019.UGA.imputation.csv",
  "2020.MEX.imputation.csv",
  "2020.RUS.imputation.csv",
  "2020.VNM.imputation.csv",
  "2021.MNG.imputation.csv"
)

# Variables to process
variables <- c("elec_cons", "gas_cons", "totbiom_cons")

# Exclusions: 2020.RUS and 2017.BRA for totbiom_cons
exclude_list <- list(
  "2020.RUS" = "totbiom_cons",
  "2017.BRA" = "totbiom_cons"
)

# Initialize results dataframe
results_df <- data.frame()

for (file in file_names) {
  # Extract year and country from the filename
  file_info <- strsplit(basename(file), split = "\\.")[[1]]
  year <- file_info[1]
  country <- file_info[2]
  
  # Read the file by specifying the path first 
  file_path <- paste0("path", file)
  data <- read.csv(file_path)
  
  # Remove rows with NA in admin1/admin2
  data <- data %>% filter(!is.na(admin1))
  
  # Special handling for Armenia and RUS (`admin1` is numeric)
  if (country == "ARM"  || country == "RUS") {
    data$admin1 <- as.character(data$admin1)
  }
  
  # Use admin2 for BRA instead of admin1 as highchart maps have the regions for that
  grouping_column <- if (country == "BRA" || country == "NGA" || country =="GTM") "admin2" else "admin1"
  
  for (variable in variables) {
    # Check for exclusions
    if (paste0(year, ".", country) %in% names(exclude_list) &&
        variable %in% exclude_list[[paste0(year, ".", country)]]) {
      next
    }
    
    # Calculate sampling error and variance
    sampling_error <- c()
    sampling_var <- c()
    for (region in unique(data[[grouping_column]])) {
      region_data <- data %>%
        filter(.data[[grouping_column]] == region)
      
      # Skip region if data is insufficient
      if (nrow(region_data) == 0) next
      
      sum_squared_diff <- sum((region_data[[variable]] - mean(region_data[[variable]], na.rm = TRUE))^2, na.rm = TRUE)
      sampling_error[region] <- sqrt(sum_squared_diff / nrow(region_data))
      sampling_var[region] <- (sampling_error[region])^2
    }
    
    # Aggregate data by region
    aggregated_data <- data %>%
      group_by(.data[[grouping_column]]) %>%
      summarise(average = mean(.data[[variable]], na.rm = TRUE)) %>%
      ungroup() %>%
      mutate(country = country, year = year) %>%
      relocate(country, year)
    
    # Simulate auxiliary data
    simulated_aux_data <- mapply(
      function(mean_value) rtruncnorm(1, a = 0, mean = mean_value, sd = sd(aggregated_data$average) / 2),
      mean_value = aggregated_data$average
    )
    
    aggregated_data <- aggregated_data %>%
      mutate(aux_data = simulated_aux_data)
    
    # Combine sampling stats
    sampling_stats <- data.frame(
      admin1 = names(sampling_error),
      sampling_error = sampling_error,
      sampling_var = sampling_var
    )
    
    aggregated_data <- aggregated_data %>%
      left_join(sampling_stats, by = setNames("admin1", grouping_column))
    
    # Remove rows with missing or invalid values
    aggregated_data <- aggregated_data %>%
      filter(!is.na(sampling_var) & sampling_var > 0)
    
    # Fit the Fay-Herriot Model
    y <- aggregated_data$average
    aux_var <- aggregated_data$aux_data
    vardir <- aggregated_data$sampling_var
    
    if (nrow(aggregated_data) > 1) {  # Ensure there is enough data for the model
      fh_model <- tryCatch(
        mseFH(y ~ aux_var, vardir = vardir, method = "REML"),
        error = function(e) NULL
      )
      
      # Check if model fitting was successful
      if (!is.null(fh_model)) {
        aggregated_data <- aggregated_data %>%
          mutate(eblup = fh_model$est$eblup)
        
        # Replace EBLUP values smaller than 1e-03 with the average (unrealistic)
        aggregated_data <- aggregated_data %>%
          mutate(eblup = ifelse(eblup < 1e-03, average, eblup))
        
        # Append results
        new_results <- data.frame(
          year = rep(unique(aggregated_data$year), nrow(aggregated_data)),
          country = rep(unique(aggregated_data$country), nrow(aggregated_data)),
          admin1 = aggregated_data[[grouping_column]], 
          variable = variable,
          value = aggregated_data$eblup
        )
        
        results_df <- rbind(results_df, new_results)
      }
    }
  }
}

# Save final results to a CSV file
write.csv(results_df, "sae_results_all.csv", row.names = FALSE)