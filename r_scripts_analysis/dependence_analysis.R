setwd("/Users/hugojosebello/Documents/git-repos/data-tuning-scripts-v2/r_scripts_analysis")
all_data <- read.csv("./all.csv",  header=TRUE, sep=";")
all_hombres <- read.csv("./all_hombres.csv",  header=TRUE, sep=";")
all_mujeres <- read.csv("./all_mujeres.csv",  header=TRUE, sep=";")
all_moved <- read.csv("./all_moved.csv",  header=TRUE, sep=";")

r <- with(all_moved, which(noticias_suicidio>270, arr.ind=TRUE))
all_moved <- all_moved[-r, ]

r <- with(all_data, which(noticias_suicidio>270, arr.ind=TRUE))
all_data <- all_data[-r, ]

# Installation
# install.packages('ggplot2')
# Loading
library(ggplot2)
#ine_data$month_code<- as.Date(ine_data$month_code , "%Y/%m/%d")
#install.packages('lubridate')
library(lubridate)

all_data$month <- ymd(all_data$month)

all_data_minus5 = all_data
all_data_minus5$month <- all_data_minus5$month - days(5 *30)

ggplot(all_data, aes(month, noticias_suicidio)) + geom_line() + xlab("") + ylab("Numero noticias suicidio")

ggplot(all_data, aes(month, -media_sentimiento_noticias)) + geom_line() + xlab("") + ylab("Media sentimentos negativos noticias")

ggplot(all_data, aes(month, -sentiment_analysis_score)) + geom_line() + xlab("") + ylab("Score noticias suicidio")

ggplot(all_data, aes(month, suicidios)) + geom_line() + xlab("") + ylab("Numero de suicidios")

plot(all_data$noticias_suicidio, all_data$suicidios, col = "blue", main = "", xlab = "noticias suicidio", ylab = "suicidios")
lm(all_data$noticias_suicidio ~ all_data$suicidios)
abline(lm(all_data$noticias_suicidio ~ all_data$suicidios))


plot(all_data$media_sentimiento_noticias, all_data$suicidios, col = "blue", main = "", xlab = "sentimiento noticias suicidio", ylab = "suicidios")
lm(all_data$media_sentimiento_noticias ~ all_data$suicidios)
abline(lm(all_data$media_sentimiento_noticias ~ all_data$suicidios))

plot(all_data$sentiment_analysis_score, all_data$suicidios, col = "blue", main = "", xlab = "sentimiento noticias suicidio", ylab = "suicidios")
lm(all_data$sentiment_analysis_score ~ all_data$suicidios)
abline(lm(all_data$sentiment_analysis_score ~ all_data$suicidios))


# Pearson correlation: not significative, although it is not the best method since we are
# working with temporal series

cor(all_data$noticias_suicidio, all_data$suicidios)
cor(all_data$media_sentimiento_noticias, all_data$suicidios)
cor(all_data$sentiment_analysis_score, all_data$suicidios)

# https://github.com/AnaBPazos/AlterCorr/blob/master/R/AlterCorrM.R

# Kendall test (non parametric test, alternative to pearson)
cor.test(all_data$suicidios, all_data$noticias_suicidio, method = "kendall")
# it is significative but we can not fully trust it since we are working with time series


# cross-correlation of TIME SERIES

ccf(all_data$noticias_suicidio, all_hombres$suicidios,main="Correlation function: number of suicide news per month\n agaist number of suicides per moth")


ccf(-all_data$media_sentimiento_noticias, all_hombres$suicidios, main="Correlation function: average negative sentiment in news per month\n agaist number of suicides per month")

ccf(-all_data$sentiment_analysis_score, all_hombres$suicidios)


cor.test(all_data$noticias_suicidio, all_data$suicidios)

cor.test(-all_data$media_sentimiento_noticias, all_data$suicidios)

cor.test(-all_data$sentiment_analysis_score, all_data$suicidios)

# men and women not significative differences
ccf(all_hombres$noticias_suicidio, all_hombres$suicidios)

ccf(-all_hombres$media_sentimiento_noticias, all_hombres$suicidios)

ccf(-all_hombres$sentiment_analysis_score, all_hombres$suicidios)


ccf(all_mujeres$noticias_suicidio, all_mujeres$suicidios)

ccf(-all_mujeres$media_sentimiento_noticias, all_mujeres$suicidios)

ccf(-all_mujeres$sentiment_analysis_score, all_mujeres$suicidios)


# interpretation 
# https://support.minitab.com/en-us/minitab/18/help-and-how-to/modeling-statistics/time-series/how-to/cross-correlation/interpret-the-results/all-statistics-and-graphs/

# threadshole
2/sqrt(length(all_data$noticias_suicidio) - 15)

# example ->
# https://nwfsc-timeseries.github.io/atsa-labs/sec-tslab-correlation-within-and-among-time-series.html

# in our case: We find that suicide cases are relatively high after a periode of 10 to 20 months of higher number of news



plot(all_moved$noticias_suicidio, all_moved$suicidios_3_meses_despues, col = "blue", main = "", xlab = "number of suicide news", ylab = "number of suicides after 3 months")
lm(all_moved$noticias_suicidio ~ all_moved$suicidios_3_meses_despues)
abline(lm(all_moved$noticias_suicidio ~ all_moved$suicidios_3_meses_despues))

plot(-all_moved$media_sentimiento_noticias, all_moved$suicidios_3_meses_despues, col = "blue", main = "", xlab = "noticias suicidio", ylab = "suicidios 5 meses después")
lm(-all_moved$media_sentimiento_noticias ~ all_moved$suicidios_3_meses_despues)
abline(lm(-all_moved$media_sentimiento_noticias ~ all_moved$suicidios_3_meses_despues))



cor.test(-all_moved$noticias_suicidio, all_moved$suicidios_3_meses_despues)
cor.test(-all_moved$media_sentimiento_noticias, all_moved$suicidios_3_meses_despues)
cor.test(-all_moved$sentiment_analysis_score, all_moved$suicidios_3_meses_despues)

cor.test(all_moved$noticias_suicidio, all_moved$suicidios_3_meses_despues, method = c("pearson", "kendall", "spearman"))
cor.test(-all_moved$media_sentimiento_noticias, all_moved$suicidios_3_meses_despues, method = c("pearson", "kendall", "spearman"))
cor.test(-all_moved$sentiment_analysis_score, all_moved$suicidios_3_meses_despues, method = c("pearson", "kendall", "spearman"))

plot(all_moved$noticias_suicidio, all_moved$suicidios_4_meses_despues, col = "blue", main = "", xlab = "noticias suicidio", ylab = "suicidios 5 meses después")
lm(-all_moved$noticias_suicidio ~ all_moved$suicidios_4_meses_despues)
abline(lm(-all_moved$noticias_suicidio ~ all_moved$suicidios_4_meses_despues))

plot(-all_moved$media_sentimiento_noticias, all_moved$suicidios_4_meses_despues, col = "blue", main = "", xlab = "noticias suicidio", ylab = "suicidios 5 meses después")
lm(-all_moved$media_sentimiento_noticias ~ all_moved$suicidios_4_meses_despues)
abline(lm(-all_moved$media_sentimiento_noticias ~ all_moved$suicidios_4_meses_despues))


cor.test(-all_moved$noticias_suicidio, all_moved$suicidios_4_meses_despues)
cor.test(-all_moved$media_sentimiento_noticias, all_moved$suicidios_4_meses_despues)
cor.test(-all_moved$sentiment_analysis_score, all_moved$suicidios_4_meses_despues)


plot(all_moved$noticias_suicidio, all_moved$suicidios_5_meses_despues, col = "blue", main = "", xlab = "noticias suicidio", ylab = "suicidios 4 meses después")
lm(-all_moved$noticias_suicidio ~ all_moved$suicidios_5_meses_despues)
abline(lm(-all_moved$noticias_suicidio ~ all_moved$suicidios_5_meses_despues))

plot(all_moved$media_sentimiento_noticias, all_moved$suicidios_5_meses_despues, col = "blue", main = "", xlab = "noticias suicidio", ylab = "suicidios 4 meses después")
lm(-all_moved$media_sentimiento_noticias ~ all_moved$suicidios_5_meses_despues)
abline(-lm(all_moved$media_sentimiento_noticias ~ all_moved$suicidios_5_meses_despues))


cor.test(all_moved$noticias_suicidio, all_moved$suicidios_5_meses_despues)
cor.test(all_moved$media_sentimiento_noticias, -all_moved$suicidios_5_meses_despues)
cor.test(all_moved$sentiment_analysis_score, -all_moved$suicidios_5_meses_despues)


ggplot(all_moved, aes(x=-media_sentimiento_noticias, y=suicidios_3_meses_despues)) +  labs(size = "Number of suicide news\n in same month",y="Number of suicides after 3 moths", x="Average sentiment of negative news") +
  geom_point(aes(size=noticias_suicidio), alpha = 0.5) + geom_smooth()


ggplot(all_moved, aes(x=noticias_suicidio, y=suicidios_3_meses_despues)) + 
  geom_point(aes(size=-media_sentimiento_noticias,  alpha = 0.5)) + geom_smooth()

