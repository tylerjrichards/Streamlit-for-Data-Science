import pandas as pd  
 
penguin_df = pd.read_csv('penguins.csv') 
penguin_df.dropna(inplace=True) 
output = penguin_df['species'] 
features = penguin_df[['island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']] 
features = pd.get_dummies(features) 
output, uniques = pd.factorize(output)
print('Here is what our unique output variables represent') 
print(uniques)
print('Here are our feature variables') 
print(features.head())