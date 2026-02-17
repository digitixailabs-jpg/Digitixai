"""
Stripe Webhook Handler

This module handles all Stripe webhook events for subscription and payment management.
"""
import stripe
from fastapi import APIRouter, Request, HTTPException, status
import structlog

from app.config import settings
from app.services.supabase import supabase_service

logger = structlog.get_logger()
router = APIRouter()

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/stripe")
async def stripe_webhook(request: Request):
    """
    Handle Stripe webhook events.
    
    Verifies the webhook signature and processes the event.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header"
        )
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error("stripe_webhook_invalid_payload", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payload"
        )
    except stripe.error.SignatureVerificationError as e:
        logger.error("stripe_webhook_invalid_signature", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )
    
    # Log the event
    logger.info(
        "stripe_webhook_received",
        event_type=event["type"],
        event_id=event["id"]
    )
    
    # Handle the event
    try:
        if event["type"] == "checkout.session.completed":
            await handle_checkout_completed(event["data"]["object"])
        
        elif event["type"] == "customer.subscription.created":
            await handle_subscription_created(event["data"]["object"])
        
        elif event["type"] == "customer.subscription.updated":
            await handle_subscription_updated(event["data"]["object"])
        
        elif event["type"] == "customer.subscription.deleted":
            await handle_subscription_deleted(event["data"]["object"])
        
        elif event["type"] == "invoice.paid":
            await handle_invoice_paid(event["data"]["object"])
        
        elif event["type"] == "invoice.payment_failed":
            await handle_invoice_payment_failed(event["data"]["object"])
        
        else:
            logger.info("stripe_webhook_unhandled", event_type=event["type"])
    
    except Exception as e:
        logger.exception(
            "stripe_webhook_handler_error",
            event_type=event["type"],
            error=str(e)
        )
        # Return 200 to acknowledge receipt (Stripe will retry otherwise)
        # Log the error for investigation
    
    return {"received": True}


async def handle_checkout_completed(session: dict):
    """
    Handle checkout.session.completed event.
    
    This is triggered when a customer completes the Stripe Checkout flow.
    """
    logger.info(
        "stripe_checkout_completed",
        session_id=session["id"],
        customer_id=session.get("customer"),
        mode=session.get("mode")
    )
    
    # Get customer ID and user ID from metadata
    customer_id = session.get("customer")
    user_id = session.get("client_reference_id")  # We pass user_id here
    
    if not user_id:
        # Try to get from metadata
        user_id = session.get("metadata", {}).get("user_id")
    
    if not user_id:
        logger.error("stripe_checkout_no_user_id", session_id=session["id"])
        return
    
    # Update user profile with Stripe customer ID
    await supabase_service.update_profile(user_id, {
        "stripe_customer_id": customer_id,
    })
    
    # If it's a subscription, the subscription.created event will handle the rest
    # If it's a one-time payment, handle it here
    if session.get("mode") == "payment":
        # Handle one-time payment
        # e.g., add credits, unlock feature, etc.
        amount = session.get("amount_total", 0)
        logger.info(
            "stripe_one_time_payment",
            user_id=user_id,
            amount=amount
        )
        # Add your one-time payment logic here


async def handle_subscription_created(subscription: dict):
    """
    Handle customer.subscription.created event.
    """
    customer_id = subscription.get("customer")
    
    profile = await supabase_service.get_profile_by_stripe_customer(customer_id)
    if not profile:
        logger.error("stripe_subscription_no_profile", customer_id=customer_id)
        return
    
    # Get the price/plan details
    items = subscription.get("items", {}).get("data", [])
    price_id = items[0]["price"]["id"] if items else None
    
    # Map price ID to tier
    tier = get_tier_from_price(price_id)
    
    await supabase_service.update_profile(profile["id"], {
        "subscription_status": subscription.get("status"),
        "subscription_tier": tier,
        "subscription_current_period_end": subscription.get("current_period_end"),
    })
    
    logger.info(
        "stripe_subscription_created",
        user_id=profile["id"],
        tier=tier,
        status=subscription.get("status")
    )


async def handle_subscription_updated(subscription: dict):
    """
    Handle customer.subscription.updated event.
    
    This handles plan changes, status changes, etc.
    """
    customer_id = subscription.get("customer")
    
    profile = await supabase_service.get_profile_by_stripe_customer(customer_id)
    if not profile:
        logger.error("stripe_subscription_no_profile", customer_id=customer_id)
        return
    
    items = subscription.get("items", {}).get("data", [])
    price_id = items[0]["price"]["id"] if items else None
    tier = get_tier_from_price(price_id)
    
    await supabase_service.update_profile(profile["id"], {
        "subscription_status": subscription.get("status"),
        "subscription_tier": tier,
        "subscription_current_period_end": subscription.get("current_period_end"),
    })
    
    logger.info(
        "stripe_subscription_updated",
        user_id=profile["id"],
        tier=tier,
        status=subscription.get("status")
    )


async def handle_subscription_deleted(subscription: dict):
    """
    Handle customer.subscription.deleted event.
    
    This is triggered when a subscription is canceled.
    """
    customer_id = subscription.get("customer")
    
    profile = await supabase_service.get_profile_by_stripe_customer(customer_id)
    if not profile:
        logger.error("stripe_subscription_no_profile", customer_id=customer_id)
        return
    
    await supabase_service.update_profile(profile["id"], {
        "subscription_status": "canceled",
        "subscription_tier": None,
        "subscription_current_period_end": None,
    })
    
    logger.info(
        "stripe_subscription_deleted",
        user_id=profile["id"]
    )


async def handle_invoice_paid(invoice: dict):
    """
    Handle invoice.paid event.
    
    This is triggered when an invoice is paid (including renewals).
    """
    customer_id = invoice.get("customer")
    
    profile = await supabase_service.get_profile_by_stripe_customer(customer_id)
    if not profile:
        logger.error("stripe_invoice_no_profile", customer_id=customer_id)
        return
    
    logger.info(
        "stripe_invoice_paid",
        user_id=profile["id"],
        amount=invoice.get("amount_paid"),
        invoice_id=invoice.get("id")
    )
    
    # You might want to:
    # - Send a receipt email
    # - Add credits if using credit-based system
    # - Update usage limits


async def handle_invoice_payment_failed(invoice: dict):
    """
    Handle invoice.payment_failed event.
    
    This is triggered when a payment fails.
    """
    customer_id = invoice.get("customer")
    
    profile = await supabase_service.get_profile_by_stripe_customer(customer_id)
    if not profile:
        logger.error("stripe_invoice_no_profile", customer_id=customer_id)
        return
    
    logger.warning(
        "stripe_invoice_payment_failed",
        user_id=profile["id"],
        invoice_id=invoice.get("id"),
        attempt_count=invoice.get("attempt_count")
    )
    
    # Update subscription status
    await supabase_service.update_profile(profile["id"], {
        "subscription_status": "past_due",
    })
    
    # You might want to:
    # - Send an email to the user
    # - Show a banner in the app
    # - Restrict access after X failed attempts


def get_tier_from_price(price_id: str | None) -> str | None:
    """
    Map Stripe price ID to subscription tier.
    """
    price_to_tier = {
        settings.STRIPE_PRICE_ID_MONTHLY: "pro",
        settings.STRIPE_PRICE_ID_YEARLY: "pro",
        # Add more mappings as needed
    }
    return price_to_tier.get(price_id)
