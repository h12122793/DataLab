# Load the necessary libraries
library(shiny)
library(dplyr)
library(highcharter)
library(shinythemes)

# Load the data
data <- read.csv("dashboard_data.csv")

# Variable names mapping
variable_names <- c(
  "Electricity" = "elec_cons",
  "Gas" = "gas_cons",
  "Total Biomass" = "totbiom_cons"
)

# Country names mapping
country_names <- c(
  "India" = "IND",
  "Guatemala" = "GTM",
  "Cambodia" = "KHM",
  "Mongolia" = "MNG",
  "Ghana" = "GHA",
  "Brazil" = "BRA",
  "Mexico" = "MEX",
  "Ethiopia" = "ETH"
)

# UI Part
ui <- fluidPage(
  theme = shinytheme("journal"),
  
  # Application title
  titlePanel(
    div(
      style = "text-align:center; font-weight:bold; font-size:24px; color:#003366;",
      "Per Capita Energy Consumption Dashboard"
    )
  ),
  
  # Sidebar with input controls
  sidebarLayout(
    sidebarPanel(
      style = "background-color: #f9f9f9; padding: 15px; border-radius: 10px;",
      
      selectInput(
        inputId = "variable",
        label = h4("Select Variable:"),
        choices = names(variable_names),  
        selected = "Electricity"
      ),
      selectInput(
        inputId = "country",
        label = h4("Select Country:"),
        choices = names(country_names),
        selected = "India"
      ),
      selectizeInput(
        inputId = "region",
        label = h4("Select Region:"),
        choices = NULL,  
        options = list(placeholder = "Search for a region")
      )
    ),
    
    # Main panel for the plot
    mainPanel(
      style = "background-color: #ffffff; padding: 15px; border-radius: 10px;",
      highchartOutput("map", height = "600px", width = "100%"),
      hr(),
      uiOutput("region_details")  
    )
  )
)

# Server
server <- function(input, output, session) {
  
  # Reactive filtering for the selected country and variable
  country_data <- reactive({
    data %>%
      filter(
        country == country_names[input$country] & 
          variable == variable_names[input$variable]
      )
  })
  
  # Reactive expression to get the most recent year for the selected country and variable
  most_recent_year <- reactive({
    if (nrow(country_data()) > 0) {
      max(country_data()$year, na.rm = TRUE)
    } else {
      NA
    }
  })
  
  # Filtered data for the selected country, variable, and most recent year
  filtered_country_data <- reactive({
    if (!is.na(most_recent_year())) {
      country_data() %>%
        filter(year == most_recent_year())
    } else {
      data.frame()
    }
  })
  
  # Update the region choices dynamically
  observe({
    updateSelectizeInput(
      session,
      inputId = "region",
      choices = filtered_country_data()$region,
      server = TRUE
    )
  })
  
  # Render the map
  output$map <- renderHighchart({
    country_data <- filtered_country_data()  
    
    if (nrow(country_data) > 0) {
      country_code <- c(
        "countries/in/in-all", "countries/gt/gt-all", "countries/kh/kh-all",
        "countries/mn/mn-all", "countries/gh/gh-all", "countries/br/br-all",
        "countries/mx/mx-all", "countries/et/et-all"
      )
      names(country_code) <- country_names
      
      hcmap(
        map = country_code[country_names[input$country]],
        data = country_data,
        joinBy = c("hc-key", "hc_key"), 
        name = "Region",  
        value = "value",
        dataLabels = list(enabled = TRUE, format = "{point.name}"), 
        borderColor = "#000000",
        borderWidth = 1,
        tooltip = list(pointFormat = "{point.name}: {point.value}")
      ) |>
        hc_title(
          text = paste(input$country, most_recent_year()), 
          style = list(fontSize = "20px", color = "#333333")
        ) |>
        hc_subtitle(
          text = paste("Per Capita", names(variable_names[variable_names == input$variable]), "consumption in Megajoule"), 
          style = list(fontSize = "16px", color = "#555555")
        ) |>
        hc_colorAxis(
          min = min(country_data$value, na.rm = TRUE),
          max = max(country_data$value, na.rm = TRUE),
          minColor = ifelse(input$variable == "Electricity", "#cceeff",
                            ifelse(input$variable == "Gas", "#ccffcc", "#f5deb3")), # Light Wheat for Biomass
          maxColor = ifelse(input$variable == "Electricity", "#00008B",
                            ifelse(input$variable == "Gas", "#006400", "#8B4513"))  # SaddleBrown for Biomass
        )
      
    } else {
      highchart() %>%
        hc_add_series(
          name = "No Data",
          data = list()
        ) %>%
        hc_title(text = "No data available for selected filters")
    }
  })
  
  # Display region details
  output$region_details <- renderUI({
    if (!is.null(input$region) && input$region != "") {
      selected_region <- filtered_country_data() %>%
        filter(region == input$region)
      
      if (nrow(selected_region) > 0) {
        total_value <- sum(filtered_country_data()$value, na.rm = TRUE)
        fraction <- (selected_region$value / total_value) * 100
        
        div(
          style = "font-size: 16px; color: #333;",
          h4("Region Details"),
          p(paste("Region:", selected_region$region)),
          p(paste("Consumption Value (Megajoule):",selected_region$value)),
          p(paste("Fraction of Country Consumption:", round(fraction, 2), "%"))
        )
      }
    }
  })
}

shinyApp(ui = ui, server = server)

