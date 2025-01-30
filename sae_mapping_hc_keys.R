#Le new beginning 
library(highcharter)
library(dplyr)
library(leaflet)

#site to check the maps
#https://code.highcharts.com/mapdata/



#START OF THE CODE HERE
sae_data <- read.csv("new_sae_all.csv")

# mapping for India
ind <- sae_data[sae_data$country =="IND",]
unique(ind$region)

india_hc_keys <- data.frame(
  region = c(
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh",
    "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa",
    "Pondicherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Tripura",
    "Uttar Pradesh", "Uttaranchal", "West Bengal"
  ),
  hc_key= (c(
    "in-ap", "in-ar", "in-as", "in-br", "in-ch", "in-ct",
    "in-dn", "in-dd", "in-dl", "in-ga", "in-gj", "in-hr",
    "in-hp", "in-jk", "in-jh", "in-ka", "in-kl", "in-mp",
    "in-mh", "in-mn", "in-ml", "in-mz", "in-nl", "in-or",
    "in-py", "in-pb", "in-rj", "in-sk", "in-tn", "in-tr",
    "in-up", "in-ut", "in-wb"
  )
))

sae_data <- sae_data %>%
  left_join(india_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "IND", hc_key, NA))


cambodia_hc_keys <- data.frame(
  region = c(
    "Banteay Meanchey", "Battambang", "Kampong Cham", "Kampong Chhnang",
    "Kampong Speu", "Kampong Thom", "Kampot", "Kandal",
    "Kep", "Koh Kong", "Kratie", "Mondul Kiri",
    "Oddar Meanchey", "Pailin", "Phnom Penh", "Preah Sihanouk",
    "Preah Vihear", "Prey Veng", "Pursat", "Ratanak Kiri",
    "Siemreap", "Stung Treng", "Svay Rieng", "Takeo"
  ),
  hc_key_new = c(
    "kh-om", "kh-ba", "kh-km", "kh-kg",
    "kh-kn", "kh-ks", "kh-ka", "kh-ro",
    "kh-kk", "kh-py", "kh-st", "kh-mk",
    "kh-om", "kh-po", "kh-pp", "kh-si",
    "kh-pl", "kh-kt", "kh-ph", "kh-mk",
    "kh-si", "kh-st", "kh-kp", "kh-ta"
  )
)

#left join to merge Cambodia keys

sae_data <- sae_data %>%
  left_join(cambodia_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "KHM" & !is.na(hc_key_new), hc_key_new, hc_key))

# drop the temporary column- hc_key_new
sae_data <- sae_data[,-7]



guatemala_hc_keys <- data.frame(
  region = c(
    "Quiché", "Petén", "Huehuetenango", "Quetzaltenango", "Retalhuleu", "San Marcos",
    "Baja Verapaz", "Alta Verapaz", "Escuintla", "Chimaltenango", "Suchitepéquez",
    "Sacatepéquez", "Sololá", "Totonicapán", "El Progreso", "Santa Rosa",
    "Izabal", "Chiquimula", "Jalapa", "Jutiapa", "Zacapa"
  ),
  hc_key_new = c(
    "gt-qc", "gt-pe", "gt-hu", "gt-qz", "gt-re", "gt-sm",
    "gt-bv", "gt-av", "gt-es", "gt-cm", "gt-su",
    "gt-sa", "gt-so", "gt-to", "gt-pr", "gt-sr",
    "gt-iz", "gt-cq", "gt-ja", "gt-ju", "gt-za"
  )
)

sae_data <- sae_data %>%
  left_join(guatemala_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "GTM" & !is.na(hc_key_new), hc_key_new, hc_key))

# drop the temporary column- hc_key_new
sae_data <- sae_data[,-7]

zaf_hc_keys <- data.frame(
  region = c(
    "Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", 
    "Limpopo", "Mpumalanga", "North West", "Northern Cape", "Western Cape"
  ),
  hc_key_new = c(
    "za-ec", "za-fs", "za-gt", "za-nl", 
    "za-lp", "za-mp", "za-nw", "za-nc", "za-wc"
  )
)

sae_data <- sae_data %>%
  left_join(zaf_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "ZAF" & !is.na(hc_key_new), hc_key_new, hc_key))

# drop the temporary column- hc_key_new
sae_data <- sae_data[,-7]


russia_hc_keys <- data.frame(
  region = c(
    "Adygea", "Altai Republic", "Altai Krai", "Amur Oblast", "Arkhangelsk Oblast", 
    "Astrakhan Oblast", "Bashkortostan", "Belgorod Oblast", "Bryansk Oblast", 
    "Buryatia", "Chechen Republic", "Chelyabinsk Oblast", "Chukotka Autonomous Okrug", 
    "Chuvash Republic", "Dagestan", "Ingushetia", "Irkutsk Oblast", "Ivanovo Oblast", 
    "Jewish Autonomous Oblast", "Kabardino-Balkaria", "Kaliningrad Oblast", 
    "Kalmykia", "Kaluga Oblast", "Kamchatka Krai", "Karachay-Cherkessia", 
    "Karelia", "Kemerovo Oblast", "Khabarovsk Krai", "Khakassia", 
    "Khanty-Mansi Autonomous Okrug", "Kirov Oblast", "Komi Republic", 
    "Kostroma Oblast", "Krasnodar Krai", "Krasnoyarsk Krai", "Kurgan Oblast", 
    "Kursk Oblast", "Leningrad Oblast", "Lipetsk Oblast", "Magadan Oblast", 
    "Mari El Republic", "Mordovia", "Moscow", "Moscow Oblast", "Murmansk Oblast", 
    "Nenets Autonomous Okrug", "Nizhny Novgorod Oblast", "Novgorod Oblast", 
    "Novosibirsk Oblast", "Omsk Oblast", "Orel Oblast", "Orenburg Oblast", 
    "Penza Oblast", "Perm Krai", "Primorsky Krai", "Pskov Oblast", 
    "Rostov Oblast", "Ryazan Oblast", "Sakha (Yakutia)", "Sakhalin Oblast", 
    "Samara Oblast", "Saint Petersburg", "Saratov Oblast", "Smolensk Oblast", 
    "Stavropol Krai", "Sverdlovsk Oblast", "Tambov Oblast", "Tatarstan", 
    "Tomsk Oblast", "Tula Oblast", "Tver Oblast", "Tyumen Oblast", 
    "Tuva", "Udmurt Republic", "Ulyanovsk Oblast", "Vladimir Oblast", 
    "Volgograd Oblast", "Vologda Oblast", "Voronezh Oblast", "Yamalo-Nenets Autonomous Okrug", 
    "Yaroslavl Oblast", "Zabaykalsky Krai"
  ),
  hc_key_new = c(
    "ru-ad", "ru-ar", "ru-ak", "ru-ao", "ru-an", "ru-at", "ru-ba", "ru-be", "ru-br", 
    "ru-bu", "ru-ce", "ru-cl", "ru-ch", "ru-cu", "ru-da", "ru-in", "ru-ir", "ru-iv", 
    "ru-ja", "ru-ka", "ru-kl", "ru-km", "ru-kg", "ru-kt", "ru-kc", "ru-ke", "ru-kz", 
    "ru-kh", "ru-kx", "ru-kn", "ru-ki", "ru-ko", "ru-ks", "ru-kr", "ru-ky", "ru-ku", 
    "ru-kk", "ru-len", "ru-li", "ru-ma", "ru-me", "ru-mr", "ru-mow", "ru-mos", "ru-mu", 
    "ru-nao", "ru-nn", "ru-nv", "ru-ns", "ru-om", "ru-or", "ru-oe", "ru-pe", "ru-pk", 
    "ru-pr", "ru-ps", "ru-ros", "ru-rz", "ru-sa", "ru-sl", "ru-sm", "ru-sr", "ru-st", 
    "ru-sve", "ru-ta", "ru-to", "ru-tu", "ru-ty", "ru-ud", "ru-ul", "ru-vl", "ru-vg", 
    "ru-vd", "ru-vr", "ru-yn", "ru-yo", "ru-za"
  )
)


  region = c(
    "Adygea", "Altai Republic", "Altai Krai", "Amur Oblast", "Arkhangelsk Oblast", 
    "Astrakhan Oblast", "Bashkortostan", "Belgorod Oblast", "Bryansk Oblast", 
    "Buryatia", "Chechen Republic", "Chelyabinsk Oblast", "Chukotka Autonomous Okrug", 
    "Chuvash Republic", "Dagestan", "Ingushetia", "Irkutsk Oblast", "Ivanovo Oblast", 
    "Jewish Autonomous Oblast", "Kabardino-Balkaria", "Kaliningrad Oblast", 
    "Kalmykia", "Kaluga Oblast", "Kamchatka Krai", "Karachay-Cherkessia", 
    "Karelia", "Kemerovo Oblast", "Khabarovsk Krai", "Khakassia", 
    "Khanty-Mansi Autonomous Okrug", "Kirov Oblast", "Komi Republic", 
    "Kostroma Oblast", "Krasnodar Krai", "Krasnoyarsk Krai", "Kurgan Oblast", 
    "Kursk Oblast", "Leningrad Oblast", "Lipetsk Oblast", "Magadan Oblast", 
    "Mari El Republic", "Mordovia", "Moscow", "Moscow Oblast", "Murmansk Oblast", 
    "Nenets Autonomous Okrug", "Nizhny Novgorod Oblast", "Novgorod Oblast", 
    "Novosibirsk Oblast", "Omsk Oblast", "Orel Oblast", "Orenburg Oblast", 
    "Penza Oblast", "Perm Krai", "Primorsky Krai", "Pskov Oblast", 
    "Rostov Oblast", "Ryazan Oblast", "Sakha (Yakutia)", "Sakhalin Oblast", 
    "Samara Oblast", "Saint Petersburg", "Saratov Oblast", "Smolensk Oblast", 
    "Stavropol Krai", "Sverdlovsk Oblast", "Tambov Oblast", "Tatarstan", 
    "Tomsk Oblast", "Tula Oblast", "Tver Oblast", "Tyumen Oblast", 
    "Tuva", "Udmurt Republic", "Ulyanovsk Oblast", "Vladimir Oblast", 
    "Volgograd Oblast", "Vologda Oblast", "Voronezh Oblast", "Yamalo-Nenets Autonomous Okrug", 
    "Yaroslavl Oblast", "Zabaykalsky Krai"
  )
  hc_key_new = c(
    "ru-ad", "ru-al", "ru-ak", "ru-am", "ru-ar", "ru-as", "ru-ba", "ru-be", "ru-br", 
    "ru-bu", "ru-ce", "ru-cl", "ru-co", "ru-cu", "ru-da", "ru-in", "ru-ir", "ru-iv", 
    "ru-ja", "ru-ka", "ru-kl", "ru-km", "ru-kg", "ru-kk", "ru-kc", "ru-ke", "ru-kz", 
    "ru-kh", "ru-kx", "ru-kn", "ru-ki", "ru-ko", "ru-ks", "ru-kr", "ru-ky", "ru-ku", 
    "ru-kk", "ru-len", "ru-li", "ru-ma", "ru-me", "ru-mr", "ru-mow", "ru-mos", "ru-mu", 
    "ru-nao", "ru-nn", "ru-nv", "ru-ns", "ru-om", "ru-or", "ru-oe", "ru-pe", "ru-pk", 
    "ru-pr", "ru-ps", "ru-ros", "ru-rz", "ru-sa", "ru-sl", "ru-sm", "ru-sp", "ru-st", 
    "ru-sve", "ru-ta", "ru-to", "ru-tu", "ru-ty", "ru-ud", "ru-ul", "ru-vl", "ru-vg", 
    "ru-vd", "ru-vr", "ru-yn", "ru-ya", "ru-za"
  )



  
sae_data <- sae_data %>%
  left_join(russia_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "RUS" & !is.na(hc_key_new), hc_key_new, hc_key))

# drop the temporary column- hc_key_new
sae_data <- sae_data[,-7]

# Create the mapping for Mongolia
mongolia_hc_keys <- data.frame(
  region = c(
    "Arhangay", "Bayan-Olgiy", "Bayanhongor", "Bulgan", "Darhan-Uul", "Dornod",
    "Dornogovi", "Dundgovi", "Dzavhan", "Govi-Altay", "Hentiy", "Hovd",
    "Hovsgol", "Omnogovi", "Orhon", "Ovorhangay", "Selenge", "Suhbaatar",
    "Tov", "Ulaanbaatar", "Uvs"
  ),
  hc_key_new = c(
    "mn-ar", "mn-bo", "mn-bh", "mn-bu", "mn-da", "mn-dd",
    "mn-dg", "mn-du", "mn-dz", "mn-ga", "mn-hn", "mn-hd",
    "mn-hg", "mn-og", "mn-er", "mn-oh", "mn-sl", "mn-sb",
    "mn-to", "mn-ub", "mn-uv"
  )
)

# Add hc_key to sae_data using the mapping for Mongolia
sae_data <- sae_data %>%
  left_join(mongolia_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "MNG" & !is.na(hc_key_new), hc_key_new, hc_key))

# Drop the temporary column hc_key_new
sae_data <- sae_data %>%
  select(-hc_key_new)

# Ghana HC key mapping
ghana_hc_keys <- data.frame(
  hc_key_new = c(
    "gh-ah", "gh-ep", "gh-wp", "gh-aa", 
    "gh-tv", "gh-np", "gh-ue", "gh-uw", 
    "gh-ba", "gh-cp"
  ),
  region = c(
    "Ashanti", "Eastern", "Western", "Greater Accra", 
    "Volta", "Northern", "Upper East", "Upper West", 
    "Brong Ahafo", "Central"
  )
)

# Add hc_key to sae_data using the mapping for Ghana
sae_data <- sae_data %>%
  left_join(ghana_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "GHA" & !is.na(hc_key_new), hc_key_new, hc_key))

# Drop the temporary column hc_key_new
sae_data <- sae_data %>%
  select(-hc_key_new)


# Create a dataframe for Brazil hc-key and region mapping
brazil_hc_keys <- data.frame(
  region = c(
    "Acre", "Alagoas", "Amapa", "Amazonas",
    "Bahia", "Ceara", "Distrito Federal", "Espirito Santo",
    "Goias", "Maranhao", "Mato Grosso", "Mato Grosso do Sul",
    "Minas Gerais", "Para", "Paraiba", "Parana",
    "Pernambuco", "Piaui", "Rio Grande do Norte", "Rio Grande do Sul",
    "Rio de Janeiro", "Rondonia", "Roraima", "Santa Catarina",
    "Sao Paulo", "Sergipe", "Tocantins"
  ),
  hc_key_new = c(
    "br-ac", "br-al", "br-ap", "br-am",
    "br-ba", "br-ce", "br-df", "br-es",
    "br-go", "br-ma", "br-mt", "br-ms",
    "br-mg", "br-pa", "br-pb", "br-pr",
    "br-pe", "br-pi", "br-rn", "br-rs",
    "br-rj", "br-ro", "br-rr", "br-sc",
    "br-sp", "br-se", "br-to"
  )
)

# Perform the join to match regions with hc_key_new
sae_data <- sae_data %>%
  left_join(brazil_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "BRA" & !is.na(hc_key_new), hc_key_new, hc_key))

# Drop the temporary hc_key_new column
sae_data <- sae_data %>%
  select(-hc_key_new)

# Verify the updates
head(sae_data)

mexico_hc_keys <- data.frame(
  region = c(
    "BC", "BCS", "Son.", "Col.", "Nay.", "Camp.", "Q. Roo", "Mex.", "Mor.",
    "CDMX", "Qro.", "Tab.", "Chis.", "NL", "Sin.", "Chih.", "Ver.", "Zac.",
    "Ags.", "Jal.", "Mich.", "Oax.", "Pue.", "Gro.", "Tlax.", "Tamps.",
    "Coah.", "Yuc.", "Dgo.", "Gto.", "SLP", "Hgo."
  ),
  hc_key_new = c(
    "mx-bc", "mx-bs", "mx-so", "mx-cl", "mx-na", "mx-cm", "mx-qr", "mx-mx", "mx-mo",
    "mx-df", "mx-qt", "mx-tb", "mx-cs", "mx-nl", "mx-si", "mx-ch", "mx-ve", "mx-za",
    "mx-ag", "mx-ja", "mx-mi", "mx-oa", "mx-pu", "mx-gr", "mx-tl", "mx-tm",
    "mx-co", "mx-yu", "mx-dg", "mx-gj", "mx-sl", "mx-hg"
  )
)

# Merge with the existing dataset to add the hc_key column for Mexico
sae_data <- sae_data %>%
  left_join(mexico_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "MEX" & !is.na(hc_key_new), hc_key_new, hc_key))

# Drop the temporary hc_key_new column
sae_data <- sae_data %>% select(-hc_key_new)

# Create the hc_key mapping for the available regions
ethiopia_hc_keys <- data.frame(
  region = c(
    "Adidis Ababa", "Afar", "Amhara", "Benishangule Gumeze",
    "Dire Dawa", "Gambella", "Harer", "Oromiya",
    "Snnp", "Somali", "Tigray"
  ),
  hc_key_new = c(
    "et-2837", "et-af", "et-am", "et-be",
    "et-dd", "et-ga", "et-ha", "et-aa",
    "et-sn", "et-so", "et-ti"
  )
)

# Merge with the main dataset
sae_data <- sae_data %>%
  left_join(ethiopia_hc_keys, by = "region") %>%
  mutate(hc_key = ifelse(country == "ETH" & !is.na(hc_key_new), hc_key_new, hc_key)) %>%
  select(-hc_key_new) # Drop the temporary column


#mex <-sae_data[sae_data$country =="ETH", ]
#unique(mex$region)

write.csv(sae_data, "dashboard_data.csv")

#Map
variable_to_select <- "gas_cons"
country_t = "IND"

country_code = c("countries/in/in-all", "countries/gt/gt-all", "kh")
names(country_code) <- c("IND", "GTM", "KHM")

country_data <- sae_data %>% 
  filter(((country== "IND"&year==2011 )| country == "KHM" ) & variable ==variable_to_select )
country_data<- country_data[country_data$year==max(unique(country_data$year)),]


hcmap("custom/asia",
  showInLegend = FALSE,
  data = country_data,
  joinBy = c("hc-key", "hc_key"), # Join JSON `hc-key` with GTM's `hc_key`
  name = "region",
  value = "value",
  dataLabels = list(enabled = TRUE, format = "{point.name}"), 
  borderColor = "#000000",
  borderWidth = 1
) |>
  hc_title(text = cat(country_data$country, country_data$year)) |>
  hc_subtitle(text = "Gas consumption in Megajoule per person") |>
  hc_colorAxis(
    min = min(country_data$value, na.rm = TRUE),
    max = max(country_data$value, na.rm = TRUE),
    minColor = "#B0E0E6",  # Light blue for low values
    maxColor = "#00008B"   # Dark blue for high values
  )







