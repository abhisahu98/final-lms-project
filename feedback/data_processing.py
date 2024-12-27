import pandas as pd
from .models import UserInteraction

def export_interactions_to_csv(filename="user_interactions.csv"):
    """
    Export user interactions to a CSV file.
    """
    interactions = UserInteraction.objects.all().values()
    df = pd.DataFrame(list(interactions))
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")
