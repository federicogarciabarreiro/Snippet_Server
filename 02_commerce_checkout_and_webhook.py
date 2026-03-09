"""Portfolio sample: checkout simulation with Stripe-compatible persistence."""

from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from app.services.supabase_client import get_supabase_client


def create_checkout_simulated(user_id: str, currency: str, cart_items: list[dict]) -> dict:
    client = get_supabase_client()
    checkout_session_id = f"cs_test_sim_{uuid4().hex[:24]}"

    order = (
        client.table("orders")
        .insert(
            {
                "user_id": user_id,
                "status": "pending",
                "currency": currency.upper(),
                "payment_provider": "stripe",
                "stripe_checkout_session_id": checkout_session_id,
                "metadata": {"simulated": True},
            }
        )
        .execute()
        .data[0]
    )

    subtotal = Decimal("0")
    for row in cart_items:
        unit_price = Decimal(str(row["unit_price"]))
        quantity = int(row["quantity"])
        subtotal += unit_price * quantity

        client.table("order_items").insert(
            {
                "order_id": order["id"],
                "item_id": row["item_id"],
                "sku": row["sku"],
                "item_name": row["name"],
                "quantity": quantity,
                "unit_price": str(unit_price),
                "metadata": {"simulated": True},
            }
        ).execute()

    client.table("orders").update({"subtotal": str(subtotal), "total": str(subtotal)}).eq("id", order["id"]).execute()

    return {
        "order_id": order["id"],
        "checkout_session_id": checkout_session_id,
        "checkout_url": f"/simulated-checkout/{checkout_session_id}",
        "status": "pending",
        "currency": currency.upper(),
        "total": str(subtotal),
        "simulated": True,
    }


def process_simulated_webhook(stripe_event_id: str, checkout_session_id: str) -> dict:
    client = get_supabase_client()

    # Idempotency first: if this event already exists, do nothing.
    inserted = (
        client.table("stripe_webhook_events")
        .insert(
            {
                "stripe_event_id": stripe_event_id,
                "event_type": "checkout.session.completed",
                "payload": {"data": {"object": {"id": checkout_session_id}}},
                "is_processed": False,
            }
        )
        .execute()
        .data
    )
    if not inserted:
        return {"accepted": False, "message": "Duplicate event"}

    order = (
        client.table("orders")
        .select("id,user_id,status")
        .eq("stripe_checkout_session_id", checkout_session_id)
        .limit(1)
        .execute()
        .data[0]
    )

    if order["status"] != "paid":
        order_items = client.table("order_items").select("item_id,quantity").eq("order_id", order["id"]).execute().data
        for item in order_items:
            existing = (
                client.table("user_inventory")
                .select("id,quantity")
                .eq("user_id", order["user_id"])
                .eq("item_id", item["item_id"])
                .limit(1)
                .execute()
                .data
            )
            if existing:
                inv = existing[0]
                client.table("user_inventory").update({"quantity": int(inv["quantity"]) + int(item["quantity"])}).eq("id", inv["id"]).execute()
            else:
                client.table("user_inventory").insert(
                    {
                        "user_id": order["user_id"],
                        "item_id": item["item_id"],
                        "quantity": item["quantity"],
                        "source_order_id": order["id"],
                        "source": "order_paid",
                    }
                ).execute()

        client.table("orders").update(
            {
                "status": "paid",
                "paid_at": datetime.now(timezone.utc).isoformat(),
            }
        ).eq("id", order["id"]).execute()

    client.table("stripe_webhook_events").update(
        {
            "is_processed": True,
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("stripe_event_id", stripe_event_id).execute()

    return {"accepted": True, "order_id": order["id"]}
