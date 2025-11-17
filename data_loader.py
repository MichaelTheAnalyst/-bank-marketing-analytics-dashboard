"""
Data loading and preprocessing module for Bank Marketing Dashboard
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import os

class BankMarketingDataLoader:
    """Load and preprocess bank marketing data"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.df_encoded = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
    def load_data(self):
        """Load the CSV file"""
        print(f"Loading data from: {self.filepath}")
        self.df = pd.read_csv(self.filepath, sep=';', quotechar='"')
        print(f"Data loaded successfully. Shape: {self.df.shape}")
        return self.df
    
    def basic_info(self):
        """Get basic information about the dataset"""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        info = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'target_distribution': self.df['y'].value_counts().to_dict()
        }
        return info
    
    def clean_data(self):
        """Clean and prepare data"""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Make a copy
        self.df = self.df.copy()
        
        # Convert target to binary
        self.df['y_binary'] = (self.df['y'] == 'yes').astype(int)
        
        # Handle 'unknown' values - keep them as a category for now
        # They might be informative
        
        # Create age groups
        self.df['age_group'] = pd.cut(self.df['age'], 
                                       bins=[0, 25, 35, 45, 55, 65, 100],
                                       labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
        
        # Create campaign intensity categories
        self.df['campaign_intensity'] = pd.cut(self.df['campaign'],
                                               bins=[0, 1, 2, 5, 100],
                                               labels=['1 contact', '2 contacts', '3-5 contacts', '5+ contacts'])
        
        # Was previously contacted?
        self.df['previously_contacted'] = (self.df['pdays'] != 999).astype(int)
        
        # Create duration categories (even though we'll exclude it from modeling)
        self.df['duration_category'] = pd.cut(self.df['duration'],
                                              bins=[0, 100, 300, 600, 5000],
                                              labels=['<100s', '100-300s', '300-600s', '600s+'])
        
        print("Data cleaned successfully")
        return self.df
    
    def encode_features(self, exclude_features=['duration']):
        """Encode categorical features for machine learning"""
        if self.df is None:
            raise ValueError("Data not loaded and cleaned.")
        
        # Create a copy for encoding
        self.df_encoded = self.df.copy()
        
        # Categorical columns to encode
        categorical_cols = ['job', 'marital', 'education', 'default', 'housing', 
                           'loan', 'contact', 'month', 'day_of_week', 'poutcome']
        
        # Label encode categorical variables
        for col in categorical_cols:
            if col in self.df_encoded.columns:
                le = LabelEncoder()
                self.df_encoded[col + '_encoded'] = le.fit_transform(self.df_encoded[col].astype(str))
                self.label_encoders[col] = le
        
        print("Features encoded successfully")
        return self.df_encoded
    
    def get_features_target(self, exclude_duration=True, exclude_features=None):
        """
        Get feature matrix and target variable for modeling
        
        Parameters:
        - exclude_duration: If True, exclude duration (for realistic model)
        - exclude_features: Additional features to exclude
        """
        if self.df_encoded is None:
            self.encode_features()
        
        # Features to use for modeling
        numeric_features = ['age', 'campaign', 'pdays', 'previous',
                          'emp.var.rate', 'cons.price.idx', 'cons.conf.idx',
                          'euribor3m', 'nr.employed']
        
        encoded_features = ['job_encoded', 'marital_encoded', 'education_encoded',
                          'default_encoded', 'housing_encoded', 'loan_encoded',
                          'contact_encoded', 'month_encoded', 'day_of_week_encoded',
                          'poutcome_encoded']
        
        feature_cols = numeric_features + encoded_features
        
        # Exclude duration if specified (for realistic model)
        if exclude_duration and 'duration' in feature_cols:
            feature_cols.remove('duration')
        
        # Exclude additional features if specified
        if exclude_features:
            feature_cols = [f for f in feature_cols if f not in exclude_features]
        
        X = self.df_encoded[feature_cols]
        y = self.df_encoded['y_binary']
        
        return X, y, feature_cols
    
    def get_train_test_split(self, test_size=0.2, random_state=42, exclude_duration=True):
        """Get train-test split"""
        X, y, feature_names = self.get_features_target(exclude_duration=exclude_duration)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert back to DataFrame for feature names
        X_train_scaled = pd.DataFrame(X_train_scaled, columns=feature_names, index=X_train.index)
        X_test_scaled = pd.DataFrame(X_test_scaled, columns=feature_names, index=X_test.index)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, feature_names


def load_and_prepare_data(filepath):
    """Convenience function to load and prepare data"""
    loader = BankMarketingDataLoader(filepath)
    loader.load_data()
    loader.clean_data()
    loader.encode_features()
    return loader


if __name__ == "__main__":
    # Test the loader
    filepath = r"C:\Users\mn3g24\OneDrive - University of Southampton\Desktop\projects\Bank Maketing 2\bank-additional-full.csv"
    loader = load_and_prepare_data(filepath)
    print("\n=== Basic Info ===")
    info = loader.basic_info()
    print(f"Shape: {info['shape']}")
    print(f"Target distribution: {info['target_distribution']}")


