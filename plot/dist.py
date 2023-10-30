import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from scipy.stats import gaussian_kde
from sklearn.decomposition import PCA
import numpy as np
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

def plot_hist(intensity_df):
    # Scale the values to be between 0 and 1
    scaler = MinMaxScaler()
    intensity_df_scaled = pd.DataFrame(scaler.fit_transform(intensity_df), columns=intensity_df.columns)

    # Get the column names
    column_names = intensity_df_scaled.columns[:-1]

    # Create a figure with a larger size
    fig, ax = plt.subplots(figsize=(12, 10))

    # Plot all columns on one plot
    for column_name in column_names:
        ax.hist(intensity_df_scaled[column_name], bins=100, alpha=0.5, label=column_name)

    ax.legend(loc='upper right')
    
    # Set x and y limits
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 5000)

    plt.show()
    return None

def contour(intensity_df):
    # Scale the values to be between 0 and 1
    scaler = MinMaxScaler()
    intensity_df_scaled = pd.DataFrame(scaler.fit_transform(intensity_df), columns=intensity_df.columns)

    # Perform PCA on the data
    pca = PCA(n_components=2)
    intensity_df_pca = pd.DataFrame(pca.fit_transform(intensity_df_scaled), columns=['PC1', 'PC2'])

    # Create a figure with a larger size
    fig, ax = plt.subplots(figsize=(12, 10))

    # Define a color map for the points
    cmap = plt.get_cmap('tab10')

    # Plot the points
    ax.scatter(intensity_df_pca['PC1'], intensity_df_pca['PC2'], c=cmap(1))

    # Compute the kernel density estimate
    kde = gaussian_kde(intensity_df_pca.T)

    # Define a grid of points to evaluate the density at
    x, y = np.mgrid[intensity_df_pca['PC1'].min():intensity_df_pca['PC1'].max():200j,
                    intensity_df_pca['PC2'].min():intensity_df_pca['PC2'].max():200j]
    positions = np.vstack([x.ravel(), y.ravel()])

    # Evaluate the density at the grid points
    z = np.reshape(kde(positions).T, x.shape)

    # Plot the density
    ax.contourf(x, y, z, cmap='tab10')
    # Set x and y limits
    ax.set_xlim(intensity_df_pca['PC1'].min(), intensity_df_pca['PC1'].max())
    ax.set_ylim(intensity_df_pca['PC2'].min(), intensity_df_pca['PC2'].max())

    plt.show()
    return None

def plot_density(intensity_df):
    # Scale the values to be between 0 and 1
    scaler = MinMaxScaler()
    intensity_df_scaled = pd.DataFrame(scaler.fit_transform(intensity_df), columns=intensity_df.columns)

    # Get the column names
    column_names = intensity_df_scaled.columns[:-1]

    # Create a figure with a larger size
    _, ax = plt.subplots(figsize=(12, 10))

    # Create density plots for each column
    for column_name in column_names:
        sns.kdeplot(intensity_df_scaled[column_name], label=column_name)

    ax.legend(loc='upper right')
    
    # Set x and y limits
    ax.set_xlim(0, 2)
    
    # Set x and y labels
    ax.set_xlabel('Intensity')
    ax.set_ylabel('Estimated Density')

    plt.show()
    return None

def plot_boxplot(intensity_df):
    # Create a figure with a larger size
    _, ax = plt.subplots(figsize=(12, 10))

    # Create a boxplot for each column
    ax.boxplot(intensity_df)

    # Set x and y labels
    ax.set_xlabel('Column')
    ax.set_ylabel('Intensity')

    plt.show()
    return None
