df <- read.csv(file = "this_one_3.csv")


df$status <- factor(df$status, levels = c(2,1), labels = c("G", "R"))

df_no_I <- df[df$status %in% c("G", "R"),]


df_no_na <- na.omit(df)
df_no_I_na <- na.omit(df_no_I)



IQR_Number_of_Forks <- IQR(df_no_I_na$Number_of_Forks, na.rm = TRUE)
Q1_Number_of_Forks <- quantile(df_no_I_na$Number_of_Forks, 0.25, na.rm = TRUE)
Q3_Number_of_Forks <- quantile(df_no_I_na$Number_of_Forks, 0.75, na.rm = TRUE)

df_no_I_na_f <- df_no_I_na[df_no_I_na$Number_of_Forks > (Q1_Number_of_Forks - 1.5*IQR_Number_of_Forks) &
                             df_no_I_na$Number_of_Forks < (Q3_Number_of_Forks + 1.5*IQR_Number_of_Forks), ]


IQR_merge_to_fork_ratio <- IQR(df_no_I_na$merge_to_fork_ratio, na.rm = TRUE)
Q1_merge_to_fork_ratio <- quantile(df_no_I_na$merge_to_fork_ratio, 0.25, na.rm = TRUE)
Q3_merge_to_fork_ratio <- quantile(df_no_I_na$merge_to_fork_ratio, 0.75, na.rm = TRUE)

df_no_I_na_m <- df_no_I_na[df_no_I_na$merge_to_fork_ratio > (Q1_merge_to_fork_ratio - 1.5*IQR_merge_to_fork_ratio) &
                             df_no_I_na$merge_to_fork_ratio < (Q3_merge_to_fork_ratio + 1.5*IQR_merge_to_fork_ratio), ]

IQR_Fork_Frequency <- IQR(df_no_I_na$Fork_Frequency, na.rm = TRUE)
Q1_Fork_Frequency <- quantile(df_no_I_na$Fork_Frequency, 0.25, na.rm = TRUE)
Q3_Fork_Frequency <- quantile(df_no_I_na$Fork_Frequency, 0.75, na.rm = TRUE)


df_no_I_na_ff <- df_no_I_na[df_no_I_na$Fork_Frequency > (Q1_Fork_Frequency - 1.5*IQR_Fork_Frequency) &
                              df_no_I_na$Fork_Frequency < (Q3_Fork_Frequency + 1.5*IQR_Fork_Frequency), ]

IQR_Merge_Frequency <- IQR(df_no_I_na$Merge_Frequency, na.rm = TRUE)
Q1_Merge_Frequency <- quantile(df_no_I_na$Merge_Frequency, 0.25, na.rm = TRUE)
Q3_Merge_Frequency <- quantile(df_no_I_na$Merge_Frequency, 0.75, na.rm = TRUE)


df_no_I_na_mf <- df_no_I_na[df_no_I_na$Merge_Frequency > (Q1_Merge_Frequency - 1.5*IQR_Merge_Frequency) &
                              df_no_I_na$Merge_Frequency < (Q3_Merge_Frequency + 1.5*IQR_Merge_Frequency), ]



model_forks <- glm(status ~ Number_of_Forks, data=df_no_I_na, family=binomial())
summary(model_forks)

#"Pseudo R-squared" and its p-value
ll.null1 <- model_forks$null.deviance/-2
ll.proposed1 <- model_forks$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null1 - ll.proposed1) / ll.null1



# For Merge to Fork Ratio
model_mfratio <- glm(status ~ merge_to_fork_ratio, data=df_no_I_na_m, family=binomial())
summary(model_mfratio)

#"Pseudo R-squared" and its p-value
ll.null2 <- model_mfratio$null.deviance/-2
ll.proposed2 <- model_mfratio$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null2 - ll.proposed2) / ll.null2


# For Fork Frequency
model_ffreq <- glm(status ~ Fork_Frequency, data=df_no_I_na_ff, family=binomial())
summary(model_ffreq)

#"Pseudo R-squared" and its p-value
ll.null3 <- model_ffreq$null.deviance/-2
ll.proposed3 <- model_ffreq$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null3 - ll.proposed3) / ll.null3



# For Merge Frequency
model_mfreq <- glm(status ~ Merge_Frequency, data=df_no_I_na_mf, family=binomial())
summary(model_mfreq)

#"Pseudo R-squared" and its p-value
ll.null4 <- model_mfreq$null.deviance/-2
ll.proposed4 <- model_mfreq$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null4 - ll.proposed4) / ll.null4