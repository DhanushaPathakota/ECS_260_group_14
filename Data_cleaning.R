# 1. Load metrics value from csv file
df <- read.csv(file = 'Main_dataset.csv')
df_no_I <- df[(df$status == 1) | (df$status == 2),]
str(df_no_I)
str(df)
summary(df)

# 2. Define "status" as categorical variable (Factor)
df[df$status == 0,]$status <- "I"
df[df$status == 1,]$status <- "G"
df[df$status == 2,]$status <- "R"
df$status <- as.factor(df$status)

df_no_I[df_no_I$status == 1,]$status <- 1
df_no_I[df_no_I$status == 2,]$status <- 0
head(df_no_I)
df_no_I$status <- as.factor(df_no_I$status)

summary(df_no_I)

### Data cleaning ###
## 3. Remove NA values
#	Merged_Forks	merge-to-fork ratio	Merge_Frequency	Fork_Frequency

df_no_na <- df[!(is.na(df$Number_of_Direct_Forks) | is.na(df$merge_to_fork_ratio) | is.na(df$Merge_Frequency) | is.na(df$Fork_Frequency)), ]
summary(df_no_na)

df_no_I_na <- df_no_I[!(is.na(df_no_I$Number_of_Direct_Forks) |  is.na(df_no_I$merge_to_fork_ratio) | is.na(df_no_I$Merge_Frequency) | is.na(df_no_I$Fork_Frequency)), ]
summary(df_no_I_na)
