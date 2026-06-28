resource "cloudflare_access_identity_provider" "ai_saml" {
  account_id = var.account_id
  name       = "zeazdev-ai-saml"
  type       = "saml"
  config {
    issuer_url        = var.idp_metadata_url
    sso_target_url    = var.idp_metadata_url
    sign_request      = true
  }
}
