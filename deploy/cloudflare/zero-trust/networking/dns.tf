# DNS CNAME records routing all zeaz.dev subdomains to zeaz-tunnel
# Tunnel ID: 45667e7e-7383-4265-b53e-6a9e770a8554
locals {
  tunnel_cname = "45667e7e-7383-4265-b53e-6a9e770a8554.cfargotunnel.com"

  # All subdomains routed through zeaz-tunnel
  subdomains = [
    # Identity
    "auth",
    # AI Platform
    "zveo", "zstudio", "analytics", "api-zveo",
    # Financial
    "app", "zpay", "ztreasury", "zwallet",
    # Developer Tools
    "zcloud", "zdash", "api-zdash", "zcfdash", "api-zcfdash", "release",
    # Algo Trading & Games
    "ztrader", "api-ztrader", "zcino",
    # Education & Workspace
    "zacademy", "academy", "zlms", "zoffice", "zow",
    # Automation
    "zfbauto",
    # Agent UI
    "zagents",
    # Root
    "www", "api",
  ]
}

resource "cloudflare_record" "zeaz_tunnel_subdomains" {
  for_each = toset(local.subdomains)

  zone_id = var.zone_id
  name    = each.key
  type    = "CNAME"
  content = local.tunnel_cname
  proxied = true
}

# Root apex record
resource "cloudflare_record" "zeaz_root" {
  zone_id = var.zone_id
  name    = "zeaz.dev"
  type    = "CNAME"
  content = local.tunnel_cname
  proxied = true
}
