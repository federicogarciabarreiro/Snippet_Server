-- Portfolio sample: schema + RPC approach for ecommerce + telemetry.

create table if not exists public.orders (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null,
    status text not null default 'pending',
    currency text not null,
    subtotal numeric(12,2) not null default 0,
    total numeric(12,2) not null default 0,
    stripe_checkout_session_id text unique,
    created_at timestamptz not null default now(),
    paid_at timestamptz
);

create table if not exists public.order_items (
    id uuid primary key default gen_random_uuid(),
    order_id uuid not null references public.orders(id) on delete cascade,
    item_id uuid not null,
    sku text not null,
    item_name text not null,
    quantity int not null check (quantity > 0),
    unit_price numeric(12,2) not null check (unit_price > 0),
    total_price numeric(12,2) generated always as (quantity * unit_price) stored
);

create table if not exists public.stripe_webhook_events (
    id uuid primary key default gen_random_uuid(),
    stripe_event_id text not null unique,
    event_type text not null,
    payload jsonb not null,
    is_processed boolean not null default false,
    received_at timestamptz not null default now(),
    processed_at timestamptz
);

create or replace function public.rpc_mark_stripe_webhook_received(
    p_stripe_event_id text,
    p_event_type text,
    p_payload jsonb
)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
    inserted_rows int;
begin
    insert into public.stripe_webhook_events (stripe_event_id, event_type, payload, is_processed)
    values (p_stripe_event_id, p_event_type, coalesce(p_payload, '{}'::jsonb), false)
    on conflict (stripe_event_id) do nothing;

    get diagnostics inserted_rows = row_count;
    return inserted_rows > 0;
end;
$$;
