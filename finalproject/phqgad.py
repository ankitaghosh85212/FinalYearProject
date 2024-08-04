
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("depression_anxiety_data.csv")
df1=pd.read_csv("depression_anxiety_data.csv")
print(df.head())
print(df1.head())


colstodrop = ["id", "school_year", "bmi", "who_bmi", "depression_severity", "depression_diagnosis", "anxiety_severity", "depression_treatment",
              "anxiety_diagnosis", "anxiety_treatment", "epworth_score", "sleepiness","depressiveness","suicidal","anxiousness","phq_score"]
df.drop(columns=colstodrop, inplace=True)
print(df.head())

colstodrop1 = ["id", "school_year", "bmi", "who_bmi", "depression_severity", "depression_diagnosis", "anxiety_severity", "depression_treatment",
              "anxiety_diagnosis", "anxiety_treatment", "epworth_score", "sleepiness","depressiveness","suicidal","anxiousness","gad_score"]
df1.drop(columns=colstodrop1, inplace=True)
print(df1.head())
#df["depressiveness"] = df["depressiveness"].astype(bool)
#df["depressiveness_True"] = df["depressiveness"].astype(int)
#df["depressiveness_False"] = (1 - df["depressiveness"]).astype(int)
#df.drop(columns="depressiveness", inplace=True)

#df["suicidal"] = df["suicidal"].astype(bool)
#df["suicidal_True"] = df["suicidal"].astype(int)
#df["suicidal_False"] = (1 - df["suicidal"]).astype(int)
#df.drop(columns="suicidal", inplace=True)

#df["anxiousness"] = df["anxiousness"].astype(bool)
#df["anxiousness_True"] = df["anxiousness"].astype(int)
#df["anxiousness_False"] = (1 - df["anxiousness"]).astype(int)
#df.drop(columns="anxiousness", inplace=True)

df = pd.get_dummies(df, columns=["gender"], prefix="gender",drop_first=True)
df1 = pd.get_dummies(df1, columns=["gender"], prefix="gender",drop_first=True)
age_mapping = {
     18:1,
     19:1,
     20:1,
     21:2,
     22:2,
     23:2,
     24:2,
     25:2,
     26:3,
     27:3,
     28:3,
     29:3,
     30:3,
     31:3,
}
df['Age'] = df['age'].map(age_mapping)
df['Age'] = df['Age'].fillna(0)
print(df['Age'].unique())
df.to_csv('Age', index=False)
print(df.head())

df1['Age'] = df1['age'].map(age_mapping)
df1['Age'] = df1['Age'].fillna(0)
print(df1['Age'].unique())
df1.to_csv('Age', index=False)
print(df1.head())

df.drop(columns='age',inplace=True)
df1.drop(columns='age',inplace=True)
print(df.head())
print(df1.head())

def categorize_depression(score):
    if score >= 1 and score <= 4:
        return "Minimal Depression"
    elif score >= 5 and score <= 9:
        return "Mild Depression"
    elif score >= 10 and score <= 14:
        return "Moderate Depression"
    elif score >= 15 and score <= 19:
        return "Moderately Severe Depression"
    else:
        return "Severe Depression"

def categorize_anxiety(score):
    if score >= 0 and score <= 4:
        return "Minimal Anxiety"
    elif score >= 5 and score <= 9:
        return "Mild Anxiety"
    elif score >= 10 and score <= 14:
        return "Moderate Anxiety"
    else:
        return "Severe Anxiety"

df['Anxiety_Level'] = df['gad_score'].apply(categorize_anxiety)
df1['Depression_Level'] = df1['phq_score'].apply(categorize_depression)


phq_average = df1['phq_score'].mean()
print("phq average score =" , phq_average)
gad_average = df['gad_score'].mean()
print("gad average score =" , gad_average)
columns_with_missing = df.columns[df.isnull().any()]
for column in columns_with_missing:
    if column not in [ "Anxiety_Level"]:
        median_value = df[column].median()
        df[column].fillna(median_value, inplace=True)
    else:
        mode_value = df[column].mode().iloc[0]  # Get the mode (most frequent value)
        df[column].fillna(mode_value, inplace=True)

#df.dropna(subset=["Depression_Level"], inplace=True)


columns_with_missing = df1.columns[df1.isnull().any()]
for column in columns_with_missing:
    if column not in ["Depression_Level"]:
        median_value = df1[column].median()
        df1[column].fillna(median_value, inplace=True)
    else:
        mode_value = df1[column].mode().iloc[0]  # Get the mode (most frequent value)
        df1[column].fillna(mode_value, inplace=True)
#df1.dropna(subset=["Depression_Level"], inplace=True)

X = df.drop(["Anxiety_Level"], axis=1)
X1 = df1.drop(["Depression_Level"], axis=1)
Y_anxiety = df["Anxiety_Level"]
Y_depression = df1["Depression_Level"]

Y_anxiety = Y_anxiety.map({'Minimal Anxiety': 0, 'Mild Anxiety': 1
                              , 'Moderate Anxiety': 2, 'Severe Anxiety': 3})
Y_depression = Y_depression.map({'Minimal Depression': 0, 'Mild Depression': 1,
                                 'Moderate Depression': 2, 'Moderately Severe Depression': 3,
                                 'Severe Depression': 4})

X_train_anxiety, X_test_anxiety, Y_train_anxiety, Y_test_anxiety = train_test_split(X, Y_anxiety, test_size=0.2, random_state=11)
X_train_depression, X_test_depression, Y_train_depression, Y_test_depression = train_test_split(X1, Y_depression, test_size=0.2, random_state=40)

# random forest
print("------------------Random forest-------------------")
from sklearn.ensemble import RandomForestClassifier
modelAnxiety = RandomForestClassifier(n_estimators=40)
modelDepression = RandomForestClassifier(n_estimators=40)
modelAnxiety.fit(X_train_anxiety, Y_train_anxiety)
modelDepression.fit(X_train_depression, Y_train_depression)

joblib.dump(modelAnxiety, 'modelAnxiety.pkl')
joblib.dump(modelDepression, 'modelDepression.pkl')










