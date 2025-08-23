from db import engine
from models import SubscriptionPlan
from sqlmodel import Session

def create_initial_plans():
    with Session(engine) as session:
        # Check if plans already exist to avoid duplicates
        if session.query(SubscriptionPlan).count() > 0:
            print("Plans already exist. Skipping initialization.")
            return

        plans = [
            SubscriptionPlan(
                name="Free",
                price=0,
                stripe_price_id="price_1P",
                features="Basic CRM, 2 AI Agents"
            ),
            SubscriptionPlan(
                name="Pro",
                price=29,
                stripe_price_id="price_2P",
                features="All Agents, Analytics"
            ),
            SubscriptionPlan(
                name="Team",
                price=99,
                stripe_price_id="price_3P",
                features="Multi-user, Collaboration"
            )
        ]
        session.add_all(plans)
        session.commit()
        print("Success: Created 3 subscription plans")

if __name__ == "__main__":
    create_initial_plans()