# Placeholder for config loading (env vars, API keys, etc.) 
# AZURE_ENDPOINT="https://synthetic-data-test.openai.azure.com"
# DEPLOYMENT_NAME="synthetic-4o"
OPENAI_API_KEY = "sk-**"
MODEL_NAME = "gpt-4o-mini"

# Supabase Configuration
SUPABASE_URL = "https://siydccpivqusbxyhcvbm.supabase.co/rest/v1/events"
SUPABASE_API_KEY = "sb_secret_3Lnr_sODZfF7gUZBI9RyEg_tO4yEaTw"
SUPABASE_AUTH_TOKEN = "sb_secret_3Lnr_sODZfF7gUZBI9RyEg_tO4yEaTw"

# Event Fetching Configuration
# curl --location 'https://siydccpivqusbxyhcvbm.supabase.co/rest/v1/events?user_id=eq.{user_id}' \
# --header 'apikey: sb_secret_3Lnr_sODZfF7gUZBI9RyEg_tO4yEaTw' \
# --header 'Authorization: Bearer sb_secret_3Lnr_sODZfF7gUZBI9RyEg_tO4yEaTw' \
# --header 'Content-Type: application/json'
SUPABASE_EVENTS_FETCH_URL = "https://siydccpivqusbxyhcvbm.supabase.co/rest/v1/events"