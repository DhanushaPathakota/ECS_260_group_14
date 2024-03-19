

library(ggplot2)
library(cowplot)
library(ggstatsplot)
library(mlbench)
library(MASS)
library(pROC)

## Before removing outliers ##
## Before removing outliers ##
df <- read.csv(file = 'updatefd_metrics.csv')

# Convert 'status' to a factor with "G" and "R" labels directly after loading the data
df$status <- factor(df$status, levels = c(1, 2), labels = c("G", "R"))

# Now, create df_no_I from the already converted df
df_no_I <- df[df$status %in% c("G", "R"),]

# Proceed with your data cleaning
df_no_na <- na.omit(df)
df_no_I_na <- na.omit(df_no_I)

par(cex.lab=1)



boxplot(Number_of_Forks ~ status, data = df_no_I_na, main = "Number_of_Forks", cex.main = 2, xlab = "Before removing Outliers" , at = c(1,2), col = c("light green","pink"))

boxplot(merge_to_fork_ratio ~ status, data = df_no_I_na, main = "merge_to_fork_ratio", cex.main = 2, xlab = "Before removing Outliers", at = c(1,2), col = c("light green","pink"))
boxplot(Merge_Frequency ~ status, data = df_no_I_na, main = "Merge_Frequency", cex.main = 2, xlab = "Before removing Outliers", at = c(1,2), col = c("light green","pink"))

boxplot(Fork_Frequency ~ status, data = df_no_I_na, main = "Fork_Frequency", cex.main = 2, xlab = "Before removing Outliers", at = c(1,2), col = c("light green","pink"))





## After removing outliers [Status all] ##

Q <- quantile(df_no_na$Number_of_Forks, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df$Number_of_Forks)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
freq_df <- subset(df_no_na, df_no_na$Number_of_Forks > (Q[1] - 1.5*iqr) & df_no_na$Number_of_Forks < (Q[2]+1.5*iqr))

boxplot(Number_of_Forks ~ status, data = freq_df, main = "Number_of_Forks", cex.main = 2, xlab = "After removing Outliers" , at = c(1,2), col = c("light green","pink"))

summary(freq_df$Number_of_Forks)

Q <- quantile(df_no_na$merge_to_fork_ratio, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$merge_to_fork_ratio)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
dem_df <- subset(df_no_na, df_no_na$merge_to_fork_ratio > (Q[1] - 1.5*iqr) & df_no_na$merge_to_fork_ratio < (Q[2]+1.5*iqr))


boxplot(merge_to_fork_ratio ~ status, data = dem_df, 
        main = "Merge to Fork Ratio", cex.main = 2, 
        xlab = "After removing Outliers", col = c("light green","pink"), ylim = c(0, 0.8))

axis(side = 2, at = seq(0, 0.8, by = 0.2), labels = TRUE)

summary(dem_df)



Q <- quantile(df_no_na$Merge_Frequency, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$Merge_Frequency)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
cntr_df <- subset(df_no_na, df_no_na$Merge_Frequency > (Q[1] - 1.5*iqr) & df_no_na$Merge_Frequency< (Q[2]+1.5*iqr))

boxplot(Merge_Frequency ~ status, data = cntr_df, main = "Merge_Frequency", cex.main = 2, xlab = "After removing Outliers", at = c(1,2), col = c("light green","pink"))


Q <- quantile(df_no_na$Fork_Frequency, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$Fork_Frequency)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
add_df <- subset(df_no_na, df_no_na$Fork_Frequency > (Q[1] - 1.5*iqr) & df_no_na$Fork_Frequency < (Q[2]+1.5*iqr))

boxplot(Fork_Frequency ~ status, data = add_df, main = "Fork_Frequency", cex.main = 2, xlab = "After removing Outliers", at = c(1,2), col = c("light green","pink"))

#For communication data
df <- read.csv(file = 'Communication_metrics.csv')



par(cex.lab=1)

IQR_count <- IQR(df_no_I_na$count, na.rm = TRUE)
Q1_count <- quantile(df_no_I_na$count, 0.25, na.rm = TRUE)
Q3_count <- quantile(df_no_I_na$count, 0.75, na.rm = TRUE)


df_no_I_na_c <- df_no_I_na[df_no_I_na$count > (Q1_count - 1.5*IQR_count) &
                             df_no_I_na$count < (Q3_count + 1.5*IQR_count), ]

boxplot(count ~ status, data = df_no_I_na_c , main = "Number_of_emails_exchanged", cex.main = 2,at = c(1,2), col = c("light green","pink"))

IQR_average_length <- IQR(df_no_I_na$average_length, na.rm = TRUE)
Q1_average_length <- quantile(df_no_I_na$average_length, 0.25, na.rm = TRUE)
Q3_average_length <- quantile(df_no_I_na$average_length, 0.75, na.rm = TRUE)


df_no_I_na_a <- df_no_I_na[df_no_I_na$average_length > (Q1_average_length - 1.5*IQR_average_length) &
                             df_no_I_na$average_length < (Q3_average_length + 1.5*IQR_average_length), ]

boxplot( average_length~ status, data = df_no_I_na_a , main = "Average_length_of_messages", cex.main = 2,at = c(1,2), col = c("light green","pink"))

IQR_number_active_senders <- IQR(df_no_I_na$number_active_senders, na.rm = TRUE)
Q1_number_active_senders <- quantile(df_no_I_na$number_active_senders, 0.25, na.rm = TRUE)
Q3_number_active_senders<- quantile(df_no_I_na$number_active_senders, 0.75, na.rm = TRUE)


df_no_I_na_s <- df_no_I_na[df_no_I_na$number_active_senders > (Q1_number_active_senders - 1.5*IQR_number_active_senders) &
                             df_no_I_na$number_active_senders < (Q3_number_active_senders + 1.5*IQR_number_active_senders), ]

boxplot( number_active_senders~ status, data = df_no_I_na_s , main = "Number_of_Active_Senders", cex.main = 2,at = c(1,2), col = c("light green","pink"))


IQR_frequency <- IQR(df_no_I_na$frequency, na.rm = TRUE)
Q1_frequency <- quantile(df_no_I_na$frequency, 0.25, na.rm = TRUE)
Q3_frequency<- quantile(df_no_I_na$frequency, 0.75, na.rm = TRUE)

df_no_I_na_f <- df_no_I_na[df_no_I_na$frequency > (Q1_frequency- 1.5*IQR_frequency) &
                             df_no_I_na$frequency < (Q3_frequency + 1.5*IQR_frequency), ]

boxplot( frequency~ status, data = df_no_I_na_f , main = "Frequency_of_messaging", cex.main = 2,at = c(1,2), col = c("light green","pink"))

