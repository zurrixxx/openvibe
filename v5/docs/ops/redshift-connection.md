# Redshift Connection

## Architecture

```
localhost:5439 → SSH tunnel → hopper-us (34.215.112.142) → 44.230.97.127:5439 (Redshift)
```

Database: `vibe-cdp`, User: `analysis`

## Setup

### 1. SSH config

Add to `~/.ssh/config`:
```
Host hopper-us
    HostName 34.215.112.142
    User ubuntu
```

### 2. Start tunnel

**Manual (tmux):**
```bash
tmux new -s redshift
ssh -N -L 5439:44.230.97.127:5439 hopper-us
```

**Persistent (autossh):**
```bash
autossh -M 0 -N \
  -o "ServerAliveInterval=30" \
  -o "ServerAliveCountMax=3" \
  -o "ExitOnForwardFailure=yes" \
  -L 5439:44.230.97.127:5439 \
  ubuntu@hopper-us
```

### 3. Environment variables

```bash
export REDSHIFT_HOST=localhost
export REDSHIFT_PORT=5439
export REDSHIFT_DATABASE=vibe-cdp
export REDSHIFT_USER=analysis
export REDSHIFT_PASSWORD=<ask admin>
```

### 4. Test connection

```bash
# Via psql
PGPASSWORD=$REDSHIFT_PASSWORD psql -h localhost -p 5439 -U analysis -d vibe-cdp -c "SELECT 1"

# Via Python (in v5 venv)
python -c "
import redshift_connector
conn = redshift_connector.connect(
    host='localhost', port=5439,
    database='vibe-cdp', user='analysis',
    password='...'
)
print('OK')
conn.close()
"
```

## Schema overview

| Schema | Tables | Content |
|--------|--------|---------|
| `common` | ~20 | dbt production facts + dims (fct_order, fct_ads_*, dim_ads_*) |
| `common_mart_marketing` | ~5 | Pre-built marketing marts |
| `dbt_analytics` | ~280 | Analytics layer (rich fct_website_page_view with 55 cols) |
| `dbt_analytics_prep` | ~245 | Prep/staging layer |
| `dbt_dev` | ~179 | Dev environment (retl_mixpanel_event_* tables) |
| `website` | ~44 | Raw Rudderstack events (pages, generate_lead, order_completed) |
| `hubspot` | ~23 | HubSpot CRM data |
| `salesforce` | ~33 | Salesforce CRM data |
| `klaviyo` | ~4 | Klaviyo email marketing |
| `shopify_webhook` | ~8 | Shopify e-commerce |

Full schema list: 88 schemas. See `shared_memory/data/catalog.yaml` for key tables.

## Redshift gotchas

- No correlated subqueries — use CTE + JOIN
- No `ILIKE ANY(ARRAY[...])` — use multiple OR
- First page in session: use `row_number = 1`
- Bot orders: `products LIKE '%"product_id":"Bot"%'`
- Tunnel drops — use autossh or check tmux session

## Used by

- `RedshiftProvider` (`vibe_inc/tools/analytics/redshift.py`) — reads catalog.yaml, generates dynamic SQL
- `analytics_query_sql` tool — raw SQL execution
- Daily Growth Report — L1/L2/L3 queries
