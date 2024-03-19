df <- read.csv(file = 'Communication_metrics.csv')

# Convert 'status' to a factor with "G" and "R" labels directly after loading the data
df$status <- factor(df$status, levels = c(2,1), labels = c("G", "R"))

# Now, create df_no_I from the already converted df
df_no_I <- df[df$status %in% c("G", "R"),]

# Proceed with your data cleaning
df_no_na <- na.omit(df)
df_no_I_na <- na.omit(df_no_I)

IQR_count <- IQR(df_no_I_na$count, na.rm = TRUE)
Q1_count <- quantile(df_no_I_na$count, 0.25, na.rm = TRUE)
Q3_count <- quantile(df_no_I_na$count, 0.75, na.rm = TRUE)


df_no_I_na_c <- df_no_I_na[df_no_I_na$count > (Q1_count - 1.5*IQR_count) &
                             df_no_I_na$count < (Q3_count + 1.5*IQR_count), ]

IQR_average_length <- IQR(df_no_I_na$average_length, na.rm = TRUE)
Q1_average_length <- quantile(df_no_I_na$average_length, 0.25, na.rm = TRUE)
Q3_average_length <- quantile(df_no_I_na$average_length, 0.75, na.rm = TRUE)


df_no_I_na_a <- df_no_I_na[df_no_I_na$average_length > (Q1_average_length - 1.5*IQR_average_length) &
                             df_no_I_na$average_length < (Q3_average_length + 1.5*IQR_average_length), ]


IQR_number_active_senders <- IQR(df_no_I_na$number_active_senders, na.rm = TRUE)
Q1_number_active_senders <- quantile(df_no_I_na$number_active_senders, 0.25, na.rm = TRUE)
Q3_number_active_senders<- quantile(df_no_I_na$number_active_senders, 0.75, na.rm = TRUE)


df_no_I_na_s <- df_no_I_na[df_no_I_na$number_active_senders > (Q1_number_active_senders - 1.5*IQR_number_active_senders) &
                             df_no_I_na$number_active_senders < (Q3_number_active_senders + 1.5*IQR_number_active_senders), ]


IQR_frequency <- IQR(df_no_I_na$frequency, na.rm = TRUE)
Q1_frequency <- quantile(df_no_I_na$frequency, 0.25, na.rm = TRUE)
Q3_frequency<- quantile(df_no_I_na$frequency, 0.75, na.rm = TRUE)

df_no_I_na_f <- df_no_I_na[df_no_I_na$frequency > (Q1_frequency- 1.5*IQR_frequency) &
                             df_no_I_na$frequency < (Q3_frequency + 1.5*IQR_frequency), ]



model_forks <- glm(status ~ count, data=df_no_I_na_c, family=binomial())
summary(model_forks)

#"Pseudo R-squared" and its p-value
ll.null1 <- model_forks$null.deviance/-2
ll.proposed1 <- model_forks$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null1 - ll.proposed1) / ll.null1
## chi-square value = 2*(LL(Proposed) - LL(Null))




model_mfratio <- glm(status ~ average_length, data=df_no_I_na_a, family=binomial())
summary(model_mfratio)

#"Pseudo R-squared" and its p-value
ll.null2 <- model_mfratio$null.deviance/-2
ll.proposed2 <- model_mfratio$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null2 - ll.proposed2) / ll.null2



model_ffreq <- glm(status ~ number_active_senders, data=df_no_I_na_s, family=binomial())
summary(model_ffreq)

#"Pseudo R-squared" and its p-value
ll.null3 <- model_ffreq$null.deviance/-2
ll.proposed3 <- model_ffreq$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null3 - ll.proposed3) / ll.null3



model_mfreq <- glm(status ~ frequency, data=df_no_I_na_f, family=binomial())
summary(model_mfreq)

#"Pseudo R-squared" and its p-value
ll.null4 <- model_mfreq$null.deviance/-2
ll.proposed4 <- model_mfreq$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null4 - ll.proposed4) / ll.null4
