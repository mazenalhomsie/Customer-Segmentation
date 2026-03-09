import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df = pd.read_csv('data/user_segments.csv')
    plt.figure(figsize=(12, 7))
    ax = sns.countplot(x='cluster', data=df, hue='cluster', palette='viridis', legend=False)
    plt.title('Distribution of the 5 Customer Personas (Segments)', fontsize=16, pad=20)
    plt.xlabel('Customer Segments (Cluster)', fontsize=12)
    plt.ylabel('Number of Users', fontsize=12)
    
    # Custom Labels
    labels = [
        '0: Young Window Shopper\n(Exclusive discounts)', 
        '1: Frühbucher\n(No cancellation fees)', 
        '2: Familienurlauber\n(1 night free hotel)', 
        '3: Business-Traveller\n(Free hotel meal)', 
        '4: Ältere Urlauber\n(Free checked bag)'
    ]
    plt.xticks(ticks=[0, 1, 2, 3, 4], labels=labels, rotation=45, ha='right')
    
    # Werte auf die Balken schreiben
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig('presentation/Cluster_Verteilung_5.png', dpi=300)
    print('✅ Cluster_Verteilung_5.png successfully created in presentation folder!')
except Exception as e:
    print('Error creating Bar Chart:', e)
